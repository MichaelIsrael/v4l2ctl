###############################################################################
# Copyright 2020, Michael Israel
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by
# the European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
#   https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" basis, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence.
###############################################################################
from .v4l2interface import VidIocOps, V4l2Capabilities
from .v4l2formats import V4l2Formats, V4l2FormatDescFlags
from .v4l2frame import V4l2FrameSize
from pathlib import Path


class V4l2Format(object):
    """The v4l2 format information."""
    def __init__(self, ioc_ops, fmt_desc):
        self._ioc_ops = ioc_ops
        self._fmt_desc = fmt_desc

    @property
    def format(self):
        "The format type (see :class:`V4l2Formats`)."
        return V4l2Formats(self._fmt_desc.pixelformat)

    @property
    def description(self):
        "The format description."
        return self._fmt_desc.description.decode()

    @property
    def flags(self):
        "The format flags (see :class:`V4l2FormatDescFlags`)."
        return V4l2FormatDescFlags(self._fmt_desc.flags)

    def sizes(self):
        """A generator function that yiels the available sizes for this
        format."""
        fr_idx = 0
        while fr_idx < 2**32:
            try:
                frm_size = self._ioc_ops.enum_frame_sizes(
                    index=fr_idx,
                    pixel_format=self._fmt_desc.pixelformat)
            except OSError:
                break
            else:
                yield V4l2FrameSize(self._ioc_ops, frm_size)
            fr_idx += 1

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return ("V4l2Format(format={fmt}, description={desc}, flags={flgs})"
                ).format(fmt=self.format.name,
                         desc=self.description,
                         flgs=self.flags)


class V4l2Device(object):
    """Initialize the V4l2Device object and read its basic information.

    Keyword arguments:
        device (str, path-like, int): the video device (default r"/dev/video0")
                if an int is given, it is assumed to be number after "video" in
                "/dev".

    Raises:
        OSError: if a non-video device file is given.
    """
    def __init__(self, device=r"/dev/video0"):
        if isinstance(device, int):
            device = Path(r"/dev/video{}".format(device))

        self._device = device

        # Create VidIocOps object for the ioctl operations.
        self._ioc_ops = VidIocOps(self._device)

        # Query capabilities and basic information
        caps = self._ioc_ops.query_cap()

        self._driver = caps.driver.decode()
        self._name = caps.card.decode()
        self._bus = caps.bus_info.decode()
        # Decode kernel version.
        self._version = ((caps.version & 0xFF0000) >> 16,
                         (caps.version & 0x00FF00) >> 8,
                         (caps.version & 0x0000FF),
                         )
        # General physical capabilities.
        self._physical_caps = V4l2Capabilities(caps.capabilities)
        # If the device has device-specific capabilities store them
        # accordingly. Otherwise, use the physical ones.
        if V4l2Capabilities.DEVICE_CAPS in self._physical_caps:
            self._device_caps = V4l2Capabilities(caps.device_caps)
        else:
            self._device_caps = self._physical_caps

    @property
    def name(self):
        """The card name (read-only)."""
        return self._name

    @property
    def device(self):
        """The device file (read-only)."""
        return self._device

    @property
    def driver(self):
        """The linux driver (read-only)."""
        return self._driver

    @property
    def bus(self):
        """The bus through which this device is connected (read-only)."""
        return self._bus

    @property
    def version(self):
        """The kernel version as a string (read-only)."""
        return "{}.{}.{}".format(*self._version)

    @property
    def version_tuple(self):
        """The kernel version as a tuple (read-only)."""
        return self._version

    @property
    def capabilities(self):
        """The device specific capabilities (read-only).
        These are the capabilities associated with this dev-file only. The
        physical device can have more than one dev-file, and hence more
        capabilities. See physical_capabilities.
        """
        return self._device_caps

    @property
    def physical_capabilities(self):
        """The general physical capabilities (read-only).
        These are the capabilities associated with the physical device as a
        while, and not limited to this dev-file only.
        """
        return self._physical_caps

    @staticmethod
    def iter_devices(skip_links=True):
        """Return an iterator over the available v4l2 devices.

        Keyword arguments:
            skip_links (bool): skip links and return every device only once
                               (default True)

        Returns:
            an iterator
        """
        return V4l2DeviceIterator(skip_links)

    def __repr__(self):
        return "<V4l2Device object for '{}({})'>".format(self.name,
                                                         self.device,
                                                         )

    def iter_buffer_formats(self, buffer_type):
        """Iterate over the formats supported by a certain buffer.

        Keyword arguments:
            buffer_type:

        Returns:
            a generator
        """
        idx = 0
        # Well, I guess the sky is the limit. index is 32 bits wide.
        while idx < 2**32:
            try:
                fmt_desc = self._ioc_ops.enum_fmt(index=idx, type=buffer_type)
            except OSError:
                break
            else:
                yield V4l2Format(self._ioc_ops, fmt_desc)
            idx += 1


class V4l2DeviceIterator(object):
    _v4l2_device_prefixes = ["video",
                             "radio",
                             "vbi",
                             "swradio",
                             "v4l-subdev",
                             ]

    def __init__(self, skip_links):
        self._skip_links = skip_links

    def __iter__(self):
        dev_list = []
        extend_dev_list = dev_list.extend

        # Find all devices conforming to the v4l2 devices pattern.
        slash_dev = Path(r"/dev")
        for prefix in self._v4l2_device_prefixes:
            extend_dev_list(slash_dev.glob(prefix+"*"))

        if self._skip_links:
            # Find redundant links.
            to_remove = []
            for idx, dev in enumerate(dev_list):
                if dev.is_symlink() and dev.resolve() in dev_list:
                    to_remove.append(idx)

            # Remove links.
            for dev_idx in reversed(to_remove):
                del dev_list[dev_idx]

        # Try to instanciate a V4l2Device object and yield it if successful.
        for dev in dev_list:
            try:
                dev_instance = V4l2Device(dev)
            except OSError:
                continue
            else:
                yield dev_instance

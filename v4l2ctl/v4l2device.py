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
from .ioctls import V4l2IocOps, V4l2Capabilities, V4l2BufferType, IoctlError
from .v4l2types import V4l2Rectangle, V4l2CroppingCapabilities
from .v4l2format import V4l2Format
from pathlib import Path
from .utils.filehandle import FileHandleCM, FileHandleStatus
import io


class FeatureNotSupported(Exception):
    pass


class V4l2Device(io.IOBase):
    """Initialize the V4l2Device object and read its basic information.

    Keyword arguments:
        device (str, path-like, int): the video device (default r"/dev/video0")
                if an int is given, it is assumed to be number after "video" in
                "/dev".

    Raises:
        IoctlError: if a non-video device file is given.
    """

    cropping_buffer_types = [V4l2BufferType.VIDEO_CAPTURE,
                             V4l2BufferType.VIDEO_CAPTURE_MPLANE,
                             V4l2BufferType.VIDEO_OUTPUT,
                             V4l2BufferType.VIDEO_OUTPUT_MPLANE,
                             V4l2BufferType.VIDEO_OVERLAY,
                             ]

    ###########################################################################
    # Constructor.
    ###########################################################################
    def __init__(self, device=r"/dev/video0"):
        if isinstance(device, int):
            device = Path(r"/dev/video{}".format(device))

        self._dev_handle = FileHandleCM(device, {"mode": "rb"})

        # Create V4l2IocOps object for the ioctl operations.
        self._ioc_ops = V4l2IocOps(self._dev_handle)

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

        # Find the supported buffer types.
        self._supported_buffer_types = [buftype for buftype in V4l2BufferType
                                        if V4l2Capabilities[buftype.name]
                                        in self._device_caps]

        # Use the first supported buffer type as default.
        self._buffer_type = self._supported_buffer_types[0]

    ###########################################################################
    # I/O Interface
    ###########################################################################
    def __enter__(self):
        self._open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def _open(self):
        self._dev_handle.open()

    def close(self):
        self._dev_handle.close()

    @property
    def closed(self):
        return self._dev_handle.status == FileHandleStatus.Closed

    def fileno(self):
        if self.closed:
            raise ValueError("I/O operation on closed file")
        return self._dev_handle.fileno()

    def seekable(self):
        return False

    def flush(self):
        pass

    def isatty(self):
        return False

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration()
        return line

    def readable(self):
        # TODO
        return False

    def readline(self, size=-1):
        # TODO
        raise io.UnsupportedOperation("readline")

    def readlines(self, hint=-1):
        # TODO
        raise io.UnsupportedOperation("readlines")

    def writable(self):
        return False

    def writelines(self, lines):
        raise io.UnsupportedOperation("writelines")

    ###########################################################################
    # Device properties.
    ###########################################################################
    @property
    def name(self):
        """The card name (read-only)."""
        return self._name

    @property
    def device(self):
        """The device file (read-only)."""
        return self._dev_handle.filename

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

    @property
    def cropping_capabilities(self):
        """The cropping capabilities (read-only).
        These are the cropping capabilities of this video device.

        Only valid for these buffer types:
            * V4l2BufferType.VIDEO_CAPTURE
            * V4l2BufferType.VIDEO_CAPTURE_MPLANE
            * V4l2BufferType.VIDEO_OUTPUT
            * V4l2BufferType.VIDEO_OUTPUT_MPLANE
            * V4l2BufferType.VIDEO_OVERLAY
        """
        if self.buffer_type not in self.cropping_buffer_types:
            raise FeatureNotSupported(
                "Cropping is not supported for " + str(self.buffer_type) +
                ". Supported buffer types: " + str([b.name for b in
                                                    self.cropping_buffer_types]
                                                   ))
        # Query cropping capabilities.
        crop_caps = self._ioc_ops.crop_cap(type=self.buffer_type)
        return V4l2CroppingCapabilities._from_v4l2(crop_caps)

    ###########################################################################
    # V4L2 setters, getters and iterators/generators.
    ###########################################################################
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
            buffer_type: see :class:`V4l2BufferType`.

        Returns:
            a generator
        """
        idx = 0
        # Well, I guess the sky is the limit. index is 32 bits wide.
        while idx < 2**32:
            try:
                fmt_desc = self._ioc_ops.enum_fmt(index=idx, type=buffer_type)
            except IoctlError:
                break
            else:
                yield V4l2Format(self._ioc_ops, fmt_desc)
            idx += 1

    @property
    def formats(self):
        """A generator for the suported formats by this video device.

        Note:
            The formats are specfic to the set buffer type. (See
            :py:attr:`~buffer_type`)
        """
        return self.iter_buffer_formats(self.buffer_type)

    @property
    def supported_buffer_types(self):
        """The supported buffer types by this video device (read-only)."""
        return self._supported_buffer_types

    @property
    def buffer_type(self):
        """The buffer type (see :class:`V4l2BufferType`) required for several
        operations. This attribute does not change anything in the device
        itself. It is used by other operations.
        """
        return self._buffer_type

    @buffer_type.setter
    def buffer_type(self, buffer_type):
        """Setter for buffer_type."""
        if V4l2BufferType(buffer_type) not in self.supported_buffer_types:
            raise ValueError("This device supports only the following buffer" +
                             " types: " + str([b.name for b in
                                               self.supported_buffer_types]))
        self._buffer_type = buffer_type

    @property
    def cropping_rectangle(self):
        """The cropping rectangle (see :class:`V4l2Rectangle`).

        Note:
            The cropping rectange is specfic to the set buffer type. (See
            :py:attr:`~buffer_type`)
        """
        try:
            cropping = self._ioc_ops.get_crop(type=self._buffer_type)
        except IoctlError as e:
            if "Errno 22" in str(e):
                raise FeatureNotSupported("Cropping is not supported") \
                    from None
            else:
                raise
        return V4l2Rectangle._from_v4l2(cropping.c)

    @cropping_rectangle.setter
    def cropping_rectangle(self, rectangle):
        """Setter for cropping_rectangle."""
        try:
            self._ioc_ops.set_crop(type=self._buffer_type,
                                   c=rectangle._to_v4l2())
        except IoctlError as e:
            if "Errno 25" in str(e):
                raise FeatureNotSupported("Cropping is not supported") \
                    from None


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
            except IoctlError:
                continue
            else:
                yield dev_instance

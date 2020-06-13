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
from .v4l2interface import VidIocOps, CapabilityFlags


class V4l2Capabilities(int):
    """The v4l2 capabilities.
    This is basically an 'int' that supports checking if a certain capability
    is supported using the 'in' operator.

    Example:
        Check if device /dev/video0 supports video capturing::

            vid_dev = VideoDevice(r"/dev/video0")
            if CapabilityFlags.VIDEO_CAPTURE in vid_dev.capabilities:
                start_recording()
    """
    def __init__(self, caps):
        self._caps = caps

    def __contains__(self, capability):
        return (capability | self) != 0

    def __repr__(self):
        return "<VideoCapabilities: {:#010X}>".format(self._caps)


class V4l2Device(object):
    """Initialize the VideoDevice object and read its basic information.

    Keyword arguments:
        device: the video device (default r"/dev/video0")

    Raises:
        OSError: if a non-video device file is given.
    """
    def __init__(self, device=r"/dev/video0"):
        self._device = device
        # Create VidIocOps object for the ioctl operations.
        self._ioc_ops = VidIocOps(self._device)

        # Query capabilities and basic information
        caps = self._ioc_ops.querycap()

        self._driver = caps.driver.decode()
        self._name = caps.card.decode()
        self._bus = caps.bus_info.decode()
        # Decode kernel version.
        self._version = "{}.{}.{}".format((caps.version & 0xFF0000) >> 16,
                                          (caps.version & 0x00FF00) >> 8,
                                          (caps.version & 0x0000FF)
                                          )
        # General physical capabilities.
        self._physical_caps = V4l2Capabilities(caps.capabilities)
        # If the device has device-specific capabilities store them
        # accordingly. Otherwise, use the physical ones.
        if CapabilityFlags.DEVICE_CAPS in self._physical_caps:
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
        """The kernel version (read-only)."""
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

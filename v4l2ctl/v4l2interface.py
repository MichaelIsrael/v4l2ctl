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
from .ioctlmacros import _IOC, _IOC_READ, _IOC_WRITE, _IOC_TYPECHECK
from enum import IntFlag, IntEnum
from fcntl import ioctl
import ctypes


###############################################################################
# Exception classes
###############################################################################
class IoctlError(Exception):
    """Raised when ioctl() returns a non-zero value."""
    def __init__(self, device, name, request, return_code):
        super().__init__()
        self._info = {"device": device,
                      "name": name,
                      "request": request,
                      "return_code": return_code,
                      }

    def __str__(self):
        return("The ioctl request '{name}' ({request:#X}) on '{device}' "
               "returned '{return_code}'.").format(**self._info)


###############################################################################
# From linux/videodev2.h
#
# /**
#   * struct v4l2_capability - Describes V4L2 device caps returned by
#   * VIDIOC_QUERYCAP
#   *
#   * @driver:       name of the driver module (e.g. "bttv")
#   * @card:         name of the card (e.g. "Hauppauge WinTV")
#   * @bus_info:     name of the bus (e.g. "PCI:" + pci_name(pci_dev) )
#   * @version:      KERNEL_VERSION
#   * @capabilities: capabilities of the physical device as a whole
#   * @device_caps:  capabilities accessed via this particular device (node)
#   * @reserved:     reserved fields for future extensions
#   */
###############################################################################
class V4l2Capability(ctypes.Structure):
    """An implementation of struct v4l2_capability (linux/videodev.h)

    Attributes:
        driver: name of the driver module (e.g. "bttv")
        card: name of the card (e.g. "Hauppauge WinTV")
        bus_info: name of the bus (e.g. "PCI:" + pci_name(pci_dev) )
        version: KERNEL_VERSION
        capabilities: capabilities of the physical device as a whole
        device_caps: capabilities accessed via this particular device (node)

    See also class CapabilityFlags.

    :meta private:
    """
    _fields_ = [
        ('driver', ctypes.c_char * 16),
        ('card', ctypes.c_char * 32),
        ('bus_info', ctypes.c_char * 32),
        ('version', ctypes.c_uint32),
        ('capabilities', ctypes.c_uint32),
        ('device_caps', ctypes.c_uint32),
        ('reserved', ctypes.c_uint32 * 3),
    ]

    driver = None  # :noindex:
    # :noindex:
    card = None
    bus_info = None
    version = None
    capabilities = None
    device_caps = None


###############################################################################
# An abstraction of the capabilities' directives defined in linux/videodev2.h.
###############################################################################
class CapabilityFlags(IntFlag):
    """Values for the 'capabilities' field in V4l2Capability().  """
    #: Is a video capture device.
    VIDEO_CAPTURE = 0x00000001
    #: Is a video output device.
    VIDEO_OUTPUT = 0x00000002
    #: Can do video overlay.
    VIDEO_OVERLAY = 0x00000004

    #: Is a raw VBI capture device.
    VBI_CAPTURE = 0x00000010
    #: Is a raw VBI output device.
    VBI_OUTPUT = 0x00000020
    #: Is a sliced VBI capture device.
    SLICED_VBI_CAPTURE = 0x00000040
    #: Is a sliced VBI output device.
    SLICED_VBI_OUTPUT = 0x00000080

    #: RDS data capture.
    RDS_CAPTURE = 0x00000100
    #: Can do video output overlay.
    VIDEO_OUTPUT_OVERLAY = 0x00000200
    #: Can do hardware frequency seek.
    HW_FREQ_SEEK = 0x00000400
    #: Is an RDS encoder.
    RDS_OUTPUT = 0x00000800

    #: Is a video capture device that supports multiplanar formats.
    VIDEO_CAPTURE_MPLANE = 0x00001000
    #: Is a video output device that supports multiplanar formats.
    VIDEO_OUTPUT_MPLANE = 0x00002000
    #: Is a video mem-to-mem device that supports multiplanar formats.
    VIDEO_M2M_MPLANE = 0x00004000
    #: Is a video mem-to-mem device.
    VIDEO_M2M = 0x00008000

    #: Has a tuner.
    TUNER = 0x00010000
    #: Has audio support.
    AUDIO = 0x00020000
    #: Is a radio device.
    RADIO = 0x00040000
    #: Has a modulator.
    MODULATOR = 0x00080000

    #: Is a SDR capture device.
    SDR_CAPTURE = 0x00100000
    #: Supports the extended pixel format.
    EXT_PIX_FORMAT = 0x00200000
    #: Is a SDR output device.
    SDR_OUTPUT = 0x00400000
    #: Is a metadata capture device.
    META_CAPTURE = 0x00800000

    #: Read/write systemcalls.
    READWRITE = 0x01000000
    #: Async I/O.
    ASYNCIO = 0x02000000
    #: Streaming I/O ioctls.
    STREAMING = 0x04000000
    #: Is a metadata output device.
    META_OUTPUT = 0x08000000

    #: Is a touch device.
    TOUCH = 0x10000000
    #: Sets device capabilities field.
    DEVICE_CAPS = 0x80000000


###############################################################################
# An abstraction for all ioctl operations.
###############################################################################
class IoctlDirection(IntEnum):
    """The ioctl direction, i.e., Read, Write or both.

    :meta private:
    """
    R = _IOC_READ
    W = _IOC_WRITE
    RW = R | W


class IoctlAbstraction(object):
    """An abstraction for perfroming ioctl operations

    Keyword arguments:
        device: the device file subject to the ioctl-request.
        name: A name describing this request.
        direction: A member of IoctlDirection
        device_type: device type as used by the _IO macros.
        number: request code number as used by the _IO macros.
        buffer_type: the class used to instanciate the C-struct buffer
                     used by the ioctl-request.

    :meta private:
    """
    def __init__(self, device, name, direction, device_type, number,
                 buffer_type):
        self._device = device
        self._name = name
        self._buffer_type = buffer_type
        # Create ioctl request-code.
        self._code = _IOC(direction,
                          device_type,
                          number,
                          _IOC_TYPECHECK(buffer_type),
                          )

    def __call__(self):
        """Runs the ioctl request and returns the buffers."""
        # Create the buffer.
        buff = self._buffer_type()

        # Run the ioctl request.
        with open(self._device, "rb") as dev_fd:
            ret_code = ioctl(dev_fd, self._code, buff)

        # I couldn't figure out a scenario where ret_code is none zero, because
        # so far an exception is always raised when there is an error with the
        # ioctl call. But the python documentation says the return code will be
        # passed back to python, so anyway, better safe than sorry :)
        if ret_code != 0:
            raise IoctlError(self._device, self._name, self._code, ret_code)

        return buff


###############################################################################
# An abstraction for supported ioctl operations on V4L2 devices.
###############################################################################
class VidIocOps(object):
    """Abstraction for ioctl operations on v4l2 devices.
    see LINUX_HEADERS/include/media/v4l2-ioctl.h: struct v4l2_ioctl_ops.
    see include/videodev2.h

    Keyword Arguments:
        device (str): the video device file.

    :meta private:
    """
    def __init__(self, device):
        # This page is intentionally empty. ;)
        pass

    def __new__(cls, device):
        # Create base object.
        obj = super().__new__(cls)
        # Add real callables.
        obj.querycap = IoctlAbstraction(device, "QueryCap", IoctlDirection.R,
                                        'V', 0, V4l2Capability)
        return obj

    ###########################################################################
    # The following are dummy functions for documentation purpose only. The
    # real callables are assigned in __new__.
    ###########################################################################
    def querycap(self):
        """Interface to the ioctl code VIDIOC_QUERYCAP.
        For more information see struct v4l2_capability in include/videodev2.h.
        """

    # TODO:
    """
    ENUM_FMT = _IOWR('V',  2, V4l2Fmtdesc)
    G_FMT = _IOWR('V',  4, V4l2Format)
    S_FMT = _IOWR('V',  5, V4l2Format)
    REQBUFS = _IOWR('V',  8, V4l2Requestbuffers)
    QUERYBUF = _IOWR('V',  9, V4l2Buffer)
    G_FBUF = _IOR('V', 10, V4l2Framebuffer)
    S_FBUF = _IOW('V', 11, V4l2Framebuffer)
    OVERLAY = _IOW('V', 14, int)
    QBUF = _IOWR('V', 15, V4l2Buffer)
    EXPBUF = _IOWR('V', 16, V4l2Exportbuffer)
    DQBUF = _IOWR('V', 17, V4l2Buffer)
    STREAMON = _IOW('V', 18, int)
    STREAMOFF = _IOW('V', 19, int)
    G_PARM = _IOWR('V', 21, V4l2Streamparm)
    S_PARM = _IOWR('V', 22, V4l2Streamparm)
    G_STD = _IOR('V', 23, v4l2_std_id)
    S_STD = _IOW('V', 24, v4l2_std_id)
    ENUMSTD = _IOWR('V', 25, V4l2Standard)
    ENUMINPUT = _IOWR('V', 26, V4l2Input)
    G_CTRL = _IOWR('V', 27, V4l2Control)
    S_CTRL = _IOWR('V', 28, V4l2Control)
    G_TUNER = _IOWR('V', 29, V4l2Tuner)
    S_TUNER = _IOW('V', 30, V4l2Tuner)
    G_AUDIO = _IOR('V', 33, V4l2Audio)
    S_AUDIO = _IOW('V', 34, V4l2Audio)
    QUERYCTRL = _IOWR('V', 36, V4l2Queryctrl)
    QUERYMENU = _IOWR('V', 37, V4l2Querymenu)
    G_INPUT = _IOR('V', 38, int)
    S_INPUT = _IOWR('V', 39, int)
    G_EDID = _IOWR('V', 40, V4l2Edid)
    S_EDID = _IOWR('V', 41, V4l2Edid)
    G_OUTPUT = _IOR('V', 46, int)
    S_OUTPUT = _IOWR('V', 47, int)
    ENUMOUTPUT = _IOWR('V', 48, V4l2Output)
    G_AUDOUT = _IOR('V', 49, V4l2Audioout)
    S_AUDOUT = _IOW('V', 50, V4l2Audioout)
    G_MODULATOR = _IOWR('V', 54, V4l2Modulator)
    S_MODULATOR = _IOW('V', 55, V4l2Modulator)
    G_FREQUENCY = _IOWR('V', 56, V4l2Frequency)
    S_FREQUENCY = _IOW('V', 57, V4l2Frequency)
    CROPCAP = _IOWR('V', 58, V4l2Cropcap)
    G_CROP = _IOWR('V', 59, V4l2Crop)
    S_CROP = _IOW('V', 60, V4l2Crop)
    G_JPEGCOMP = _IOR('V', 61, V4l2Jpegcompression)
    S_JPEGCOMP = _IOW('V', 62, V4l2Jpegcompression)
    QUERYSTD = _IOR('V', 63, v4l2_std_id)
    TRY_FMT = _IOWR('V', 64, V4l2Format)
    ENUMAUDIO = _IOWR('V', 65, V4l2Audio)
    ENUMAUDOUT = _IOWR('V', 66, V4l2Audioout)
    G_PRIORITY = _IOR('V', 67, __u32)
    S_PRIORITY = _IOW('V', 68, __u32)
    G_SLICED_VBI_CAP = _IOWR('V', 69, V4l2SlicedVbiCap)
    LOG_STATUS = _IO('V', 70)
    G_EXT_CTRLS = _IOWR('V', 71, V4l2ExtControls)
    S_EXT_CTRLS = _IOWR('V', 72, V4l2ExtControls)
    TRY_EXT_CTRLS = _IOWR('V', 73, V4l2ExtControls)
    ENUM_FRAMESIZES = _IOWR('V', 74, V4l2Frmsizeenum)
    ENUM_FRAMEINTERVALS = _IOWR('V', 75, V4l2Frmivalenum)
    G_ENC_INDEX = _IOR('V', 76, V4l2EncIdx)
    ENCODER_CMD = _IOWR('V', 77, V4l2EncoderCmd)
    TRY_ENCODER_CMD = _IOWR('V', 78, V4l2EncoderCmd)
    DBG_S_REGISTER = _IOW('V', 79, V4l2DbgRegister)
    DBG_G_REGISTER = _IOWR('V', 80, V4l2DbgRegister)
    S_HW_FREQ_SEEK = _IOW('V', 82, V4l2HwFreqSeek)
    S_DV_TIMINGS = _IOWR('V', 87, V4l2DvTimings)
    G_DV_TIMINGS = _IOWR('V', 88, V4l2DvTimings)
    DQEVENT = _IOR('V', 89, V4l2Event)
    SUBSCRIBE_EVENT = _IOW('V', 90, V4l2EventSubscription)
    UNSUBSCRIBE_EVENT = _IOW('V', 91, V4l2EventSubscription)
    CREATE_BUFS = _IOWR('V', 92, V4l2CreateBuffers)
    PREPARE_BUF = _IOWR('V', 93, V4l2Buffer)
    G_SELECTION = _IOWR('V', 94, V4l2Selection)
    S_SELECTION = _IOWR('V', 95, V4l2Selection)
    DECODER_CMD = _IOWR('V', 96, V4l2DecoderCmd)
    TRY_DECODER_CMD = _IOWR('V', 97, V4l2DecoderCmd)
    ENUM_DV_TIMINGS = _IOWR('V', 98, V4l2EnumDvTimings)
    QUERY_DV_TIMINGS = _IOR('V', 99, V4l2DvTimings)
    DV_TIMINGS_CAP = _IOWR('V', 100, V4l2DvTimingsCap)
    ENUM_FREQ_BANDS = _IOWR('V', 101, V4l2FrequencyBand)
    DBG_G_CHIP_INFO = _IOWR('V', 102, V4l2DbgChipInfo)
    QUERY_EXT_CTRL = _IOWR('V', 103, V4l2QueryExtCtrl)
    """

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
from .v4l2formats import V4l2IoctlFmtDesc, V4l2IoctlFrameSizeEnum, \
         V4l2IoctlFrameIvalEnum
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
class V4l2IoctlCapability(ctypes.Structure):
    """An implementation of struct v4l2_capability (linux/videodev.h)

    Describes V4L2 device caps returned by VIDIOC_QUERYCAP

    For the values of :attribute:`capabilities` and :attribute:`device_caps`,
    see :class:`V4l2Capabilities`.

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

    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Name of the driver module (e.g. "bttv").
    driver = None
    #: Name of the card (e.g. "Hauppauge WinTV").
    card = None
    #: Name of the bus (e.g. "PCI" + pci_name(pci_dev) ).
    bus_info = None
    #: The driver version.
    version = None
    #: Capabilities of the physical device as a whole.
    capabilities = None
    #: Capabilities accessed via this particular device (node).
    device_caps = None
    #: Reserved for future extensions.
    reserved = None


###############################################################################
# An abstraction of the capabilities' directives defined in linux/videodev2.h.
# These are the capabilities used in V4l2IoctlCapability.capabilities and
# V4l2IoctlCapability.device_caps.
###############################################################################
class V4l2Capabilities(IntFlag):
    """The v4l2 capability flags.

    These are the flags defining the supported capabilities of a V4l2 devince.

    Example:
        Check if device /dev/video0 supports video capturing::

            vid_dev = VideoDevice(r"/dev/video0")
            if CapabilityFlags.VIDEO_CAPTURE in vid_dev.capabilities:
                start_recording()
    """
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
# An abstraction of enum v4l2_buf_type in linux/videodev2.h.
# These are the buffer types used in V4l2IoctlFmtDesc.type.
###############################################################################
class V4l2BufferType(IntEnum):
    """The v4l2 buffer types.

    Used with :attribute:`enum_fmt`.
    """
    #: Buffer of a single-planar video capture stream, see Video Capture
    #: Interface.
    VIDEO_CAPTURE = 1
    #: Buffer of a single-planar video output stream, see Video Output
    #: Interface.
    VIDEO_OUTPUT = 2
    #: Buffer for video overlay, see Video Overlay Interface.
    VIDEO_OVERLAY = 3
    #: Buffer of a raw VBI capture stream, see Raw VBI Data Interface.
    VBI_CAPTURE = 4
    #: Buffer of a raw VBI output stream, see Raw VBI Data Interface.
    VBI_OUTPUT = 5
    #: Buffer of a sliced VBI capture stream, see Sliced VBI Data Interface.
    SLICED_VBI_CAPTURE = 6
    #: Buffer of a sliced VBI output stream, see Sliced VBI Data Interface.
    SLICED_VBI_OUTPUT = 7
    #: Buffer for video output overlay (OSD), see Video Output Overlay
    #: Interface.
    VIDEO_OUTPUT_OVERLAY = 8
    #: Buffer of a multi-planar video capture stream, see Video Capture
    #: Interface.
    VIDEO_CAPTURE_MPLANE = 9
    #: Buffer of a multi-planar video output stream, see Video Output
    #: Interface.
    VIDEO_OUTPUT_MPLANE = 10
    #: Buffer for Software Defined Radio (SDR) capture stream, see Software
    #: Defined Radio Interface (SDR).
    SDR_CAPTURE = 11
    #: Buffer for Software Defined Radio (SDR) output stream, see Software
    #: Defined Radio Interface (SDR).
    SDR_OUTPUT = 12
    #: Buffer for metadata capture, see Metadata Interface.
    META_CAPTURE = 13
    #: Buffer for metadata output, see Metadata Interface.
    META_OUTPUT = 14


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

    def __call__(self, **kwargs):
        """Runs the ioctl request and returns the buffers."""
        # Create the buffer.
        buff = self._buffer_type()

        # Store user data (for writable ioctls).
        for key, value in kwargs.items():
            # Just to make sure this is a defined field ;)
            # Otherwise, a new attribute which is not part of the c structure
            # will be created, and may cause weird difficult to detect
            # behaviors.
            getattr(buff, key)
            # Now set it.
            setattr(buff, key, value)

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
    see uapi/include/videodev2.h

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

        #######################
        # Add real callables. #
        #######################
        # define VIDIOC_QUERYCAP _IOR('V',  0, struct v4l2_capability)
        obj.query_cap = IoctlAbstraction(device, "QueryCap", IoctlDirection.R,
                                         'V', 0, V4l2IoctlCapability)

        # define VIDIOC_ENUM_FMT _IOWR('V',  2, struct v4l2_fmtdesc)
        obj.enum_fmt = IoctlAbstraction(device, "EnumFmt", IoctlDirection.RW,
                                        'V', 2, V4l2IoctlFmtDesc)

        # define VIDIOC_ENUM_FRAMESIZES _IOWR('V', 74, struct v4l2_frmsizeenum)
        obj.enum_frame_sizes = IoctlAbstraction(device,
                                                "EnumFrameSizes",
                                                IoctlDirection.RW,
                                                'V',
                                                74,
                                                V4l2IoctlFrameSizeEnum)

        # define VIDIOC_ENUM_FRAMEINTERVALS \
        #           _IOWR('V', 75, struct v4l2_frmivalenum)
        obj.enum_frame_intervals = IoctlAbstraction(device,
                                                    "EnumFrameIntervals",
                                                    IoctlDirection.RW,
                                                    'V',
                                                    75,
                                                    V4l2IoctlFrameIvalEnum)
        ###############################
        # End of supported callables. #
        ###############################
        return obj

    ###########################################################################
    # The following are dummy functions for documentation purpose only. The
    # real callables are assigned in __new__.
    ###########################################################################
    def query_cap(self):
        """Interface to the ioctl code VIDIOC_QUERYCAP.
        For more information see struct v4l2_capability in
        uapi/include/videodev2.h.
        """

    def enum_fmt(self, index, type):
        """Interface to the ioctl code VIDIOC_ENUM_FMT.
        For more information see struct v4l2_fmtdesc in
        uapi/include/videodev2.h.
        """

    def enum_frame_sizes(self, index, pixel_format, width, height):
        """Interface to the ioctl code VIDIOC_ENUM_FRAMESIZES.
        For more information see struct v4l2_frmsizeenum in
        uapi/include/videodev2.h.
        """

    def enum_frame_intervals(self, index, pixel_format):
        """Interface to the ioctl code VIDIOC_ENUM_FRAMEINTERVALS.
        For more information see struct v4l2_frmivalenum in
        uapi/include/videodev2.h.
        """

    # TODO: To be implemented.
    """
    G_FMT = _IOWR('V',  4, V4l2IoctlFormat)
    S_FMT = _IOWR('V',  5, V4l2IoctlFormat)
    REQBUFS = _IOWR('V',  8, V4l2IoctlRequestbuffers)
    QUERYBUF = _IOWR('V',  9, V4l2IoctlBuffer)
    G_FBUF = _IOR('V', 10, V4l2IoctlFramebuffer)
    S_FBUF = _IOW('V', 11, V4l2IoctlFramebuffer)
    OVERLAY = _IOW('V', 14, int)
    QBUF = _IOWR('V', 15, V4l2IoctlBuffer)
    EXPBUF = _IOWR('V', 16, V4l2IoctlExportbuffer)
    DQBUF = _IOWR('V', 17, V4l2IoctlBuffer)
    STREAMON = _IOW('V', 18, int)
    STREAMOFF = _IOW('V', 19, int)
    G_PARM = _IOWR('V', 21, V4l2IoctlStreamparm)
    S_PARM = _IOWR('V', 22, V4l2IoctlStreamparm)
    G_STD = _IOR('V', 23, v4l2_std_id)
    S_STD = _IOW('V', 24, v4l2_std_id)
    ENUMSTD = _IOWR('V', 25, V4l2IoctlStandard)
    ENUMINPUT = _IOWR('V', 26, V4l2IoctlInput)
    G_CTRL = _IOWR('V', 27, V4l2IoctlControl)
    S_CTRL = _IOWR('V', 28, V4l2IoctlControl)
    G_TUNER = _IOWR('V', 29, V4l2IoctlTuner)
    S_TUNER = _IOW('V', 30, V4l2IoctlTuner)
    G_AUDIO = _IOR('V', 33, V4l2IoctlAudio)
    S_AUDIO = _IOW('V', 34, V4l2IoctlAudio)
    QUERYCTRL = _IOWR('V', 36, V4l2IoctlQueryctrl)
    QUERYMENU = _IOWR('V', 37, V4l2IoctlQuerymenu)
    G_INPUT = _IOR('V', 38, int)
    S_INPUT = _IOWR('V', 39, int)
    G_EDID = _IOWR('V', 40, V4l2IoctlEdid)
    S_EDID = _IOWR('V', 41, V4l2IoctlEdid)
    G_OUTPUT = _IOR('V', 46, int)
    S_OUTPUT = _IOWR('V', 47, int)
    ENUMOUTPUT = _IOWR('V', 48, V4l2IoctlOutput)
    G_AUDOUT = _IOR('V', 49, V4l2IoctlAudioout)
    S_AUDOUT = _IOW('V', 50, V4l2IoctlAudioout)
    G_MODULATOR = _IOWR('V', 54, V4l2IoctlModulator)
    S_MODULATOR = _IOW('V', 55, V4l2IoctlModulator)
    G_FREQUENCY = _IOWR('V', 56, V4l2IoctlFrequency)
    S_FREQUENCY = _IOW('V', 57, V4l2IoctlFrequency)
    CROPCAP = _IOWR('V', 58, V4l2IoctlCropcap)
    G_CROP = _IOWR('V', 59, V4l2IoctlCrop)
    S_CROP = _IOW('V', 60, V4l2IoctlCrop)
    G_JPEGCOMP = _IOR('V', 61, V4l2IoctlJpegcompression)
    S_JPEGCOMP = _IOW('V', 62, V4l2IoctlJpegcompression)
    QUERYSTD = _IOR('V', 63, v4l2_std_id)
    TRY_FMT = _IOWR('V', 64, V4l2IoctlFormat)
    ENUMAUDIO = _IOWR('V', 65, V4l2IoctlAudio)
    ENUMAUDOUT = _IOWR('V', 66, V4l2IoctlAudioout)
    G_PRIORITY = _IOR('V', 67, __u32)
    S_PRIORITY = _IOW('V', 68, __u32)
    G_SLICED_VBI_CAP = _IOWR('V', 69, V4l2IoctlSlicedVbiCap)
    LOG_STATUS = _IO('V', 70)
    G_EXT_CTRLS = _IOWR('V', 71, V4l2IoctlExtControls)
    S_EXT_CTRLS = _IOWR('V', 72, V4l2IoctlExtControls)
    TRY_EXT_CTRLS = _IOWR('V', 73, V4l2IoctlExtControls)
    G_ENC_INDEX = _IOR('V', 76, V4l2IoctlEncIdx)
    ENCODER_CMD = _IOWR('V', 77, V4l2IoctlEncoderCmd)
    TRY_ENCODER_CMD = _IOWR('V', 78, V4l2IoctlEncoderCmd)
    DBG_S_REGISTER = _IOW('V', 79, V4l2IoctlDbgRegister)
    DBG_G_REGISTER = _IOWR('V', 80, V4l2IoctlDbgRegister)
    S_HW_FREQ_SEEK = _IOW('V', 82, V4l2IoctlHwFreqSeek)
    S_DV_TIMINGS = _IOWR('V', 87, V4l2IoctlDvTimings)
    G_DV_TIMINGS = _IOWR('V', 88, V4l2IoctlDvTimings)
    DQEVENT = _IOR('V', 89, V4l2IoctlEvent)
    SUBSCRIBE_EVENT = _IOW('V', 90, V4l2IoctlEventSubscription)
    UNSUBSCRIBE_EVENT = _IOW('V', 91, V4l2IoctlEventSubscription)
    CREATE_BUFS = _IOWR('V', 92, V4l2IoctlCreateBuffers)
    PREPARE_BUF = _IOWR('V', 93, V4l2IoctlBuffer)
    G_SELECTION = _IOWR('V', 94, V4l2IoctlSelection)
    S_SELECTION = _IOWR('V', 95, V4l2IoctlSelection)
    DECODER_CMD = _IOWR('V', 96, V4l2IoctlDecoderCmd)
    TRY_DECODER_CMD = _IOWR('V', 97, V4l2IoctlDecoderCmd)
    ENUM_DV_TIMINGS = _IOWR('V', 98, V4l2IoctlEnumDvTimings)
    QUERY_DV_TIMINGS = _IOR('V', 99, V4l2IoctlDvTimings)
    DV_TIMINGS_CAP = _IOWR('V', 100, V4l2IoctlDvTimingsCap)
    ENUM_FREQ_BANDS = _IOWR('V', 101, V4l2IoctlFrequencyBand)
    DBG_G_CHIP_INFO = _IOWR('V', 102, V4l2IoctlDbgChipInfo)
    QUERY_EXT_CTRL = _IOWR('V', 103, V4l2IoctlQueryExtCtrl)
    """

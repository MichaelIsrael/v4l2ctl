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
from .v4l2ioctlstructs import V4l2IoctlFmtDesc, \
                              V4l2IoctlFrameSizeEnum, \
                              V4l2IoctlFrameIvalEnum, \
                              V4l2IoctlCropCap, \
                              V4l2IoctlCrop, \
                              V4l2IoctlCapability
from enum import IntEnum
from fcntl import ioctl


###############################################################################
# Exception classes
###############################################################################
class IoctlError(Exception):
    """Raised when ioctl() returns a non-zero value."""
    def __init__(self, device, name, request, return_code, extra_msg=None):
        super().__init__()
        self._info = {"device": device,
                      "name": name,
                      "request": request,
                      "return_code": return_code,
                      }
        self._extra_msg = extra_msg

    def __str__(self):
        msg = ("The ioctl request '{name}' ({request:#X}) on '{device}' "
               "returned '{return_code}'.").format(**self._info)
        if self._extra_msg:
            msg += ": " + self._extra_msg
        return msg


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
        with self._device as dev_fd:
            Timeout = 20
            while Timeout > 0:
                try:
                    ret_code = ioctl(dev_fd, self._code, buff)
                except OSError as e:
                    if "Errno 4" in str(e):
                        pass
                    else:
                        raise IoctlError(self._device.filename,
                                         self._name,
                                         self._code,
                                         -1,
                                         str(e),
                                         ) from None
                else:
                    break
                Timeout -= 1
            else:
                raise IoctlError(self._device.filename,
                                 self._name,
                                 self._code,
                                 -1,
                                 "Call was interrupted 20 times.",
                                 )

        # I couldn't figure out a scenario where ret_code is none zero, because
        # so far an exception is always raised when there is an error with the
        # ioctl call. But the python documentation says the return code will be
        # passed back to python, so anyway, better safe than sorry :)
        if ret_code != 0:
            raise IoctlError(self._device.filename,
                             self._name,
                             self._code,
                             ret_code)

        return buff


###############################################################################
# An abstraction for supported ioctl operations on V4L2 devices.
###############################################################################
class V4l2IocOps(object):
    """Abstraction for ioctl operations on v4l2 devices.
    see LINUX_HEADERS/include/media/v4l2-ioctl.h: struct v4l2_ioctl_ops.
    see uapi/include/videodev2.h

    Keyword Arguments:
        device (str): the video device file.

    :meta private:
    """
    def __init__(self, device, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __new__(cls, device):
        # Create base object.
        obj = super().__new__(cls)

        #######################
        # Add real callables. #
        #######################
        # define VIDIOC_QUERYCAP _IOR('V',  0, struct v4l2_capability)
        obj.query_cap = IoctlAbstraction(device,
                                         "QueryCap",
                                         IoctlDirection.R,
                                         'V',
                                         0,
                                         V4l2IoctlCapability)

        # define VIDIOC_ENUM_FMT _IOWR('V',  2, struct v4l2_fmtdesc)
        obj.enum_fmt = IoctlAbstraction(device,
                                        "EnumFmt",
                                        IoctlDirection.RW,
                                        'V',
                                        2,
                                        V4l2IoctlFmtDesc)

        # define VIDIOC_G_FMT		_IOWR('V',  4, struct v4l2_format)
        obj.get_format = None

        # define VIDIOC_S_FMT		_IOWR('V',  5, struct v4l2_format)
        obj.set_format = None

        # define VIDIOC_TRY_FMT		_IOWR('V', 64, struct v4l2_format)
        obj.try_format = None

        # define VIDIOC_CROPCAP		_IOWR('V', 58, struct v4l2_cropcap)
        obj.crop_cap = IoctlAbstraction(device,
                                        "CropCapabilities",
                                        IoctlDirection.RW,
                                        'V',
                                        58,
                                        V4l2IoctlCropCap)

        # define VIDIOC_G_CROP		_IOWR('V', 59, struct v4l2_crop)
        obj.get_crop = IoctlAbstraction(device,
                                        "GetCropping",
                                        IoctlDirection.RW,
                                        'V',
                                        59,
                                        V4l2IoctlCrop)

        # define VIDIOC_S_CROP		 _IOW('V', 60, struct v4l2_crop)
        obj.set_crop = IoctlAbstraction(device,
                                        "SetCropping",
                                        IoctlDirection.W,
                                        'V',
                                        60,
                                        V4l2IoctlCrop)

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

        Queries the capabilities of a video device.

        For more information see struct v4l2_capability in
        uapi/include/videodev2.h.
        """

    def enum_fmt(self, index, type):
        """Interface to the ioctl code VIDIOC_ENUM_FMT.

        Enumerates the supported formats on a video device.

        Keyword arguments:
            index (int): the format index to read.
            type (V4l2BufferType): the buffer type under inspection.

        For more information see struct v4l2_fmtdesc in
        uapi/include/videodev2.h.
        """

    def crop_cap(self, type):
        """Interface to the ioctl code VIDIOC_CROPCAP.

        Queries the cropping capabilities of a video device.

        Keyword arguments:
            type (V4l2BufferType): the buffer type under inspection.

        For more information see struct v4l2_fmtdesc in
        uapi/include/videodev2.h.
        """

    def get_crop(self, type):
        """Interface to the ioctl code VIDIOC_G_CROP.

        Gets a cropping rectangle.

        Keyword arguments:
            type (V4l2BufferType): the buffer type under inspection.

        For more information see struct v4l2_fmtdesc in
        uapi/include/videodev2.h.
        """

    def set_crop(self, type, c):
        """Interface to the ioctl code VIDIOC_S_CROP.

        Sets a cropping rectangle.

        Keyword arguments:
            type (V4l2BufferType): the buffer type under inspection.
            c (V4l2IoctlRect): the cropping rectangle to set.

        For more information see struct v4l2_fmtdesc in
        uapi/include/videodev2.h.
        """

    def enum_frame_sizes(self, index, pixel_format):
        """Interface to the ioctl code VIDIOC_ENUM_FRAMESIZES.

        Enumerates the supported frame size for a certain format on a video
        device.

        Keyword arguments:
            index (int): the frame size index to read.
            pixel_format (V4l2Formats): the pixel format under inspection.

        For more information see struct v4l2_frmsizeenum in
        uapi/include/videodev2.h.
        """

    def enum_frame_intervals(self, index, pixel_format, width, height):
        """Interface to the ioctl code VIDIOC_ENUM_FRAMEINTERVALS.

        Enumerates the supported frame intervals for a certain format and frame
        size on a video device.

        Keyword arguments:
            index (int): the frame interval index to read.
            pixel_format (V4l2Formats): the pixel format under inspection.
            width (int): the frame width under inspection.
            height (int): the frame height under inspection.

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

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
import ctypes


###############################################################################
# Basic abstractions.
###############################################################################
class V4l2IoctlFract(ctypes.Structure):
    _fields_ = [
        ('numerator', ctypes.c_uint32),
        ('denominator', ctypes.c_uint32),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Numerator.
    numerator = None
    #: Denominator.
    denominator = None


class V4l2IoctlRect(ctypes.Structure):
    """Implementation of struct v4l2_rect from uapi/linux/videodev2.h"""
    _fields_ = [
        ('left', ctypes.c_int32),
        ('top', ctypes.c_int32),
        ('width', ctypes.c_uint32),
        ('height', ctypes.c_uint32),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Left.
    left = None
    #: Top.
    top = None
    #: Width.
    width = None
    #: Height.
    height = None


###############################################################################
# Implementation for struct v4l2_capability from uapi/linux/videodev2.h
###############################################################################
class V4l2IoctlCapability(ctypes.Structure):
    """An implementation of struct v4l2_capability (uapi/linux/videodev.h)

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
# Implementation for struct v4l2_fmtdesc from uapi/linux/videodev2.h
###############################################################################
class V4l2IoctlFmtDesc(ctypes.Structure):
    """An implementation of struct v4l2_fmtdesc (uapi/linux/videodev.h)

    Used to request the supported fomrats on a  V4L2 device (VIDIOC_ENUM_FMT).

    For the values of :attribute:`type`, see :class:`V4l2BufferType`.

    :meta private:
    """
    _fields_ = [
        ('index', ctypes.c_uint32),
        ('type', ctypes.c_uint32),
        ('flags', ctypes.c_uint32),
        ('description', ctypes.c_char * 32),
        ('pixelformat', ctypes.c_uint32),
        ('reserved', ctypes.c_uint32 * 4),
    ]

    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Format number.
    index = None
    #: The buffer subject to this request. see :class:`V4l2BufferType`.
    type = None
    #: see :class:`V4l2FormatDescFlags`.
    flags = None
    #: Description string.
    description = None
    #: Format fourcc. see :class:`V4l2Formats`.
    pixelformat = None
    #: Reserved for future extensions.
    reserved = None


###############################################################################
#                   Frame Size and frame rate enumeration.
###############################################################################

###############################################################################
#
#       F R A M E   S I Z E   E N U M E R A T I O N
#
###############################################################################
class V4l2IoctlFrameSizeDiscrete(ctypes.Structure):
    _fields_ = [
        ('width', ctypes.c_uint32),
        ('height', ctypes.c_uint32),
    ]

    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Frame width [pixel].
    width = None
    #: Frame height [pixel].
    height = None


class V4l2IoctlFrameSizeStepwise(ctypes.Structure):
    _fields_ = [
        ('min_width', ctypes.c_uint32),
        ('max_width', ctypes.c_uint32),
        ('step_width', ctypes.c_uint32),
        ('min_height', ctypes.c_uint32),
        ('max_height', ctypes.c_uint32),
        ('step_height', ctypes.c_uint32),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Minimum frame width [pixel].
    min_width = None
    #: Maximum frame width [pixel].
    max_width = None
    #: Frame width step size [pixel].
    step_width = None
    #: Minimum frame height [pixel].
    min_height = None
    #: Maximum frame height [pixel].
    max_height = None
    #: Frame height step size [pixel].
    step_height = None


# Frame size
class _FrameSizeUnion(ctypes.Union):
    _fields_ = [
        ('discrete', V4l2IoctlFrameSizeDiscrete),
        ('stepwise', V4l2IoctlFrameSizeStepwise),
        ]


class V4l2IoctlFrameSizeEnum(ctypes.Structure):
    _anonymous_ = ("_",)
    _fields_ = [
        ('index', ctypes.c_uint32),
        ('pixel_format', ctypes.c_uint32),
        ('type', ctypes.c_uint32),
        ('_', _FrameSizeUnion),
        ('reserved', ctypes.c_uint32 * 2),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Frame size number.
    index = None
    #: Pixel format.
    pixel_format = None
    #: Frame size type the device supports.
    type = None
    #: Frame size (discrete).
    discrete = None
    #: Frame size (stepwise).
    stepwise = None
    #: Reserved space for future use.
    reserved = None


###############################################################################
#       F R A M E   R A T E   E N U M E R A T I O N
###############################################################################
class V4l2IoctlFrameIvalStepwise(ctypes.Structure):
    _fields_ = [
        ('min', V4l2IoctlFract),
        ('max', V4l2IoctlFract),
        ('step', V4l2IoctlFract),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Minimum frame interval [s].
    min = None
    #: Maximum frame interval [s].
    max = None
    #: Frame interval step size [s].
    step = None


class _FrameIntervalUnion(ctypes.Union):
    _fields_ = [
        ('discrete', V4l2IoctlFract),
        ('stepwise', V4l2IoctlFrameIvalStepwise),
        ]


class V4l2IoctlFrameIvalEnum(ctypes.Structure):
    _anonymous_ = ("_",)
    _fields_ = [
        ('index', ctypes.c_uint32),
        ('pixel_format', ctypes.c_uint32),
        ('width', ctypes.c_uint32),
        ('height', ctypes.c_uint32),
        ('type', ctypes.c_uint32),
        ('_', _FrameIntervalUnion),
        ('reserved', ctypes.c_uint32 * 2),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Frame format index */
    index = None
    #: Pixel format */
    pixel_format = None
    #: Frame width */
    width = None
    #: Frame height */
    height = None
    #: Frame interval type the device supports. */
    type = None
    #: Frame interval (discrete).
    discrete = None
    #: Frame interval (stepwise).
    stepwise = None
    #: Reserved space for future use */
    reserved = None


###############################################################################
#       I N P U T   I M A G E   C R O P P I N G
###############################################################################
# Implementation of struct v4l2_cropcap from uapi/linux/videodev2.h
class V4l2IoctlCropCap(ctypes.Structure):
    _fields_ = [
        ('type', ctypes.c_uint32),
        ('bounds', V4l2IoctlRect),
        ('defrect', V4l2IoctlRect),
        ('pixelaspect', V4l2IoctlFract),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: enum v4l2_buf_type TODO
    type = None
    #: struct v4l2_rect TODO
    bounds = None
    #: struct v4l2_rect TODO
    defrect = None
    #: struct v4l2_rect TODO
    pixelaspect = None


# Implementation of struct v4l2_crop from uapi/linux/videodev2.h
class V4l2IoctlCrop(ctypes.Structure):
    _fields_ = [
        ('type', ctypes.c_uint32),
        ('c', V4l2IoctlRect),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: enum v4l2_buf_type TODO
    type = None
    #: struct v4l2_rect TODO
    c = None

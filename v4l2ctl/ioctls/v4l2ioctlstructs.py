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


class V4l2IoctlClip(ctypes.Structure):
    pass


V4l2IoctlClip._fields_ = [("c", V4l2IoctlRect),
                          ("next", ctypes.POINTER(V4l2IoctlClip)),
                          ]


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


###############################################################################
# 	    V I D E O   I M A G E   F O R M A T
###############################################################################
class V4l2IoctlMetaFormat(ctypes.Structure):
    """Implementation of struct v4l2_meta_format from uapi/linux/videodev2.h"""
    _fields_ = [
        ('dataformat', ctypes.c_uint32),
        ('buffersize', ctypes.c_uint32),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Little endian four character code (fourcc)
    dataformat = None
    #: Maximum size in bytes required for data
    buffersize = None


class V4l2IoctlSdrFormat(ctypes.Structure):
    """Implementation of struct v4l2_sdr_format from uapi/linux/videodev2.h"""
    _fields_ = [
        ('pixelformat', ctypes.c_uint32),
        ('buffersize', ctypes.c_uint32),
        ('reserved', ctypes.c_uint8 * 24),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: TODO
    pixelformat = None
    #: TODO
    buffersize = None
    #: TODO
    reserved = None


class V4l2IoctlSlicedVbiFormat(ctypes.Structure):
    """Implementation of struct v4l2_sliced_vbi_format from
    uapi/linux/videodev2.h
    """
    _fields_ = [
        ('service_set', ctypes.c_uint16),
        ('service_lines', ctypes.c_uint16 * 48),
        ('io_size', ctypes.c_uint32),
        ('reserved', ctypes.c_uint32 * 2),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: TODO
    service_set = None
    #: TODO
    service_lines = None
    #: TODO
    io_size = None
    #: TODO
    reserved = None


class V4l2IoctlVbiFormat(ctypes.Structure):
    """Implementation of struct v4l2_vbi_format from uapi/linux/videodev2.h"""
    _fields_ = [
        ('sampling_rate', ctypes.c_uint32),
        ('offset', ctypes.c_uint32),
        ('samples_per_line', ctypes.c_uint32),
        ('sample_format', ctypes.c_uint32),
        ('start', ctypes.c_int32 * 2),
        ('count', ctypes.c_uint32 * 2),
        ('flags', ctypes.c_uint32),
        ('reserved', ctypes.c_uint32 * 2),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: TODO
    sampling_rate = None
    #: TODO
    offset = None
    #: TODO
    samples_per_line = None
    #: TODO
    sample_format = None
    #: TODO
    start = None
    #: TODO
    count = None
    #: TODO
    flags = None
    #: TODO
    reserved = None


class V4l2IoctlWindow(ctypes.Structure):
    """Implementation of struct v4l2_window from uapi/linux/videodev2.h"""
    _fields_ = [
        ('w', V4l2IoctlRect),
        ('field', ctypes.c_uint32),
        ('chromakey', ctypes.c_uint32),
        ('clips', ctypes.POINTER(V4l2IoctlClip)),
        ('clipcount', ctypes.c_uint32),
        ('global_alpha', ctypes.c_uint8),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: TODO
    w = None
    #: TODO
    field = None
    #: TODO
    chromakey = None
    #: TODO
    clips = None
    #: TODO
    clipcount = None
    #: TODO
    global_alpha = None


class V4l2IoctlPlanePixFormat(ctypes.Structure):
    """Implementation of struct v4l2_plane_pix_format from
    uapi/linux/videodev2.h
    """
    _fields_ = [
        ('sizeimage', ctypes.c_uint32),
        ('bytesperline', ctypes.c_uint32),
        ('reserved', ctypes.c_uint16 * 6),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: TODO
    sizeimage = None
    #: TODO
    bytesperline = None
    #: TODO
    reserved = None


class _PixFormatMplaneUnion(ctypes.Union):
    """Implementation of the union inside the struct v4l2_pix_format_mplane from
    uapi/linux/videodev2.h
    """
    _fields_ = [
        ('ycbcr_enc', ctypes.c_uint8),
        ('hsv_enc', ctypes.c_uint8),
        ]


class V4l2IoctlPixFormatMplane(ctypes.Structure):
    """Implementation of struct v4l2_pix_format_mplane from
    uapi/linux/videodev2.h
    """
    _anonymous_ = ('_', )
    _fields_ = [
        ('width', ctypes.c_uint32),
        ('height', ctypes.c_uint32),
        ('pixelformat', ctypes.c_uint32),
        ('field', ctypes.c_uint32),
        ('colorspace', ctypes.c_uint32),
        ('plane_fmt', V4l2IoctlPlanePixFormat * 8),
        ('num_planes', ctypes.c_uint8),
        ('flags', ctypes.c_uint8),
        ('_', _PixFormatMplaneUnion),
        ('quantization', ctypes.c_uint8),
        ('xfer_func', ctypes.c_uint8),
        ('reserved', ctypes.c_uint8 * 7),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: TODO
    width = None
    #: TODO
    height = None
    #: TODO
    pixelformat = None
    #: TODO
    field = None
    #: TODO
    colorspace = None
    #: TODO
    plane_fmt = None
    #: TODO
    num_planes = None
    #: TODO
    flags = None
    #: TODO
    ycbcr_enc = None
    #: TODO
    hsv_enc = None
    #: TODO
    quantization = None
    #: TODO
    xfer_func = None
    #: TODO
    reserved = None


class _PixFormatUnion(ctypes.Union):
    """Implementation of the union inside the struct v4l2_pix_format from
    uapi/linux/videodev2.h
    """
    _fields_ = [
        ('ycbcr_enc', ctypes.c_uint32),
        ('hsv_enc', ctypes.c_uint32),
        ]


class V4l2IoctlPixFormat(ctypes.Structure):
    """Implementation of struct v4l2_pix_format from uapi/linux/videodev2.h"""
    _anonymous_ = ('_', )
    _fields_ = [
        ('width', ctypes.c_uint32),
        ('height', ctypes.c_uint32),
        ('pixelformat', ctypes.c_uint32),
        ('field', ctypes.c_uint32),
        ('bytesperline', ctypes.c_uint32),
        ('sizeimage', ctypes.c_uint32),
        ('colorspace', ctypes.c_uint32),
        ('priv', ctypes.c_uint32),
        ('flags', ctypes.c_uint32),
        ('_', _PixFormatUnion),
        ('quantization', ctypes.c_uint32),
        ('xfer_func', ctypes.c_uint32),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Image width in pixels.
    width = None
    #: Image height in pixels. If field is one of :py:attr:`V4l2Field.TOP`,
    #: :py:attr:`V4l2Field.BOTTOM` or :py:attr:`V4l2Field.ALTERNATE` then
    #: height refers to the number of lines in the field, otherwise it refers
    #: to the number of lines in the frame (which is twice the field height for
    #: interlaced formats).
    height = None
    #: The pixel format or type of compression, set by the application. see
    #: :py:class:`V4l2Formats`
    pixelformat = None
    #: TODO
    field = None
    #: Distance in bytes between the leftmost pixels in two adjacent lines.
    bytesperline = None
    #: TODO
    sizeimage = None
    #: Image colorspace, from :py:class:`V4l2ColorSpace`. This information
    #: supplements the :py:attr:`pixelformat` and must be set by the driver for
    #: capture streams and by the application for output streams.
    colorspace = None
    #: This field indicates whether the remaining fields, also called the
    #: extended fields, are valid. When set to
    #: :py:attr:`V4l2PixFormat.PRIV_MAGIC`, it indicates that the extended
    #: fields have been correctly initialized. When set to any other value it
    #: indicates that the extended fields contain undefined values.
    #: Applications that wish to use the pixel format extended fields must
    #: first ensure that the feature is supported by querying the device for
    #: the :py:attr:`V4l2Capabilities.EXT_PIX_FORMAT` capability. If the
    #: capability isn’t set the pixel format extended fields are not supported
    #: and using the extended fields will lead to undefined results.
    priv = None
    #: TODO
    flags = None
    #: TODO
    ycbcr_enc = None
    #: TODO
    hsv_enc = None
    #: TODO
    quantization = None
    #: TODO
    xfer_func = None


class V4l2IoctlFormatUnion(ctypes.Union):
    """Implementation of the union inside the struct v4l2_format from
    uapi/linux/videodev2.h
    """
    _fields_ = [
        ('pix', V4l2IoctlPixFormat),
        ('pix_mp', V4l2IoctlPixFormatMplane),
        ('win', V4l2IoctlWindow),
        ('vbi', V4l2IoctlVbiFormat),
        ('sliced', V4l2IoctlSlicedVbiFormat),
        ('sdr', V4l2IoctlSdrFormat),
        ('meta', V4l2IoctlMetaFormat),
        ('raw_data', ctypes.c_uint8 * 200),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Definition of an image format.
    #: For buffer type :py:attr:`V4l2BufferType.VIDEO_CAPTURE`.
    pix = None
    #: Definition of a multiplanar image format.
    #: For buffer type :py:attr:`V4l2BufferType.VIDEO_CAPTURE_MPLANE`.
    pix_mp = None
    #: Definition of an overlaid image.
    #: For buffer type :py:attr:`V4l2BufferType.VIDEO_OVERLAY`.
    win = None
    #: Raw VBI capture or output parameters.
    #: For buffer type :py:attr:`V4l2BufferType.VBI_CAPTURE`.
    vbi = None
    #: Sliced VBI capture or output parameters.
    #: For buffer type :py:attr:`V4l2BufferType.SLICED_VBI_CAPTURE`.
    sliced = None
    #: Definition of a data format used by SDR capture and output devices.
    #: For buffer type :py:attr:`V4l2BufferType.SDR_CAPTURE`.
    sdr = None
    #: Definition of a metadata format used by metadata capture devices.
    #: For buffer type :py:attr:`V4l2BufferType.META_CAPTURE`.
    meta = None
    #: Placeholder for future extensions and custom formats
    raw_data = None


class V4l2IoctlFormat(ctypes.Structure):
    """Implementation of struct v4l2_format from uapi/linux/videodev2.h"""
    _fields_ = [
        ('type', ctypes.c_uint32),
        ('fmt', V4l2IoctlFormatUnion),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: Type of the data stream (see :class:`V4l2BufferType`).
    type = None
    #: Union of different image format structures depending on the used
    #: :py:attr:`V4l2IoctlFormat.type`.
    fmt = None


###############################################################################
# 	M E M O R Y - M A P P I N G   B U F F E R S
###############################################################################
class V4l2IoctlRequestbuffers(ctypes.Structure):
    """Implementation of struct v4l2_requestbuffers from uapi/linux/videodev2.h
    """
    _fields_ = [
        ('count', ctypes.c_uint32),
        ('type', ctypes.c_uint32),
        ('memory', ctypes.c_uint32),
        ('capabilities', ctypes.c_uint32),
        ('reserved', ctypes.c_uint32 * 1),
        ]
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################
    #: TODO
    count = None
    #: TODO
    type = None
    #: TODO
    memory = None
    #: TODO
    capabilities = None
    #: TODO
    reserved = None

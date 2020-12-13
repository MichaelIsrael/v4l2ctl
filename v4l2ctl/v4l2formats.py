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
from enum import IntEnum, IntFlag
import ctypes


###############################################################################
# Four-character-code (FOURCC).
###############################################################################
def v4l2_fourcc(a, b, c, d):
    return ((ord(a) & 0xFF) |
            ((ord(b) & 0xFF) << 8) |
            ((ord(c) & 0xFF) << 16) |
            ((ord(d) & 0xFF) << 24))


def v4l2_fourcc_be(a, b, c, d):
    return (v4l2_fourcc(a, b, c, d) | (1 << 31))


###############################################################################
# An abstrction for struct v4l2_fmtdesc from linux/videodev2.h
###############################################################################
class V4l2IoctlFmtDesc(ctypes.Structure):
    """An implementation of struct v4l2_fmtdesc (linux/videodev.h)

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


class V4l2Formats(IntEnum):
    """An enumeration of all supported formats."""
    #: 8  RGB-3-3-2
    PIX_FMT_RGB332 = v4l2_fourcc('R', 'G', 'B', '1')
    #: 16  xxxxrrrr g
    PIX_FMT_RGB444 = v4l2_fourcc('R', '4', '4', '4')
    #: 16  aaaarrrr g
    PIX_FMT_ARGB444 = v4l2_fourcc('A', 'R', '1', '2')
    #: 16  xxxxrrrr g
    PIX_FMT_XRGB444 = v4l2_fourcc('X', 'R', '1', '2')
    #: 16  rrrrgggg b
    PIX_FMT_RGBA444 = v4l2_fourcc('R', 'A', '1', '2')
    #: 16  rrrrgggg b
    PIX_FMT_RGBX444 = v4l2_fourcc('R', 'X', '1', '2')
    #: 16  aaaabbbb g
    PIX_FMT_ABGR444 = v4l2_fourcc('A', 'B', '1', '2')
    #: 16  xxxxbbbb g
    PIX_FMT_XBGR444 = v4l2_fourcc('X', 'B', '1', '2')

    #########################################################################
    # Originally this had 'BA12' as fourcc, but this clashed with the older #
    # V4L2_PIX_FMT_SGRBG12 which inexplicably used that same fourcc.        #
    # So use 'GA12' instead for V4L2_PIX_FMT_BGRA444.                       #
    #########################################################################
    #: 16  bbbbgggg r
    PIX_FMT_BGRA444 = v4l2_fourcc('G', 'A', '1', '2')
    #: 16  bbbbgggg r
    PIX_FMT_BGRX444 = v4l2_fourcc('B', 'X', '1', '2')
    #: 16  RGB-5-5-5
    PIX_FMT_RGB555 = v4l2_fourcc('R', 'G', 'B', 'O')
    #: 16  ARGB-1-5-5-5
    PIX_FMT_ARGB555 = v4l2_fourcc('A', 'R', '1', '5')
    #: 16  XRGB-1-5-5-5
    PIX_FMT_XRGB555 = v4l2_fourcc('X', 'R', '1', '5')
    #: 16  RGBA-5-5-5-1
    PIX_FMT_RGBA555 = v4l2_fourcc('R', 'A', '1', '5')
    #: 16  RGBX-5-5-5-1
    PIX_FMT_RGBX555 = v4l2_fourcc('R', 'X', '1', '5')
    #: 16  ABGR-1-5-5-5
    PIX_FMT_ABGR555 = v4l2_fourcc('A', 'B', '1', '5')
    #: 16  XBGR-1-5-5-5
    PIX_FMT_XBGR555 = v4l2_fourcc('X', 'B', '1', '5')
    #: 16  BGRA-5-5-5-1
    PIX_FMT_BGRA555 = v4l2_fourcc('B', 'A', '1', '5')
    #: 16  BGRX-5-5-5-1
    PIX_FMT_BGRX555 = v4l2_fourcc('B', 'X', '1', '5')
    #: 16  RGB-5-6-5
    PIX_FMT_RGB565 = v4l2_fourcc('R', 'G', 'B', 'P')
    #: 16  RGB-5-5-5 B
    PIX_FMT_RGB555X = v4l2_fourcc('R', 'G', 'B', 'Q')
    #: 16  ARGB-5-5-5 B
    PIX_FMT_ARGB555X = v4l2_fourcc_be('A', 'R', '1', '5')
    #: 16  XRGB-5-5-5 B
    PIX_FMT_XRGB555X = v4l2_fourcc_be('X', 'R', '1', '5')
    #: 16  RGB-5-6-5 B
    PIX_FMT_RGB565X = v4l2_fourcc('R', 'G', 'B', 'R')
    #: 18  BGR-6-6-6
    PIX_FMT_BGR666 = v4l2_fourcc('B', 'G', 'R', 'H')
    #: 24  BGR-8-8-8
    PIX_FMT_BGR24 = v4l2_fourcc('B', 'G', 'R', '3')
    #: 24  RGB-8-8-8
    PIX_FMT_RGB24 = v4l2_fourcc('R', 'G', 'B', '3')
    #: 32  BGR-8-8-8-8
    PIX_FMT_BGR32 = v4l2_fourcc('B', 'G', 'R', '4')
    #: 32  BGRA-8-8-8-8
    PIX_FMT_ABGR32 = v4l2_fourcc('A', 'R', '2', '4')
    #: 32  BGRX-8-8-8-8
    PIX_FMT_XBGR32 = v4l2_fourcc('X', 'R', '2', '4')
    #: 32  ABGR-8-8-8-8
    PIX_FMT_BGRA32 = v4l2_fourcc('R', 'A', '2', '4')
    #: 32  XBGR-8-8-8-8
    PIX_FMT_BGRX32 = v4l2_fourcc('R', 'X', '2', '4')
    #: 32  RGB-8-8-8-8
    PIX_FMT_RGB32 = v4l2_fourcc('R', 'G', 'B', '4')
    #: 32  RGBA-8-8-8-8
    PIX_FMT_RGBA32 = v4l2_fourcc('A', 'B', '2', '4')
    #: 32  RGBX-8-8-8-8
    PIX_FMT_RGBX32 = v4l2_fourcc('X', 'B', '2', '4')
    #: 32  ARGB-8-8-8-8
    PIX_FMT_ARGB32 = v4l2_fourcc('B', 'A', '2', '4')
    #: 32  XRGB-8-8-8-8
    PIX_FMT_XRGB32 = v4l2_fourcc('B', 'X', '2', '4')

    #################
    # Grey formats. #
    #################
    #: 8  G
    PIX_FMT_GREY = v4l2_fourcc('G', 'R', 'E', 'Y')
    #: 4  G
    PIX_FMT_Y4 = v4l2_fourcc('Y', '0', '4', ' ')
    #: 6  G
    PIX_FMT_Y6 = v4l2_fourcc('Y', '0', '6', ' ')
    #: 10  G
    PIX_FMT_Y10 = v4l2_fourcc('Y', '1', '0', ' ')
    #: 12  G
    PIX_FMT_Y12 = v4l2_fourcc('Y', '1', '2', ' ')
    #: 16  G
    PIX_FMT_Y16 = v4l2_fourcc('Y', '1', '6', ' ')
    #: 16  Greyscale B
    PIX_FMT_Y16_BE = v4l2_fourcc_be('Y', '1', '6', ' ')

    ############################
    # Grey bit-packed formats. #
    ############################
    #: 10  Greyscale bit-p
    PIX_FMT_Y10BPACK = v4l2_fourcc('Y', '1', '0', 'B')
    #: 10  Greyscale, MIPI RAW10 p
    PIX_FMT_Y10P = v4l2_fourcc('Y', '1', '0', 'P')

    ####################
    # Palette formats. #
    ####################
    #: 8  8-bit p
    PIX_FMT_PAL8 = v4l2_fourcc('P', 'A', 'L', '8')

    ########################
    # Chrominance formats. #
    ########################
    #: 8  UV 4:4
    PIX_FMT_UV8 = v4l2_fourcc('U', 'V', '8', ' ')

    ##################################
    # Luminance+Chrominance formats. #
    ##################################
    #: 16  YUV 4:2:2
    PIX_FMT_YUYV = v4l2_fourcc('Y', 'U', 'Y', 'V')
    #: 16  YUV 4:2:2
    PIX_FMT_YYUV = v4l2_fourcc('Y', 'Y', 'U', 'V')
    #: 16 YVU 4:2:2
    PIX_FMT_YVYU = v4l2_fourcc('Y', 'V', 'Y', 'U')
    #: 16  YUV 4:2:2
    PIX_FMT_UYVY = v4l2_fourcc('U', 'Y', 'V', 'Y')
    #: 16  YUV 4:2:2
    PIX_FMT_VYUY = v4l2_fourcc('V', 'Y', 'U', 'Y')
    #: 12  YUV 4:1:1
    PIX_FMT_Y41P = v4l2_fourcc('Y', '4', '1', 'P')
    #: 16  xxxxyyyy u
    PIX_FMT_YUV444 = v4l2_fourcc('Y', '4', '4', '4')
    #: 16  YUV-5-5-5
    PIX_FMT_YUV555 = v4l2_fourcc('Y', 'U', 'V', 'O')
    #: 16  YUV-5-6-5
    PIX_FMT_YUV565 = v4l2_fourcc('Y', 'U', 'V', 'P')
    #: 32  YUV-8-8-8-8
    PIX_FMT_YUV32 = v4l2_fourcc('Y', 'U', 'V', '4')
    #: 32  AYUV-8-8-8-8
    PIX_FMT_AYUV32 = v4l2_fourcc('A', 'Y', 'U', 'V')
    #: 32  XYUV-8-8-8-8
    PIX_FMT_XYUV32 = v4l2_fourcc('X', 'Y', 'U', 'V')
    #: 32  VUYA-8-8-8-8
    PIX_FMT_VUYA32 = v4l2_fourcc('V', 'U', 'Y', 'A')
    #: 32  VUYX-8-8-8-8
    PIX_FMT_VUYX32 = v4l2_fourcc('V', 'U', 'Y', 'X')
    #: 8  8-bit c
    PIX_FMT_HI240 = v4l2_fourcc('H', 'I', '2', '4')
    #: 8  YUV 4:2:0 16x16 m
    PIX_FMT_HM12 = v4l2_fourcc('H', 'M', '1', '2')
    #: 12  YUV 4:2:0 2 lines y, 1 line uv i
    PIX_FMT_M420 = v4l2_fourcc('M', '4', '2', '0')

    #################################################
    # two planes -- one Y, one Cr + Cb interleaved. #
    #################################################
    #: 12  Y/CbCr 4:2:0
    PIX_FMT_NV12 = v4l2_fourcc('N', 'V', '1', '2')
    #: 12  Y/CrCb 4:2:0
    PIX_FMT_NV21 = v4l2_fourcc('N', 'V', '2', '1')
    #: 16  Y/CbCr 4:2:2
    PIX_FMT_NV16 = v4l2_fourcc('N', 'V', '1', '6')
    #: 16  Y/CrCb 4:2:2
    PIX_FMT_NV61 = v4l2_fourcc('N', 'V', '6', '1')
    #: 24  Y/CbCr 4:4:4
    PIX_FMT_NV24 = v4l2_fourcc('N', 'V', '2', '4')
    #: 24  Y/CrCb 4:4:4
    PIX_FMT_NV42 = v4l2_fourcc('N', 'V', '4', '2')

    ###############################################################
    # two non contiguous planes - one Y, one Cr + Cb interleaved. #
    ###############################################################
    #: 12  Y/CbCr 4:2:0
    PIX_FMT_NV12M = v4l2_fourcc('N', 'M', '1', '2')
    #: 21  Y/CrCb 4:2:0
    PIX_FMT_NV21M = v4l2_fourcc('N', 'M', '2', '1')
    #: 16  Y/CbCr 4:2:2
    PIX_FMT_NV16M = v4l2_fourcc('N', 'M', '1', '6')
    #: 16  Y/CrCb 4:2:2
    PIX_FMT_NV61M = v4l2_fourcc('N', 'M', '6', '1')
    #: 12  Y/CbCr 4:2:0 64x32 m
    PIX_FMT_NV12MT = v4l2_fourcc('T', 'M', '1', '2')
    #: 12  Y/CbCr 4:2:0 16x16 m
    PIX_FMT_NV12MT_16X16 = v4l2_fourcc('V', 'M', '1', '2')

    ############################
    # three planes - Y Cb, Cr. #
    ############################
    #: 9  YUV 4:1:0
    PIX_FMT_YUV410 = v4l2_fourcc('Y', 'U', 'V', '9')
    #: 9  YVU 4:1:0
    PIX_FMT_YVU410 = v4l2_fourcc('Y', 'V', 'U', '9')
    #: 12  YVU411 p
    PIX_FMT_YUV411P = v4l2_fourcc('4', '1', '1', 'P')
    #: 12  YUV 4:2:0
    PIX_FMT_YUV420 = v4l2_fourcc('Y', 'U', '1', '2')
    #: 12  YVU 4:2:0
    PIX_FMT_YVU420 = v4l2_fourcc('Y', 'V', '1', '2')
    #: 16  YVU422 p
    PIX_FMT_YUV422P = v4l2_fourcc('4', '2', '2', 'P')

    ############################################
    # three non contiguous planes - Y, Cb, Cr. #
    ############################################
    #: 12  YUV420 p
    PIX_FMT_YUV420M = v4l2_fourcc('Y', 'M', '1', '2')
    #: 12  YVU420 p
    PIX_FMT_YVU420M = v4l2_fourcc('Y', 'M', '2', '1')
    #: 16  YUV422 p
    PIX_FMT_YUV422M = v4l2_fourcc('Y', 'M', '1', '6')
    #: 16  YVU422 p
    PIX_FMT_YVU422M = v4l2_fourcc('Y', 'M', '6', '1')
    #: 24  YUV444 p
    PIX_FMT_YUV444M = v4l2_fourcc('Y', 'M', '2', '4')
    #: 24  YVU444 p
    PIX_FMT_YVU444M = v4l2_fourcc('Y', 'M', '4', '2')

    ######################################################################
    # Bayer formats - see http://www.siliconimaging.com/RGB%20Bayer.htm. #
    ######################################################################
    #: 8  BGBG.. GRGR.
    PIX_FMT_SBGGR8 = v4l2_fourcc('B', 'A', '8', '1')
    #: 8  GBGB.. RGRG.
    PIX_FMT_SGBRG8 = v4l2_fourcc('G', 'B', 'R', 'G')
    #: 8  GRGR.. BGBG.
    PIX_FMT_SGRBG8 = v4l2_fourcc('G', 'R', 'B', 'G')
    #: 8  RGRG.. GBGB.
    PIX_FMT_SRGGB8 = v4l2_fourcc('R', 'G', 'G', 'B')
    #: 10  BGBG.. GRGR.
    PIX_FMT_SBGGR10 = v4l2_fourcc('B', 'G', '1', '0')
    #: 10  GBGB.. RGRG.
    PIX_FMT_SGBRG10 = v4l2_fourcc('G', 'B', '1', '0')
    #: 10  GRGR.. BGBG.
    PIX_FMT_SGRBG10 = v4l2_fourcc('B', 'A', '1', '0')
    #: 10  RGRG.. GBGB.
    PIX_FMT_SRGGB10 = v4l2_fourcc('R', 'G', '1', '0')
    #######################################################
    # 10bit raw bayer packed, 5 bytes for every 4 pixels. #
    #######################################################
    PIX_FMT_SBGGR10P = v4l2_fourcc('p', 'B', 'A', 'A')
    PIX_FMT_SGBRG10P = v4l2_fourcc('p', 'G', 'A', 'A')
    PIX_FMT_SGRBG10P = v4l2_fourcc('p', 'g', 'A', 'A')
    PIX_FMT_SRGGB10P = v4l2_fourcc('p', 'R', 'A', 'A')
    ###############################################
    # 10bit raw bayer a-law compressed to 8 bits. #
    ###############################################
    PIX_FMT_SBGGR10ALAW8 = v4l2_fourcc('a', 'B', 'A', '8')
    PIX_FMT_SGBRG10ALAW8 = v4l2_fourcc('a', 'G', 'A', '8')
    PIX_FMT_SGRBG10ALAW8 = v4l2_fourcc('a', 'g', 'A', '8')
    PIX_FMT_SRGGB10ALAW8 = v4l2_fourcc('a', 'R', 'A', '8')
    ##############################################
    # 10bit raw bayer DPCM compressed to 8 bits. #
    ##############################################
    PIX_FMT_SBGGR10DPCM8 = v4l2_fourcc('b', 'B', 'A', '8')
    PIX_FMT_SGBRG10DPCM8 = v4l2_fourcc('b', 'G', 'A', '8')
    PIX_FMT_SGRBG10DPCM8 = v4l2_fourcc('B', 'D', '1', '0')
    PIX_FMT_SRGGB10DPCM8 = v4l2_fourcc('b', 'R', 'A', '8')
    #: 12  BGBG.. GRGR.
    PIX_FMT_SBGGR12 = v4l2_fourcc('B', 'G', '1', '2')
    #: 12  GBGB.. RGRG.
    PIX_FMT_SGBRG12 = v4l2_fourcc('G', 'B', '1', '2')
    #: 12  GRGR.. BGBG.
    PIX_FMT_SGRBG12 = v4l2_fourcc('B', 'A', '1', '2')
    #: 12  RGRG.. GBGB.
    PIX_FMT_SRGGB12 = v4l2_fourcc('R', 'G', '1', '2')
    #######################################################
    # 12bit raw bayer packed, 6 bytes for every 4 pixels. #
    #######################################################
    PIX_FMT_SBGGR12P = v4l2_fourcc('p', 'B', 'C', 'C')
    PIX_FMT_SGBRG12P = v4l2_fourcc('p', 'G', 'C', 'C')
    PIX_FMT_SGRBG12P = v4l2_fourcc('p', 'g', 'C', 'C')
    PIX_FMT_SRGGB12P = v4l2_fourcc('p', 'R', 'C', 'C')
    #######################################################
    # 14bit raw bayer packed, 7 bytes for every 4 pixels. #
    #######################################################
    PIX_FMT_SBGGR14P = v4l2_fourcc('p', 'B', 'E', 'E')
    PIX_FMT_SGBRG14P = v4l2_fourcc('p', 'G', 'E', 'E')
    PIX_FMT_SGRBG14P = v4l2_fourcc('p', 'g', 'E', 'E')
    PIX_FMT_SRGGB14P = v4l2_fourcc('p', 'R', 'E', 'E')
    #: 16  BGBG.. GRGR.
    PIX_FMT_SBGGR16 = v4l2_fourcc('B', 'Y', 'R', '2')
    #: 16  GBGB.. RGRG.
    PIX_FMT_SGBRG16 = v4l2_fourcc('G', 'B', '1', '6')
    #: 16  GRGR.. BGBG.
    PIX_FMT_SGRBG16 = v4l2_fourcc('G', 'R', '1', '6')
    #: 16  RGRG.. GBGB.
    PIX_FMT_SRGGB16 = v4l2_fourcc('R', 'G', '1', '6')

    ################
    # HSV formats. #
    ################
    PIX_FMT_HSV24 = v4l2_fourcc('H', 'S', 'V', '3')
    PIX_FMT_HSV32 = v4l2_fourcc('H', 'S', 'V', '4')

    #######################
    # compressed formats. #
    #######################
    #: Motion-J
    PIX_FMT_MJPEG = v4l2_fourcc('M', 'J', 'P', 'G')
    #: JFIF J
    PIX_FMT_JPEG = v4l2_fourcc('J', 'P', 'E', 'G')
    #: 1
    PIX_FMT_DV = v4l2_fourcc('d', 'v', 's', 'd')
    #: MPEG-1/2/4 M
    PIX_FMT_MPEG = v4l2_fourcc('M', 'P', 'E', 'G')
    #: H264 with start c
    PIX_FMT_H264 = v4l2_fourcc('H', '2', '6', '4')
    #: H264 without start c
    PIX_FMT_H264_NO_SC = v4l2_fourcc('A', 'V', 'C', '1')
    #: H264 M
    PIX_FMT_H264_MVC = v4l2_fourcc('M', '2', '6', '4')
    #: H
    PIX_FMT_H263 = v4l2_fourcc('H', '2', '6', '3')
    #: MPEG-1 E
    PIX_FMT_MPEG1 = v4l2_fourcc('M', 'P', 'G', '1')
    #: MPEG-2 E
    PIX_FMT_MPEG2 = v4l2_fourcc('M', 'P', 'G', '2')
    #: MPEG-2 parsed slice d
    PIX_FMT_MPEG2_SLICE = v4l2_fourcc('M', 'G', '2', 'S')
    #: MPEG-4 part 2 E
    PIX_FMT_MPEG4 = v4l2_fourcc('M', 'P', 'G', '4')
    #: X
    PIX_FMT_XVID = v4l2_fourcc('X', 'V', 'I', 'D')
    #: SMPTE 421M Annex G compliant s
    PIX_FMT_VC1_ANNEX_G = v4l2_fourcc('V', 'C', '1', 'G')
    #: SMPTE 421M Annex L compliant s
    PIX_FMT_VC1_ANNEX_L = v4l2_fourcc('V', 'C', '1', 'L')
    #: V
    PIX_FMT_VP8 = v4l2_fourcc('V', 'P', '8', '0')
    #: V
    PIX_FMT_VP9 = v4l2_fourcc('V', 'P', '9', '0')
    #: HEVC aka H.2
    PIX_FMT_HEVC = v4l2_fourcc('H', 'E', 'V', 'C')
    #: Fast Walsh Hadamard Transform (vicodec)
    PIX_FMT_FWHT = v4l2_fourcc('F', 'W', 'H', 'T')
    #: Stateless FWHT (vicodec)
    PIX_FMT_FWHT_STATELESS = v4l2_fourcc('S', 'F', 'W', 'H')

    #############################
    #  Vendor-specific formats. #
    #############################
    #: cpia1 Y
    PIX_FMT_CPIA1 = v4l2_fourcc('C', 'P', 'I', 'A')
    #: Winnov hw c
    PIX_FMT_WNVA = v4l2_fourcc('W', 'N', 'V', 'A')
    #: SN9C10x c
    PIX_FMT_SN9C10X = v4l2_fourcc('S', '9', '1', '0')
    #: SN9C20x YUV 4:2:0
    PIX_FMT_SN9C20X_I420 = v4l2_fourcc('S', '9', '2', '0')
    #: pwc older w
    PIX_FMT_PWC1 = v4l2_fourcc('P', 'W', 'C', '1')
    #: pwc newer w
    PIX_FMT_PWC2 = v4l2_fourcc('P', 'W', 'C', '2')
    #: ET61X251 c
    PIX_FMT_ET61X251 = v4l2_fourcc('E', '6', '2', '5')
    #: YUYV per l
    PIX_FMT_SPCA501 = v4l2_fourcc('S', '5', '0', '1')
    #: YYUV per l
    PIX_FMT_SPCA505 = v4l2_fourcc('S', '5', '0', '5')
    #: YUVY per l
    PIX_FMT_SPCA508 = v4l2_fourcc('S', '5', '0', '8')
    #: compressed GBRG b
    PIX_FMT_SPCA561 = v4l2_fourcc('S', '5', '6', '1')
    #: compressed BGGR b
    PIX_FMT_PAC207 = v4l2_fourcc('P', '2', '0', '7')
    #: compressed BGGR b
    PIX_FMT_MR97310A = v4l2_fourcc('M', '3', '1', '0')
    #: compressed RGGB b
    PIX_FMT_JL2005BCD = v4l2_fourcc('J', 'L', '2', '0')
    #: compressed GBRG b
    PIX_FMT_SN9C2028 = v4l2_fourcc('S', 'O', 'N', 'X')
    #: compressed RGGB b
    PIX_FMT_SQ905C = v4l2_fourcc('9', '0', '5', 'C')
    #: Pixart 73xx J
    PIX_FMT_PJPG = v4l2_fourcc('P', 'J', 'P', 'G')
    #: ov511 J
    PIX_FMT_OV511 = v4l2_fourcc('O', '5', '1', '1')
    #: ov518 J
    PIX_FMT_OV518 = v4l2_fourcc('O', '5', '1', '8')
    #: stv0680 b
    PIX_FMT_STV0680 = v4l2_fourcc('S', '6', '8', '0')
    #: tm5600/t
    PIX_FMT_TM6000 = v4l2_fourcc('T', 'M', '6', '0')
    #: one line of Y then 1 line of V
    PIX_FMT_CIT_YYVYUY = v4l2_fourcc('C', 'I', 'T', 'V')
    #: YUV420 planar in blocks of 256 p
    PIX_FMT_KONICA420 = v4l2_fourcc('K', 'O', 'N', 'I')
    #: JPEG-L
    PIX_FMT_JPGL = v4l2_fourcc('J', 'P', 'G', 'L')
    #: se401 janggu compressed r
    PIX_FMT_SE401 = v4l2_fourcc('S', '4', '0', '1')
    #: S5C73M3 interleaved UYVY/J
    PIX_FMT_S5C_UYVY_JPG = v4l2_fourcc('S', '5', 'C', 'I')
    #: Greyscale 8-bit L/R i
    PIX_FMT_Y8I = v4l2_fourcc('Y', '8', 'I', ' ')
    #: Greyscale 12-bit L/R i
    PIX_FMT_Y12I = v4l2_fourcc('Y', '1', '2', 'I')
    #: Depth data 16-b
    PIX_FMT_Z16 = v4l2_fourcc('Z', '1', '6', ' ')
    #: Mediatek compressed block m
    PIX_FMT_MT21C = v4l2_fourcc('M', 'T', '2', '1')
    #: Intel Planar Greyscale 10-bit and Depth 16-b
    PIX_FMT_INZI = v4l2_fourcc('I', 'N', 'Z', 'I')
    #: Sunxi Tiled NV12 F
    PIX_FMT_SUNXI_TILED_NV12 = v4l2_fourcc('S', 'T', '1', '2')
    #: Intel 4-bit packed depth confidence i
    PIX_FMT_CNF4 = v4l2_fourcc('C', 'N', 'F', '4')

    #########################################################################
    # 10bit raw bayer packed, 32 bytes for every 25 pixels, last LSB 6 bits #
    # unused.                                                               #
    #########################################################################
    #: IPU3 packed 10-bit BGGR b
    PIX_FMT_IPU3_SBGGR10 = v4l2_fourcc('i', 'p', '3', 'b')
    #: IPU3 packed 10-bit GBRG b
    PIX_FMT_IPU3_SGBRG10 = v4l2_fourcc('i', 'p', '3', 'g')
    #: IPU3 packed 10-bit GRBG b
    PIX_FMT_IPU3_SGRBG10 = v4l2_fourcc('i', 'p', '3', 'G')
    #: IPU3 packed 10-bit RGGB b
    PIX_FMT_IPU3_SRGGB10 = v4l2_fourcc('i', 'p', '3', 'r')

    ###############################################################
    # SDR formats - used only for Software Defined Radio devices. #
    ###############################################################
    #: IQ u
    SDR_FMT_CU8 = v4l2_fourcc('C', 'U', '0', '8')
    #: IQ u
    SDR_FMT_CU16LE = v4l2_fourcc('C', 'U', '1', '6')
    #: complex s
    SDR_FMT_CS8 = v4l2_fourcc('C', 'S', '0', '8')
    #: complex s
    SDR_FMT_CS14LE = v4l2_fourcc('C', 'S', '1', '4')
    #: real u
    SDR_FMT_RU12LE = v4l2_fourcc('R', 'U', '1', '2')
    #: planar complex u
    SDR_FMT_PCU16BE = v4l2_fourcc('P', 'C', '1', '6')
    #: planar complex u
    SDR_FMT_PCU18BE = v4l2_fourcc('P', 'C', '1', '8')
    #: planar complex u
    SDR_FMT_PCU20BE = v4l2_fourcc('P', 'C', '2', '0')

    ###########################################
    # Touch formats - used for Touch devices. #
    ###########################################
    #: 16-bit signed d
    TCH_FMT_DELTA_TD16 = v4l2_fourcc('T', 'D', '1', '6')
    #: 8-bit signed d
    TCH_FMT_DELTA_TD08 = v4l2_fourcc('T', 'D', '0', '8')
    #: 16-bit unsigned touch d
    TCH_FMT_TU16 = v4l2_fourcc('T', 'U', '1', '6')
    #: 8-bit unsigned touch d
    TCH_FMT_TU08 = v4l2_fourcc('T', 'U', '0', '8')

    #####################
    # Meta-data formats #
    #####################
    #: R-Car VSP1 1-D H
    META_FMT_VSP1_HGO = v4l2_fourcc('V', 'S', 'P', 'H')
    #: R-Car VSP1 2-D H
    META_FMT_VSP1_HGT = v4l2_fourcc('V', 'S', 'P', 'T')
    #: UVC Payload Header m
    META_FMT_UVC = v4l2_fourcc('U', 'V', 'C', 'H')
    #: D4XX Payload Header m
    META_FMT_D4XX = v4l2_fourcc('D', '4', 'X', 'X')
    #: Vivid M
    META_FMT_VIVID = v4l2_fourcc('V', 'I', 'V', 'D')


class V4l2FormatDescFlags(IntFlag):
    """The v4l2 format flags."""
    #: No flags are set.
    NONE = 0x0000
    #: This is a compressed format.
    COMPRESSED = 0x0001
    #: This format is not native to the device but emulated through software
    #: (usually libv4l2), where possible try to use a native format instead
    #: for better performance.
    EMULATED = 0x0002
    CONTINUOUS_BYTESTREAM = 0x0004
    DYNAMIC_RESOLUTION = 0x0008


###############################################################################
#                   Frame Size and frame rate enumeration.
###############################################################################

###############################################################################
#
#       F R A M E   S I Z E   E N U M E R A T I O N
#
###############################################################################
class V4l2FrameSizeTypes(IntEnum):
    DISCRETE = 1,
    CONTINUOUS = 2,
    STEPWISE = 3,


class V4l2FrameSizeDiscrete(ctypes.Structure):
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


class V4l2FrameSizeStepwise(ctypes.Structure):
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
        ('discrete', V4l2FrameSizeDiscrete),
        ('stepwise', V4l2FrameSizeStepwise),
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
class V4l2FrameIvalTypes(IntEnum):
    DISCRETE = 1
    CONTINUOUS = 2
    STEPWISE = 3


class V4l2Fraction(ctypes.Structure):
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


class V4l2FrameIvalStepwise(ctypes.Structure):
    _fields_ = [
        ('min', V4l2Fraction),
        ('max', V4l2Fraction),
        ('step', V4l2Fraction),
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
        ('discrete', V4l2Fraction),
        ('stepwise', V4l2FrameIvalStepwise),
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

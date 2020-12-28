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
from ..utils.enumcontainer import BaseEnumContainer


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


class V4l2PixFormats(IntEnum):
    """An enumeration of all supported formats."""
    #: 8  RGB-3-3-2
    RGB332 = v4l2_fourcc('R', 'G', 'B', '1')
    #: 16  xxxxrrrr g
    RGB444 = v4l2_fourcc('R', '4', '4', '4')
    #: 16  aaaarrrr g
    ARGB444 = v4l2_fourcc('A', 'R', '1', '2')
    #: 16  xxxxrrrr g
    XRGB444 = v4l2_fourcc('X', 'R', '1', '2')
    #: 16  rrrrgggg b
    RGBA444 = v4l2_fourcc('R', 'A', '1', '2')
    #: 16  rrrrgggg b
    RGBX444 = v4l2_fourcc('R', 'X', '1', '2')
    #: 16  aaaabbbb g
    ABGR444 = v4l2_fourcc('A', 'B', '1', '2')
    #: 16  xxxxbbbb g
    XBGR444 = v4l2_fourcc('X', 'B', '1', '2')

    #########################################################################
    # Originally this had 'BA12' as fourcc, but this clashed with the older #
    # SGRBG12 which inexplicably used that same fourcc.                     #
    # So use 'GA12' instead for BGRA444.                                    #
    #########################################################################
    #: 16  bbbbgggg r
    BGRA444 = v4l2_fourcc('G', 'A', '1', '2')
    #: 16  bbbbgggg r
    BGRX444 = v4l2_fourcc('B', 'X', '1', '2')
    #: 16  RGB-5-5-5
    RGB555 = v4l2_fourcc('R', 'G', 'B', 'O')
    #: 16  ARGB-1-5-5-5
    ARGB555 = v4l2_fourcc('A', 'R', '1', '5')
    #: 16  XRGB-1-5-5-5
    XRGB555 = v4l2_fourcc('X', 'R', '1', '5')
    #: 16  RGBA-5-5-5-1
    RGBA555 = v4l2_fourcc('R', 'A', '1', '5')
    #: 16  RGBX-5-5-5-1
    RGBX555 = v4l2_fourcc('R', 'X', '1', '5')
    #: 16  ABGR-1-5-5-5
    ABGR555 = v4l2_fourcc('A', 'B', '1', '5')
    #: 16  XBGR-1-5-5-5
    XBGR555 = v4l2_fourcc('X', 'B', '1', '5')
    #: 16  BGRA-5-5-5-1
    BGRA555 = v4l2_fourcc('B', 'A', '1', '5')
    #: 16  BGRX-5-5-5-1
    BGRX555 = v4l2_fourcc('B', 'X', '1', '5')
    #: 16  RGB-5-6-5
    RGB565 = v4l2_fourcc('R', 'G', 'B', 'P')
    #: 16  RGB-5-5-5 B
    RGB555X = v4l2_fourcc('R', 'G', 'B', 'Q')
    #: 16  ARGB-5-5-5 B
    ARGB555X = v4l2_fourcc_be('A', 'R', '1', '5')
    #: 16  XRGB-5-5-5 B
    XRGB555X = v4l2_fourcc_be('X', 'R', '1', '5')
    #: 16  RGB-5-6-5 B
    RGB565X = v4l2_fourcc('R', 'G', 'B', 'R')
    #: 18  BGR-6-6-6
    BGR666 = v4l2_fourcc('B', 'G', 'R', 'H')
    #: 24  BGR-8-8-8
    BGR24 = v4l2_fourcc('B', 'G', 'R', '3')
    #: 24  RGB-8-8-8
    RGB24 = v4l2_fourcc('R', 'G', 'B', '3')
    #: 32  BGR-8-8-8-8
    BGR32 = v4l2_fourcc('B', 'G', 'R', '4')
    #: 32  BGRA-8-8-8-8
    ABGR32 = v4l2_fourcc('A', 'R', '2', '4')
    #: 32  BGRX-8-8-8-8
    XBGR32 = v4l2_fourcc('X', 'R', '2', '4')
    #: 32  ABGR-8-8-8-8
    BGRA32 = v4l2_fourcc('R', 'A', '2', '4')
    #: 32  XBGR-8-8-8-8
    BGRX32 = v4l2_fourcc('R', 'X', '2', '4')
    #: 32  RGB-8-8-8-8
    RGB32 = v4l2_fourcc('R', 'G', 'B', '4')
    #: 32  RGBA-8-8-8-8
    RGBA32 = v4l2_fourcc('A', 'B', '2', '4')
    #: 32  RGBX-8-8-8-8
    RGBX32 = v4l2_fourcc('X', 'B', '2', '4')
    #: 32  ARGB-8-8-8-8
    ARGB32 = v4l2_fourcc('B', 'A', '2', '4')
    #: 32  XRGB-8-8-8-8
    XRGB32 = v4l2_fourcc('B', 'X', '2', '4')

    #################
    # Grey formats. #
    #################
    #: 8  G
    GREY = v4l2_fourcc('G', 'R', 'E', 'Y')
    #: 4  G
    Y4 = v4l2_fourcc('Y', '0', '4', ' ')
    #: 6  G
    Y6 = v4l2_fourcc('Y', '0', '6', ' ')
    #: 10  G
    Y10 = v4l2_fourcc('Y', '1', '0', ' ')
    #: 12  G
    Y12 = v4l2_fourcc('Y', '1', '2', ' ')
    #: 16  G
    Y16 = v4l2_fourcc('Y', '1', '6', ' ')
    #: 16  Greyscale B
    Y16_BE = v4l2_fourcc_be('Y', '1', '6', ' ')

    ############################
    # Grey bit-packed formats. #
    ############################
    #: 10  Greyscale bit-p
    Y10BPACK = v4l2_fourcc('Y', '1', '0', 'B')
    #: 10  Greyscale, MIPI RAW10 p
    Y10P = v4l2_fourcc('Y', '1', '0', 'P')

    ####################
    # Palette formats. #
    ####################
    #: 8  8-bit p
    PAL8 = v4l2_fourcc('P', 'A', 'L', '8')

    ########################
    # Chrominance formats. #
    ########################
    #: 8  UV 4:4
    UV8 = v4l2_fourcc('U', 'V', '8', ' ')

    ##################################
    # Luminance+Chrominance formats. #
    ##################################
    #: 16  YUV 4:2:2
    YUYV = v4l2_fourcc('Y', 'U', 'Y', 'V')
    #: 16  YUV 4:2:2
    YYUV = v4l2_fourcc('Y', 'Y', 'U', 'V')
    #: 16 YVU 4:2:2
    YVYU = v4l2_fourcc('Y', 'V', 'Y', 'U')
    #: 16  YUV 4:2:2
    UYVY = v4l2_fourcc('U', 'Y', 'V', 'Y')
    #: 16  YUV 4:2:2
    VYUY = v4l2_fourcc('V', 'Y', 'U', 'Y')
    #: 12  YUV 4:1:1
    Y41P = v4l2_fourcc('Y', '4', '1', 'P')
    #: 16  xxxxyyyy u
    YUV444 = v4l2_fourcc('Y', '4', '4', '4')
    #: 16  YUV-5-5-5
    YUV555 = v4l2_fourcc('Y', 'U', 'V', 'O')
    #: 16  YUV-5-6-5
    YUV565 = v4l2_fourcc('Y', 'U', 'V', 'P')
    #: 32  YUV-8-8-8-8
    YUV32 = v4l2_fourcc('Y', 'U', 'V', '4')
    #: 32  AYUV-8-8-8-8
    AYUV32 = v4l2_fourcc('A', 'Y', 'U', 'V')
    #: 32  XYUV-8-8-8-8
    XYUV32 = v4l2_fourcc('X', 'Y', 'U', 'V')
    #: 32  VUYA-8-8-8-8
    VUYA32 = v4l2_fourcc('V', 'U', 'Y', 'A')
    #: 32  VUYX-8-8-8-8
    VUYX32 = v4l2_fourcc('V', 'U', 'Y', 'X')
    #: 8  8-bit c
    HI240 = v4l2_fourcc('H', 'I', '2', '4')
    #: 8  YUV 4:2:0 16x16 m
    HM12 = v4l2_fourcc('H', 'M', '1', '2')
    #: 12  YUV 4:2:0 2 lines y, 1 line uv i
    M420 = v4l2_fourcc('M', '4', '2', '0')

    #################################################
    # two planes -- one Y, one Cr + Cb interleaved. #
    #################################################
    #: 12  Y/CbCr 4:2:0
    NV12 = v4l2_fourcc('N', 'V', '1', '2')
    #: 12  Y/CrCb 4:2:0
    NV21 = v4l2_fourcc('N', 'V', '2', '1')
    #: 16  Y/CbCr 4:2:2
    NV16 = v4l2_fourcc('N', 'V', '1', '6')
    #: 16  Y/CrCb 4:2:2
    NV61 = v4l2_fourcc('N', 'V', '6', '1')
    #: 24  Y/CbCr 4:4:4
    NV24 = v4l2_fourcc('N', 'V', '2', '4')
    #: 24  Y/CrCb 4:4:4
    NV42 = v4l2_fourcc('N', 'V', '4', '2')

    ###############################################################
    # two non contiguous planes - one Y, one Cr + Cb interleaved. #
    ###############################################################
    #: 12  Y/CbCr 4:2:0
    NV12M = v4l2_fourcc('N', 'M', '1', '2')
    #: 21  Y/CrCb 4:2:0
    NV21M = v4l2_fourcc('N', 'M', '2', '1')
    #: 16  Y/CbCr 4:2:2
    NV16M = v4l2_fourcc('N', 'M', '1', '6')
    #: 16  Y/CrCb 4:2:2
    NV61M = v4l2_fourcc('N', 'M', '6', '1')
    #: 12  Y/CbCr 4:2:0 64x32 m
    NV12MT = v4l2_fourcc('T', 'M', '1', '2')
    #: 12  Y/CbCr 4:2:0 16x16 m
    NV12MT_16X16 = v4l2_fourcc('V', 'M', '1', '2')

    ############################
    # three planes - Y Cb, Cr. #
    ############################
    #: 9  YUV 4:1:0
    YUV410 = v4l2_fourcc('Y', 'U', 'V', '9')
    #: 9  YVU 4:1:0
    YVU410 = v4l2_fourcc('Y', 'V', 'U', '9')
    #: 12  YVU411 p
    YUV411P = v4l2_fourcc('4', '1', '1', 'P')
    #: 12  YUV 4:2:0
    YUV420 = v4l2_fourcc('Y', 'U', '1', '2')
    #: 12  YVU 4:2:0
    YVU420 = v4l2_fourcc('Y', 'V', '1', '2')
    #: 16  YVU422 p
    YUV422P = v4l2_fourcc('4', '2', '2', 'P')

    ############################################
    # three non contiguous planes - Y, Cb, Cr. #
    ############################################
    #: 12  YUV420 p
    YUV420M = v4l2_fourcc('Y', 'M', '1', '2')
    #: 12  YVU420 p
    YVU420M = v4l2_fourcc('Y', 'M', '2', '1')
    #: 16  YUV422 p
    YUV422M = v4l2_fourcc('Y', 'M', '1', '6')
    #: 16  YVU422 p
    YVU422M = v4l2_fourcc('Y', 'M', '6', '1')
    #: 24  YUV444 p
    YUV444M = v4l2_fourcc('Y', 'M', '2', '4')
    #: 24  YVU444 p
    YVU444M = v4l2_fourcc('Y', 'M', '4', '2')

    ######################################################################
    # Bayer formats - see http://www.siliconimaging.com/RGB%20Bayer.htm. #
    ######################################################################
    #: 8  BGBG.. GRGR.
    SBGGR8 = v4l2_fourcc('B', 'A', '8', '1')
    #: 8  GBGB.. RGRG.
    SGBRG8 = v4l2_fourcc('G', 'B', 'R', 'G')
    #: 8  GRGR.. BGBG.
    SGRBG8 = v4l2_fourcc('G', 'R', 'B', 'G')
    #: 8  RGRG.. GBGB.
    SRGGB8 = v4l2_fourcc('R', 'G', 'G', 'B')
    #: 10  BGBG.. GRGR.
    SBGGR10 = v4l2_fourcc('B', 'G', '1', '0')
    #: 10  GBGB.. RGRG.
    SGBRG10 = v4l2_fourcc('G', 'B', '1', '0')
    #: 10  GRGR.. BGBG.
    SGRBG10 = v4l2_fourcc('B', 'A', '1', '0')
    #: 10  RGRG.. GBGB.
    SRGGB10 = v4l2_fourcc('R', 'G', '1', '0')
    #######################################################
    # 10bit raw bayer packed, 5 bytes for every 4 pixels. #
    #######################################################
    SBGGR10P = v4l2_fourcc('p', 'B', 'A', 'A')
    SGBRG10P = v4l2_fourcc('p', 'G', 'A', 'A')
    SGRBG10P = v4l2_fourcc('p', 'g', 'A', 'A')
    SRGGB10P = v4l2_fourcc('p', 'R', 'A', 'A')
    ###############################################
    # 10bit raw bayer a-law compressed to 8 bits. #
    ###############################################
    SBGGR10ALAW8 = v4l2_fourcc('a', 'B', 'A', '8')
    SGBRG10ALAW8 = v4l2_fourcc('a', 'G', 'A', '8')
    SGRBG10ALAW8 = v4l2_fourcc('a', 'g', 'A', '8')
    SRGGB10ALAW8 = v4l2_fourcc('a', 'R', 'A', '8')
    ##############################################
    # 10bit raw bayer DPCM compressed to 8 bits. #
    ##############################################
    SBGGR10DPCM8 = v4l2_fourcc('b', 'B', 'A', '8')
    SGBRG10DPCM8 = v4l2_fourcc('b', 'G', 'A', '8')
    SGRBG10DPCM8 = v4l2_fourcc('B', 'D', '1', '0')
    SRGGB10DPCM8 = v4l2_fourcc('b', 'R', 'A', '8')
    #: 12  BGBG.. GRGR.
    SBGGR12 = v4l2_fourcc('B', 'G', '1', '2')
    #: 12  GBGB.. RGRG.
    SGBRG12 = v4l2_fourcc('G', 'B', '1', '2')
    #: 12  GRGR.. BGBG.
    SGRBG12 = v4l2_fourcc('B', 'A', '1', '2')
    #: 12  RGRG.. GBGB.
    SRGGB12 = v4l2_fourcc('R', 'G', '1', '2')
    #######################################################
    # 12bit raw bayer packed, 6 bytes for every 4 pixels. #
    #######################################################
    SBGGR12P = v4l2_fourcc('p', 'B', 'C', 'C')
    SGBRG12P = v4l2_fourcc('p', 'G', 'C', 'C')
    SGRBG12P = v4l2_fourcc('p', 'g', 'C', 'C')
    SRGGB12P = v4l2_fourcc('p', 'R', 'C', 'C')
    #######################################################
    # 14bit raw bayer packed, 7 bytes for every 4 pixels. #
    #######################################################
    SBGGR14P = v4l2_fourcc('p', 'B', 'E', 'E')
    SGBRG14P = v4l2_fourcc('p', 'G', 'E', 'E')
    SGRBG14P = v4l2_fourcc('p', 'g', 'E', 'E')
    SRGGB14P = v4l2_fourcc('p', 'R', 'E', 'E')
    #: 16  BGBG.. GRGR.
    SBGGR16 = v4l2_fourcc('B', 'Y', 'R', '2')
    #: 16  GBGB.. RGRG.
    SGBRG16 = v4l2_fourcc('G', 'B', '1', '6')
    #: 16  GRGR.. BGBG.
    SGRBG16 = v4l2_fourcc('G', 'R', '1', '6')
    #: 16  RGRG.. GBGB.
    SRGGB16 = v4l2_fourcc('R', 'G', '1', '6')

    ################
    # HSV formats. #
    ################
    HSV24 = v4l2_fourcc('H', 'S', 'V', '3')
    HSV32 = v4l2_fourcc('H', 'S', 'V', '4')

    #######################
    # compressed formats. #
    #######################
    #: Motion-J
    MJPEG = v4l2_fourcc('M', 'J', 'P', 'G')
    #: JFIF J
    JPEG = v4l2_fourcc('J', 'P', 'E', 'G')
    #: 1
    DV = v4l2_fourcc('d', 'v', 's', 'd')
    #: MPEG-1/2/4 M
    MPEG = v4l2_fourcc('M', 'P', 'E', 'G')
    #: H264 with start c
    H264 = v4l2_fourcc('H', '2', '6', '4')
    #: H264 without start c
    H264_NO_SC = v4l2_fourcc('A', 'V', 'C', '1')
    #: H264 M
    H264_MVC = v4l2_fourcc('M', '2', '6', '4')
    #: H
    H263 = v4l2_fourcc('H', '2', '6', '3')
    #: MPEG-1 E
    MPEG1 = v4l2_fourcc('M', 'P', 'G', '1')
    #: MPEG-2 E
    MPEG2 = v4l2_fourcc('M', 'P', 'G', '2')
    #: MPEG-2 parsed slice d
    MPEG2_SLICE = v4l2_fourcc('M', 'G', '2', 'S')
    #: MPEG-4 part 2 E
    MPEG4 = v4l2_fourcc('M', 'P', 'G', '4')
    #: X
    XVID = v4l2_fourcc('X', 'V', 'I', 'D')
    #: SMPTE 421M Annex G compliant s
    VC1_ANNEX_G = v4l2_fourcc('V', 'C', '1', 'G')
    #: SMPTE 421M Annex L compliant s
    VC1_ANNEX_L = v4l2_fourcc('V', 'C', '1', 'L')
    #: V
    VP8 = v4l2_fourcc('V', 'P', '8', '0')
    #: V
    VP9 = v4l2_fourcc('V', 'P', '9', '0')
    #: HEVC aka H.2
    HEVC = v4l2_fourcc('H', 'E', 'V', 'C')
    #: Fast Walsh Hadamard Transform (vicodec)
    FWHT = v4l2_fourcc('F', 'W', 'H', 'T')
    #: Stateless FWHT (vicodec)
    FWHT_STATELESS = v4l2_fourcc('S', 'F', 'W', 'H')

    #############################
    #  Vendor-specific formats. #
    #############################
    #: cpia1 Y
    CPIA1 = v4l2_fourcc('C', 'P', 'I', 'A')
    #: Winnov hw c
    WNVA = v4l2_fourcc('W', 'N', 'V', 'A')
    #: SN9C10x c
    SN9C10X = v4l2_fourcc('S', '9', '1', '0')
    #: SN9C20x YUV 4:2:0
    SN9C20X_I420 = v4l2_fourcc('S', '9', '2', '0')
    #: pwc older w
    PWC1 = v4l2_fourcc('P', 'W', 'C', '1')
    #: pwc newer w
    PWC2 = v4l2_fourcc('P', 'W', 'C', '2')
    #: ET61X251 c
    ET61X251 = v4l2_fourcc('E', '6', '2', '5')
    #: YUYV per l
    SPCA501 = v4l2_fourcc('S', '5', '0', '1')
    #: YYUV per l
    SPCA505 = v4l2_fourcc('S', '5', '0', '5')
    #: YUVY per l
    SPCA508 = v4l2_fourcc('S', '5', '0', '8')
    #: compressed GBRG b
    SPCA561 = v4l2_fourcc('S', '5', '6', '1')
    #: compressed BGGR b
    PAC207 = v4l2_fourcc('P', '2', '0', '7')
    #: compressed BGGR b
    MR97310A = v4l2_fourcc('M', '3', '1', '0')
    #: compressed RGGB b
    JL2005BCD = v4l2_fourcc('J', 'L', '2', '0')
    #: compressed GBRG b
    SN9C2028 = v4l2_fourcc('S', 'O', 'N', 'X')
    #: compressed RGGB b
    SQ905C = v4l2_fourcc('9', '0', '5', 'C')
    #: Pixart 73xx J
    PJPG = v4l2_fourcc('P', 'J', 'P', 'G')
    #: ov511 J
    OV511 = v4l2_fourcc('O', '5', '1', '1')
    #: ov518 J
    OV518 = v4l2_fourcc('O', '5', '1', '8')
    #: stv0680 b
    STV0680 = v4l2_fourcc('S', '6', '8', '0')
    #: tm5600/t
    TM6000 = v4l2_fourcc('T', 'M', '6', '0')
    #: one line of Y then 1 line of V
    CIT_YYVYUY = v4l2_fourcc('C', 'I', 'T', 'V')
    #: YUV420 planar in blocks of 256 p
    KONICA420 = v4l2_fourcc('K', 'O', 'N', 'I')
    #: JPEG-L
    JPGL = v4l2_fourcc('J', 'P', 'G', 'L')
    #: se401 janggu compressed r
    SE401 = v4l2_fourcc('S', '4', '0', '1')
    #: S5C73M3 interleaved UYVY/J
    S5C_UYVY_JPG = v4l2_fourcc('S', '5', 'C', 'I')
    #: Greyscale 8-bit L/R i
    Y8I = v4l2_fourcc('Y', '8', 'I', ' ')
    #: Greyscale 12-bit L/R i
    Y12I = v4l2_fourcc('Y', '1', '2', 'I')
    #: Depth data 16-b
    Z16 = v4l2_fourcc('Z', '1', '6', ' ')
    #: Mediatek compressed block m
    MT21C = v4l2_fourcc('M', 'T', '2', '1')
    #: Intel Planar Greyscale 10-bit and Depth 16-b
    INZI = v4l2_fourcc('I', 'N', 'Z', 'I')
    #: Sunxi Tiled NV12 F
    SUNXI_TILED_NV12 = v4l2_fourcc('S', 'T', '1', '2')
    #: Intel 4-bit packed depth confidence i
    CNF4 = v4l2_fourcc('C', 'N', 'F', '4')

    #########################################################################
    # 10bit raw bayer packed, 32 bytes for every 25 pixels, last LSB 6 bits #
    # unused.                                                               #
    #########################################################################
    #: IPU3 packed 10-bit BGGR b
    IPU3_SBGGR10 = v4l2_fourcc('i', 'p', '3', 'b')
    #: IPU3 packed 10-bit GBRG b
    IPU3_SGBRG10 = v4l2_fourcc('i', 'p', '3', 'g')
    #: IPU3 packed 10-bit GRBG b
    IPU3_SGRBG10 = v4l2_fourcc('i', 'p', '3', 'G')
    #: IPU3 packed 10-bit RGGB b
    IPU3_SRGGB10 = v4l2_fourcc('i', 'p', '3', 'r')


class V4l2SdrFormats(IntEnum):
    """SDR formats - used only for Software Defined Radio devices."""
    #: IQ u
    CU8 = v4l2_fourcc('C', 'U', '0', '8')
    #: IQ u
    CU16LE = v4l2_fourcc('C', 'U', '1', '6')
    #: complex s
    CS8 = v4l2_fourcc('C', 'S', '0', '8')
    #: complex s
    CS14LE = v4l2_fourcc('C', 'S', '1', '4')
    #: real u
    RU12LE = v4l2_fourcc('R', 'U', '1', '2')
    #: planar complex u
    PCU16BE = v4l2_fourcc('P', 'C', '1', '6')
    #: planar complex u
    PCU18BE = v4l2_fourcc('P', 'C', '1', '8')
    #: planar complex u
    PCU20BE = v4l2_fourcc('P', 'C', '2', '0')


class V4l2TouchFormats(IntEnum):
    """Touch formats - used for Touch devices."""
    #: 16-bit signed d
    DELTA_TD16 = v4l2_fourcc('T', 'D', '1', '6')
    #: 8-bit signed d
    DELTA_TD08 = v4l2_fourcc('T', 'D', '0', '8')
    #: 16-bit unsigned touch d
    TU16 = v4l2_fourcc('T', 'U', '1', '6')
    #: 8-bit unsigned touch d
    TU08 = v4l2_fourcc('T', 'U', '0', '8')


class V4l2MetaFormats(IntEnum):
    """Meta-data formats."""
    #: R-Car VSP1 1-D H
    VSP1_HGO = v4l2_fourcc('V', 'S', 'P', 'H')
    #: R-Car VSP1 2-D H
    VSP1_HGT = v4l2_fourcc('V', 'S', 'P', 'T')
    #: UVC Payload Header m
    UVC = v4l2_fourcc('U', 'V', 'C', 'H')
    #: D4XX Payload Header m
    D4XX = v4l2_fourcc('D', '4', 'X', 'X')
    #: Vivid M
    VIVID = v4l2_fourcc('V', 'I', 'V', 'D')


# The format enums contained in V4l2Formats.
_v4l2_formats = [V4l2PixFormats,
                 V4l2SdrFormats,
                 V4l2TouchFormats,
                 V4l2MetaFormats,
                 ]


class V4l2Formats(BaseEnumContainer, enums=_v4l2_formats):
    __doc__ = """An Enum-Container for all V4l2Formats.
    This class delegates its operations to the contained enums.
    For more information, see:
    \t""" + "\t\n\t".join(map(lambda x: "py:class:`"+x.__name__+"`",
                              _v4l2_formats))


class V4l2PixFormatFlags(IntFlag):
    #: The color values are premultiplied by the alpha channel value. E.g., if
    #: a light blue pixel with 50% transparency was described by RGBA values
    #: (128, 192, 255, 128), the same pixel described with premultiplied colors
    #: would be described by RGBA values (64, 96, 128, 128)
    PREMULTIPLIED_ALPHA = 0x00000001


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


class V4l2FrameSizeTypes(IntEnum):
    """The type of frame size."""
    #: Discrete frame size.
    DISCRETE = 1
    #: Continuous frame size.
    CONTINUOUS = 2
    #: Step-wise defined frame size.
    STEPWISE = 3


class V4l2FrameIvalTypes(IntEnum):
    """The type of frame interval."""
    #: Discrete frame interval.
    DISCRETE = 1
    #: Continuous frame interval.
    CONTINUOUS = 2
    #: Step-wise defined frame interval.
    STEPWISE = 3


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


class V4l2Field(IntEnum):
    """The field order.
    Implemntation of enum v4l2_field in uapi/include/videodev2.h
    """
    #: Applications request this field order when any field format is
    #: acceptable. Drivers choose depending on hardware capabilities or e.g.
    #: the requested image size, and return the actual field order. Drivers
    #: must never return :py:attr:`V4l2Field.ANY`. If multiple field orders are
    #: possible the driver must choose one of the possible field orders during
    #: :py:meth:`V4l2IocOps.set_format` or :py:meth:`V4l2IocOps.try_format`.
    #: :py:attr:`v4l2Buffer.field` can never be :py:attr:`V4l2Field.ANY`.
    ANY = 0
    #: Images are in progressive (frame-based) format, not interlaced
    #: (field-based). (I.e., this device has no fields)
    NONE = 1
    #: Images consist of the top (aka odd) field only.
    TOP = 2
    #: Images consist of the bottom (aka even) field only. Applications may
    #: wish to prevent a device from capturing interlaced images because they
    #: will have “comb” or “feathering” artefacts around moving objects.
    BOTTOM = 3
    #: Images contain both fields, interleaved line by line. The temporal order
    #: of the fields (whether the top or bottom field is older) depends on the
    #: current video standard. In M/NTSC the bottom field is the older field.
    #: In all other standards the top field is the older field.
    INTERLACED = 4
    #: Images contain both fields, the top field lines are stored first in
    #: memory, immediately followed by the bottom field lines. Fields are
    #: always stored in temporal order, the older one first in memory. Image
    #: sizes refer to the frame, not fields.
    SEQUENTIAL_TOP_BOTTOM = 5
    #: Images contain both fields, the bottom field lines are stored first in
    #: memory, immediately followed by the top field lines. Fields are always
    #: stored in temporal order, the older one first in memory. Image sizes
    #: refer to the frame, not fields.
    SEQUENTIAL_BOTTOM_TOP = 6
    #: The two fields of a frame are passed in separate buffers, in temporal
    #: order, i. e. the older one first. To indicate the field parity (whether
    #: the current field is a top or bottom field) the driver or application,
    #: depending on data direction, must set :py:attr:`V4l2IoctlBuffer.field`
    #: to :py:attr:`V4l2Field.TOP` or :py:attr:`V4l2Field.BOTTOM`. Any two
    #: successive fields pair to build a frame. If fields are successive,
    #: without any dropped fields between them (fields can drop individually),
    #: can be determined from the :py:attr:`V4l2IoctlBuffer.sequence`. This
    #: format cannot be selected when using the read/write I/O method since
    #: there is no way to communicate if a field was a top or bottom field.
    ALTERNATE = 7
    #: Images contain both fields, interleaved line by line, top field first.
    #: The top field is the older field.
    INTERLACED_TOP_BOTTOM = 8
    #: Images contain both fields, interleaved line by line, top field first.
    #: The bottom field is the older field.
    INTERLACED_BOTTOM_TOP = 9

    def has_top(self):
        """If the format has a top field.
        Implemntation of the macro V4L2_FIELD_HAS_TOP(field) in
        uapi/include/videodev2.h
        """
        return (self == V4l2Field.TOP or
                self == V4l2Field.INTERLACED or
                self == V4l2Field.INTERLACED_TOP_BOTTOM or
                self == V4l2Field.INTERLACED_BOTTOM_TOP or
                self == V4l2Field.SEQUENTIAL_TOP_BOTTOM or
                self == V4l2Field.SEQUENTIAL_BOTTOM_TOP)

    def has_bottom(self):
        """If the format has a bottom field.
        Implemntation of the macro V4L2_FIELD_HAS_BOTTOM(field) in
        uapi/include/videodev2.h
        """
        return (self == V4l2Field.BOTTOM or
                self == V4l2Field.INTERLACED or
                self == V4l2Field.INTERLACED_TOP_BOTTOM or
                self == V4l2Field.INTERLACED_BOTTOM_TOP or
                self == V4l2Field.SEQUENTIAL_TOP_BOTTOM or
                self == V4l2Field.SEQUENTIAL_BOTTOM_TOP)

    def has_both(self):
        """If the format has both top and bottom fields.
        Implemntation of the macro V4L2_FIELD_HAS_BOTH(field) in
        uapi/include/videodev2.h
        """
        return (self == V4l2Field.INTERLACED or
                self == V4l2Field.INTERLACED_TOP_BOTTOM or
                self == V4l2Field.INTERLACED_BOTTOM_TOP or
                self == V4l2Field.SEQUENTIAL_TOP_BOTTOM or
                self == V4l2Field.SEQUENTIAL_BOTTOM_TOP)

    def has_top_or_bottom(self):
        """If the format has either a top or bottom field.
        Implemntation of the macro V4L2_FIELD_HAS_T_OR_B(field) in
        uapi/include/videodev2.h
        """
        return (self == V4l2Field.BOTTOM or
                self == V4l2Field.TOP or
                self == V4l2Field.ALTERNATE)

    def is_interlaced(self):
        """If the format has interlaced fields.
        Implemntation of the macro V4L2_FIELD_IS_INTERLACED(field) in
        uapi/include/videodev2.h
        """
        return (self == V4l2Field.INTERLACED or
                self == V4l2Field.INTERLACED_TOP_BOTTOM or
                self == V4l2Field.INTERLACED_BOTTOM_TOP)

    def is_sequential(self):
        """If the format has sequential fields.
        Implemntation of the macro V4L2_FIELD_IS_SEQUENTIAL(field) in
        uapi/include/videodev2.h
        """
        return (self == V4l2Field.SEQUENTIAL_TOP_BOTTOM or
                self == V4l2Field.SEQUENTIAL_BOTTOM_TOP)


class V4l2ColorSpace(IntEnum):
    """The color space.
    Implemntation of enum v4l2_colorspace in uapi/include/videodev2.h
    see also http://vektor.theorem.ca/graphics/ycbcr/
    """
    #: Default colorspace, i.e. let the driver figure it out.
    #: Can only be used with video capture.
    DEFAULT = 0
    #: SMPTE 170M: used for broadcast NTSC/PAL SDTV.
    SMPTE170M = 1
    #: Obsolete pre-1998 SMPTE 240M HDTV standard, superseded by Rec 709.
    SMPTE240M = 2
    #: Rec.709: used for HDTV.
    REC709 = 3
    #: Deprecated, do not use. No driver will ever return this. This was
    #: based on a misunderstanding of the bt878 datasheet.
    BT878 = 4
    #: NTSC 1953 colorspace. This only makes sense when dealing with
    #: really, really old NTSC recordings. Superseded by SMPTE 170M.
    _470_SYSTEM_M = 5
    #: EBU Tech 3213 PAL/SECAM colorspace. This only makes sense when
    #: dealing with really old PAL/SECAM recordings. Superseded by
    #: SMPTE 170M.
    _470_SYSTEM_BG = 6
    #: Effectively shorthand for V4L2_COLORSPACE_SRGB, V4L2_YCBCR_ENC_601
    #: and V4L2_QUANTIZATION_FULL_RANGE. To be used for (Motion-)JPEG.
    JPEG = 7
    #: For RGB colorspaces such as produces by most webcams.
    SRGB = 8
    #: opRGB colorspace.
    OPRGB = 9
    #: BT.2020 colorspace, used for UHDTV.
    BT2020 = 10
    #: Raw colorspace: for RAW unprocessed images.
    RAW = 11
    #: DCI-P3 colorspace, used by cinema projectors.
    DCI_P3 = 12


class V4l2XferFunc(IntEnum):
    """V4L2 Transfer Function."""
    #: Mapping of :py:attr:`V4l2XferFunc.DEFAULT` to actual transfer functions
    #: for the various colorspaces:
    #:
    #: :py:attr:`V4l2ColorSpace.SMPTE170M`,
    #: :py:attr:`V4l2ColorSpace.470_SYSTEM_M`,
    #: :py:attr:`V4l2ColorSpace.470_SYSTEM_BG`,
    #: :py:attr:`V4l2ColorSpace.REC709` and :py:attr:`V4l2ColorSpace.BT2020`:
    #: :py:attr:`V4l2XferFunc.709`
    #:
    #: :py:attr:`V4l2ColorSpace.SRGB`, :py:attr:`V4l2ColorSpace.JPEG`:
    #: :py:attr:`V4l2XferFunc.SRGB`
    #:
    #: :py:attr:`V4l2ColorSpace.OPRGB`: :py:attr:`V4l2XferFunc.OPRGB`
    #:
    #: :py:attr:`V4l2ColorSpace.SMPTE240M`: :py:attr:`V4l2XferFunc.SMPTE240M`
    #:
    #: :py:attr:`V4l2ColorSpace.RAW`: :py:attr:`V4l2XferFunc.NONE`
    #:
    #: :py:attr:`V4l2ColorSpace.DCI_P3`: :py:attr:`V4l2XferFunc.DCI_P3`
    DEFAULT = 0
    _709 = 1
    SRGB = 2
    OPRGB = 3
    SMPTE240M = 4
    NONE = 5
    DCI_P3 = 6
    SMPTE2084 = 7


class V4l2YcbcrEncoding(IntEnum):
    """V4L2 Y’CbCr Encodings."""
    #: Mapping of :py:attr:`V4l2YcbcrEncoding.DEFAULT` to actual encodings for
    #: the various colorspaces:
    #:
    #: :py:attr:`V4l2ColorSpace.SMPTE170M`,
    #: :py:attr:`V4l2ColorSpace.470_SYSTEM_M`,
    #: :py:attr:`V4l2ColorSpace.470_SYSTEM_BG`, :py:attr:`V4l2ColorSpace.SRGB`,
    #: :py:attr:`V4l2ColorSpace.OPRGB` and :py:attr:`V4l2ColorSpace.JPEG`:
    #: :py:attr:`V4l2YcbcrEncoding.601`
    #:
    #: :py:attr:`V4l2ColorSpace.REC709` and :py:attr:`V4l2ColorSpace.DCI_P3`:
    #: :py:attr:`V4l2YcbcrEncoding.709`
    #:
    #: :py:attr:`V4l2ColorSpace.BT2020`: :py:attr:`V4l2YcbcrEncoding.BT2020`
    #:
    #: :py:attr:`V4l2ColorSpace.SMPTE240M`:
    #: :py:attr:`V4l2YcbcrEncoding.SMPTE240M`
    DEFAULT = 0
    #: ITU-R 601 -- SDTV.
    _601 = 1
    #: Rec. 709 -- HDTV.
    _709 = 2
    #: ITU-R 601/EN 61966-2-4 Extended Gamut -- SDTV.
    XV601 = 3
    #: Rec. 709/EN 61966-2-4 Extended Gamut -- HDTV.
    XV709 = 4
    #: sYCC (Y'CbCr encoding of sRGB), identical to ENC_601. It was added
    #: originally due to a misunderstanding of the sYCC standard. It should
    #: not be used, instead use :py:attr:`V4l2YcbcrEncoding.601`.
    SYCC = 5
    #: BT.2020 Non-constant Luminance Y'CbCr.
    BT2020 = 6
    #: BT.2020 Constant Luminance Y'CbcCrc.
    BT2020_CONST_LUM = 7
    #: SMPTE 240M -- Obsolete HDTV.
    SMPTE240M = 8


class V4l2HsvEncoding(IntEnum):
    """V4L2 HSV Encodings."""
    #: For the Hue, each LSB is two degrees.
    ENC_180 = 128
    #: For the Hue, the 360 degrees are mapped into 8 bits, i.e. each LSB is
    #: roughly 1.41 degrees.
    ENC_256 = 129


class V4l2Quantization(IntEnum):
    """V4L2 Quantization Methods."""
    #: Use the default quantization encoding as defined by the colorspace. This
    #: is always full range for R’G’B’ (except for the BT.2020 colorspace) and
    #: HSV. It is usually limited range for Y’CbCr.
    DEFAULT = 0
    #: Use the full range quantization encoding. I.e. the range [0…1] is mapped
    #: to [0…255] (with possible clipping to [1…254] to avoid the 0x00 and 0xff
    #: values). Cb and Cr are mapped from [-0.5…0.5] to [0…255] (with possible
    #: clipping to [1…254] to avoid the 0x00 and 0xff values).
    FULL_RANGE = 1
    #: Use the limited range quantization encoding. I.e. the range [0…1] is
    #: mapped to [16…235]. Cb and Cr are mapped from [-0.5…0.5] to [16…240].
    LIM_RANGE = 2

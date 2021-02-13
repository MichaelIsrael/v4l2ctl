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
from .ioctls import (V4l2Formats, V4l2FormatDescFlags, IoctlError,
                     V4l2BufferType, V4l2Field,
                     )
from .ioctls.v4l2ioctlstructs import (V4l2IoctlFmtDesc, V4l2IoctlFormat,
                                      V4l2IoctlFormatUnion,
                                      V4l2IoctlPixFormat,
                                      V4l2IoctlMetaFormat,
                                      )
from .v4l2frame import V4l2FrameSize
from abc import ABC, abstractmethod


class V4l2Format(ABC):
    _repr_attrs_ = ()

    """The v4l2 format information."""
    def __new__(cls, v4l2_device, fmt=None, *args, **kwargs):
        # Return an instance of the suitable child class instead.

        if fmt.type == V4l2BufferType.VIDEO_CAPTURE or \
           fmt.type == V4l2BufferType.VIDEO_OUTPUT:
            return super().__new__(V4l2PixFormat, *args, **kwargs)

        elif fmt.type == V4l2BufferType.VIDEO_CAPTURE_MPLANE or \
                fmt.type == V4l2BufferType.VIDEO_OUTPUT_MPLANE:
            return super().__new__(V4l2PixFormatMplane, *args, **kwargs)

        elif fmt.type == V4l2BufferType.VIDEO_OVERLAY or \
                fmt.type == V4l2BufferType.VIDEO_OUTPUT_OVERLAY:
            return super().__new__(V4l2Window, *args, **kwargs)

        elif fmt.type == V4l2BufferType.VBI_CAPTURE or \
                fmt.type == V4l2BufferType.VBI_OUTPUT:
            return super().__new__(V4l2VbiFormat, *args, **kwargs)

        elif fmt.type == V4l2BufferType.SLICED_VBI_CAPTURE or \
                fmt.type == V4l2BufferType.SLICED_VBI_OUTPUT:
            return super().__new__(V4l2SlicedVbiFormat, *args, **kwargs)

        elif fmt.type == V4l2BufferType.SDR_CAPTURE or \
                fmt.type == V4l2BufferType.SDR_OUTPUT:
            return super().__new__(V4l2SdrFormat)

        elif fmt.type == V4l2BufferType.META_CAPTURE or \
                fmt.type == V4l2BufferType.META_OUTPUT:
            return super().__new__(V4l2MetaFormat, *args, **kwargs)

        else:
            raise ValueError(f"Unsupported V4l2 Buffer type: {str(fmt.type)}")

    def __init__(self, v4l2_device, fmt=None):
        self._device = v4l2_device
        self._buffer_type = fmt.type
        f = None
        if isinstance(fmt, V4l2IoctlFmtDesc):
            self.__format = fmt.pixelformat
            self.__fmt_desc = fmt
        elif isinstance(fmt, V4l2IoctlFormat):
            self.__format = None
            self.__fmt_desc = None
            f = fmt
        else:
            raise Exception("TODO")

        self._update_format(f)

    @abstractmethod
    def _to_v4l2(self):
        raise NotImplementedError()

    @property
    def _fmt_desc(self):
        if self.__fmt_desc is None:
            raise NotImplementedError()

        return self.__fmt_desc

    @property
    @abstractmethod
    def _data_format(self):
        raise NotImplementedError()

    @abstractmethod
    def _update_format(self, fmt=None):
        raise NotImplementedError()

    def try_format(self):
        """Try the format to update the properties from the driver."""
        fmt = self._device._ioc_ops.try_format(type=self.buffer_type,
                                               fmt=self._to_v4l2())
        self._update_format(fmt)

    @property
    def format(self):
        "The format type (see :class:`V4l2Formats`)."
        if self.__format:
            return V4l2Formats(self.__format)
        else:
            return V4l2Formats(self._data_format)

    @property
    def buffer_type(self):
        "The format type (see :class:`V4l2Formats`)."
        return V4l2BufferType(self._buffer_type)

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
                frm_size = self._device._ioc_ops.enum_frame_sizes(
                    index=fr_idx,
                    pixel_format=self._fmt_desc.pixelformat)
            except IoctlError:
                break
            else:
                yield V4l2FrameSize(self._device, frm_size)
            fr_idx += 1

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return ("{cls}(format={fmt}, description={desc}, flags={flgs}{attrs})"
                ).format(cls=self.__class__.__name__,
                         fmt=self.format.name,
                         desc=self.description,
                         flgs=self.flags,
                         attrs=",".join([""] +
                                        [" %s=%s" % (a, getattr(self, a))
                                         for a in self._repr_attrs_])
                         )


class V4l2PixFormat(V4l2Format):
    """Interface for :py:class:`V4l2IoctlPixFormat`."""
    _repr_attrs_ = ("height", "width", "field_order")

    def _to_v4l2(self):
        return V4l2IoctlFormatUnion(pix=self._v4l2_fmt)

    @property
    def _data_format(self):
        return self._v4l2_fmt.pixelformat

    def _update_format(self, fmt=None):
        if not fmt:
            if not hasattr(self, "_v4l2_fmt"):
                self._v4l2_fmt = V4l2IoctlPixFormat()
            fmt = self._device._ioc_ops.get_format(type=self.buffer_type,
                                                   fmt=self._to_v4l2())
        # V4l2IoctlPixFormat
        self._v4l2_fmt = fmt.fmt.pix

    @property
    def width(self):
        return self._v4l2_fmt.width

    @property
    def height(self):
        return self._v4l2_fmt.height

    @property
    def field_order(self):
        return V4l2Field(self._v4l2_fmt.field)

    @property
    def bytes_per_line(self):
        return self._v4l2_fmt.bytesperline

    @property
    def image_size(self):
        return self._v4l2_fmt.sizeimage

    @property
    def colorspace(self):
        return self._v4l2_fmt.colorspace

    @property
    def priv(self):
        return self._v4l2_fmt.priv

    @property
    def flags(self):
        return self._v4l2_fmt.flags

    @property
    def ycbcr_enc(self):
        return self._v4l2_fmt.ycbcr_enc

    @property
    def hsv_enc(self):
        return self._v4l2_fmt.hsv_enc

    @property
    def quantization(self):
        return self._v4l2_fmt.quantization

    @property
    def xfer_func(self):
        return self._v4l2_fmt.xfer_func


class V4l2PixFormatMplane(V4l2Format):
    def __init__(self, fmt, *args, **kwargs):
        super().__init__(fmt=fmt, *args, **kwargs)


class V4l2Window(V4l2Format):
    def __init__(self, fmt, *args, **kwargs):
        super().__init__(fmt=fmt, *args, **kwargs)


class V4l2VbiFormat(V4l2Format):
    def __init__(self, fmt, *args, **kwargs):
        super().__init__(fmt=fmt, *args, **kwargs)


class V4l2SlicedVbiFormat(V4l2Format):
    def __init__(self, fmt, *args, **kwargs):
        super().__init__(fmt=fmt, *args, **kwargs)


class V4l2SdrFormat(V4l2Format):
    def __init__(self, fmt, *args, **kwargs):
        super().__init__(fmt=fmt, *args, **kwargs)


class V4l2MetaFormat(V4l2Format):
    _repr_attrs_ = ("buffer_size", )

    def _to_v4l2(self):
        return V4l2IoctlFormatUnion(meta=self._v4l2_meta_fmt)

    @property
    def _data_format(self):
        return self._v4l2_meta_fmt.dataformat

    @property
    def buffer_size(self):
        # Only set by the driver.
        return self._v4l2_meta_fmt.buffersize

    def _update_format(self, fmt=None):
        if not fmt:
            if not hasattr(self, "_v4l2_meta_fmt"):
                self._v4l2_meta_fmt = V4l2IoctlMetaFormat()
            fmt = self._device._ioc_ops.get_format(type=self.buffer_type,
                                                   fmt=self._to_v4l2())
        # V4l2IoctlMetaFormat
        self._v4l2_meta_fmt = fmt.fmt.meta

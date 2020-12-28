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
from .ioctls import V4l2Formats, V4l2FormatDescFlags, IoctlError
from .v4l2frame import V4l2FrameSize


class V4l2Format(object):
    """The v4l2 format information."""
    def __init__(self, ioc_ops, fmt_desc):
        self._ioc_ops = ioc_ops
        self._fmt_desc = fmt_desc

    @property
    def format(self):
        "The format type (see :class:`V4l2Formats`)."
        return V4l2Formats(self._fmt_desc.pixelformat)

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
                frm_size = self._ioc_ops.enum_frame_sizes(
                    index=fr_idx,
                    pixel_format=self._fmt_desc.pixelformat)
            except IoctlError:
                break
            else:
                yield V4l2FrameSize(self._ioc_ops, frm_size)
            fr_idx += 1

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return ("V4l2Format(format={fmt}, description={desc}, flags={flgs})"
                ).format(fmt=self.format.name,
                         desc=self.description,
                         flgs=self.flags)

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
from .v4l2types import V4l2Fraction
from .ioctls import V4l2Formats, V4l2FrameSizeTypes, V4l2FrameIvalTypes
from abc import ABC, abstractmethod


class V4l2FrameInterval(object):
    """The v4l2 frame interval."""
    def __init__(self, frame_ival):
        self._frame_ival = frame_ival

    @property
    def type(self):
        """The frame interval type (see :class:`V4l2FrameIvalTypes`)
        (read-only).
        """
        return V4l2FrameIvalTypes(self._frame_ival.type)

    @property
    def interval(self):
        """The frame interval (read-only).

        Note:
            In case of a discrete interval, this is a V4l2Fraction.
            In case of a stepwise or coninuous interval, this is a tuple of
            fractions of the form (min, max, step).
        """
        if self.type == V4l2FrameIvalTypes.DISCRETE:
            return V4l2Fraction(self._frame_ival.discrete)
        else:
            return (V4l2Fraction(self._frame_ival.stepwise.min),
                    V4l2Fraction(self._frame_ival.stepwise.max),
                    V4l2Fraction(self._frame_ival.stepwise.step),
                    )

    def __repr__(self):
        return ("V4l2FrameInterval(type={typ}, interval={interval})"
                ).format(typ=self.type.name, interval=self.interval)


class V4l2FrameSize(ABC):
    """The v4l2 frame size.

    Note:
        This is an abstract base class. When instantiated, it will instead
        return an instance of the correct child class according to the size
        type.
        See :class:`V4l2DiscreteFrameSize` and :class:`V4l2StepwiseFrameSize`
        for the concrete implementation.
    """
    def __new__(cls, ioc_ops, frame_size):
        if frame_size.type == V4l2FrameSizeTypes.DISCRETE:
            return super().__new__(V4l2DiscreteFrameSize)
        else:
            return super().__new__(V4l2StepwiseFrameSize)

    def __init__(self, ioc_ops, frame_size):
        self._ioc_ops = ioc_ops
        self._frame_size = frame_size

    @property
    def format(self):
        "The format type (see :class:`V4l2Formats`) (read-only)."
        return V4l2Formats(self._frame_size.pixel_format)

    @property
    def type(self):
        "The frame size type (see :class:`V4l2FrameSizeTypes`) (read-only)."
        return V4l2FrameSizeTypes(self._frame_size.type)

    def __repr__(self):
        return ("V4l2FrameSize(format={fmt}, type={typ}, size={w}x{h})"
                ).format(fmt=self.format.name,
                         typ=self.type.name,
                         w=self.width,
                         h=self.height,
                         )

    @abstractmethod
    def intervals(self):
        """A generator function that yiels the available intervals for this
        format and size."""
        raise NotImplementedError("This class is not meant to be instantiated")

    @property
    @abstractmethod
    def width(self):
        """The frame width (read-only).

        Note:
            In case of a discrete size, this is an integral value.
            In case of a stepwise or coninuous size, this is a tuple of the
            form (min, max, step).
        """
        raise NotImplementedError("This class is not meant to be instantiated")

    @property
    @abstractmethod
    def height(self):
        """The frame height (read-only).

        Note:
            In case of a discrete size, this is an integral value.
            In case of a stepwise or coninuous size, this is a tuple of the
            form (min, max, step).
        """
        raise NotImplementedError("This class is not meant to be instantiated")


class V4l2DiscreteFrameSize(V4l2FrameSize):
    """The v4l2 discrete frame size."""
    @property
    def width(self):
        """The frame width (read-only)."""
        return self._frame_size.discrete.width

    @property
    def height(self):
        """The frame height (read-only)."""
        return self._frame_size.discrete.height

    def intervals(self):
        """A generator function that yiels the available intervals for this
        format and size."""
        ival_idx = 0
        while ival_idx < 2**32:
            try:
                frm_ival = self._ioc_ops.enum_frame_intervals(
                    index=ival_idx,
                    pixel_format=self._frame_size.pixel_format,
                    width=self.width,
                    height=self.height,
                    )
            except OSError:
                break
            else:
                yield V4l2FrameInterval(frm_ival)
            ival_idx += 1


class V4l2StepwiseFrameSize(V4l2FrameSize):
    """The v4l2 stepwise/continuous frame size."""
    @property
    def width(self):
        "The frame width as a tuple of the form (min, max, step) (read-only)."
        return (self._frame_size.stepwise.min_width,
                self._frame_size.stepwise.max_width,
                self._frame_size.stepwise.step_width)

    @property
    def height(self):
        "The frame height as a tuple of the form (min, max, step) (read-only)."
        return (self._frame_size.stepwise.min_height,
                self._frame_size.stepwise.max_height,
                self._frame_size.stepwise.step_height)

    def intervals(self):
        """A generator function that yiels the available intervals for this
        format and size."""
        frame_width = self.width
        frame_height = self.height
        for width in range(frame_width[0],
                           frame_width[1]+1,
                           frame_width[2]):
            for height in range(frame_height[0],
                                frame_height[1]+1,
                                frame_height[2]):
                try:
                    frm_ival = self._ioc_ops.enum_frame_intervals(
                        index=0,
                        pixel_format=self._frame_size.pixel_format,
                        width=width,
                        height=height,
                        )
                except OSError:
                    # Actually not supposed to happen, because one interval is
                    # supported per size, so let's just continue.
                    continue
                else:
                    yield V4l2FrameInterval(frm_ival)

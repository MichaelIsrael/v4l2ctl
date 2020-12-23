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
from fractions import Fraction
from dataclasses import dataclass
from .ioctls.v4l2ioctlstructs import V4l2IoctlRect


class V4l2Fraction(Fraction):
    @classmethod
    def _from_v4l2(cls, v4l2_frac):
        return cls(v4l2_frac.numerator, v4l2_frac.denominator)


@dataclass(frozen=True)
class V4l2Area(object):
    width: int
    height: int

    @classmethod
    def _from_v4l2(cls, v4l2_area):
        return cls(v4l2_area.width, v4l2_area.height)


@dataclass(frozen=True)
class V4l2Rectangle:
    left: int
    top: int
    area: V4l2Area

    @classmethod
    def _from_v4l2(cls, v4l2_rect):
        return cls(v4l2_rect.left,
                   v4l2_rect.top,
                   V4l2Area(v4l2_rect.width, v4l2_rect.height),
                   )

    def _to_v4l2(self):
        return V4l2IoctlRect(
                   left=self.left,
                   top=self.top,
                   width=self.area.width,
                   height=self.area.height,
                   )


@dataclass(frozen=True)
class V4l2CroppingCapabilities:
    bounds: V4l2Rectangle
    default: V4l2Rectangle
    pixel_aspect: V4l2Fraction

    @classmethod
    def _from_v4l2(cls, v4l2_cropcap):
        return cls(V4l2Rectangle._from_v4l2(v4l2_cropcap.bounds),
                   V4l2Rectangle._from_v4l2(v4l2_cropcap.defrect),
                   V4l2Fraction._from_v4l2(v4l2_cropcap.pixelaspect),
                   )

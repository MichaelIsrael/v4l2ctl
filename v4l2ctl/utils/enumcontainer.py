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
from itertools import chain
from enum import EnumMeta


class MetaEnumContainer(type):
    def __iter__(cls):
        return chain.from_iterable(cls._enums)

    def __contains__(cls, item):
        for sub in cls._enums:
            if item in sub:
                return True
        else:
            return False

    def __getattr__(cls, attr):
        for sub_enum in super().__getattribute__("_enums"):
            if hasattr(sub_enum, attr):
                return getattr(sub_enum, attr)
        else:
            raise AttributeError(attr)

    def __getitem__(cls, item):
        try:
            return getattr(cls, item)
        except AttributeError:
            raise KeyError(item) from None


class BaseEnumContainer(metaclass=MetaEnumContainer):
    def __init_subclass__(cls, enums, **kwargs):
        if type(enums) is EnumMeta:
            cls._enums = [enums]
        else:
            for enum in enums:
                if type(enum) is not EnumMeta:
                    raise TypeError(enum.__name__ + " is not an enum.")
            cls._enums = enums
        super().__init_subclass__(**kwargs)

    def __new__(cls, value):
        for sub_enum in cls._enums:
            try:
                return sub_enum(value)
            except ValueError:
                pass
        else:
            raise ValueError(str(value) + " is not a valid " + cls.__name__)

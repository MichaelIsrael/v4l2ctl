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
from enum import Enum, auto


class FileHandleStatus(Enum):
    Opened = auto()
    Closed = auto()
    ToBeClosed = auto()


class FileHandleCM(object):
    def __init__(self, filename, options={}):
        self._filename = filename
        self._options = options
        self._with_ref_count = 0
        self._open_ref_count = 0
        self._handle = None
        self._status = FileHandleStatus.Closed

    def _open_file(self):
        if not self._handle:
            self._handle = open(self._filename, **self._options)
        return self._handle

    def _close_file(self):
        if self._handle:
            self._handle.close()
            self._handle = None

    def __enter__(self):
        handle = self._open_file()
        if self._status == FileHandleStatus.Closed:
            self._status = FileHandleStatus.ToBeClosed
        self._with_ref_count += 1
        return handle

    def __exit__(self, exc_type, exc, tb):
        self._with_ref_count -= 1
        if self._with_ref_count == 0 and \
                self._status == FileHandleStatus.ToBeClosed:
            self._close_file()
            self._status = FileHandleStatus.Closed

    @property
    def filename(self):
        return self._filename

    @property
    def status(self):
        return self._status

    def fileno(self):
        return self._handle.fileno()

    def open(self):
        handle = self._open_file()
        self._status = FileHandleStatus.Opened
        self._open_ref_count += 1
        return handle

    def close(self):
        self._open_ref_count -= 1
        if self._with_ref_count != 0:
            self._status = FileHandleStatus.ToBeClosed
        elif self._open_ref_count == 0:
            self._status = FileHandleStatus.Closed
            self._close_file()

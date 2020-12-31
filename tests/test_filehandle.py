#!/usr/bin/env python3
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
from unittest import TestCase, main as run_tests
from pathlib import Path
import site

site.addsitedir(r".")  # For running with pytest
site.addsitedir(r"..")  # For executing this file as is.

from v4l2ctl.utils.filehandle import FileHandleCM, FileHandleStatus  # noqa E402


TEST_FILE = "/dev/zero"


def count_open_files(filename=TEST_FILE):
    own_fds = Path(r"/proc/self/fd")
    count = 0
    for f in own_fds.iterdir():
        if str(f.resolve()) == filename:
            count += 1
    return count


class FileHandleTest(TestCase):
    def test_simple_with(self):
        dev_han = FileHandleCM(TEST_FILE, {"mode": "w"})
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

        with dev_han as fd:
            self.assertEqual(dev_han.status, FileHandleStatus.ToBeClosed)
            self.assertEqual(count_open_files(), 1)
            fd.write("Foo")

        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

    def test_nested_with(self):
        dev_han = FileHandleCM(TEST_FILE, {"mode": "w"})
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

        with dev_han as fd1:
            fd1.write("Foo")
            self.assertEqual(dev_han.status, FileHandleStatus.ToBeClosed)
            self.assertEqual(count_open_files(), 1)

            with dev_han as fd2:
                self.assertEqual(fd1.fileno(), fd2.fileno())
                self.assertEqual(dev_han.status, FileHandleStatus.ToBeClosed)
                self.assertEqual(count_open_files(), 1)
                fd2.write("Foo")
                with dev_han as fd3:
                    self.assertEqual(fd1.fileno(), fd3.fileno())
                    self.assertEqual(dev_han.status,
                                     FileHandleStatus.ToBeClosed)
                    self.assertEqual(count_open_files(), 1)
                    fd3.write("Foo")
                self.assertEqual(dev_han.status, FileHandleStatus.ToBeClosed)
                self.assertEqual(count_open_files(), 1)
            self.assertEqual(dev_han.status, FileHandleStatus.ToBeClosed)
            self.assertEqual(count_open_files(), 1)
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

    def test_simple_open(self):
        dev_han = FileHandleCM(TEST_FILE, {"mode": "w"})
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

        fd = dev_han.open()
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        self.assertEqual(count_open_files(), 1)
        fd.write("Foo")

        dev_han.close()
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

    def test_several_open(self):
        dev_han = FileHandleCM(TEST_FILE, {"mode": "w"})
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

        fd1 = dev_han.open()
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        self.assertEqual(count_open_files(), 1)
        fd1.write("Foo")

        fd2 = dev_han.open()
        self.assertEqual(fd1.fileno(), fd2.fileno())
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        self.assertEqual(count_open_files(), 1)
        fd2.write("Foo")

        fd3 = dev_han.open()
        self.assertEqual(fd1.fileno(), fd3.fileno())
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        self.assertEqual(count_open_files(), 1)
        fd3.write("Foo")

        dev_han.close()
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        self.assertEqual(count_open_files(), 1)
        fd2.write("Foo")

        dev_han.close()
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        self.assertEqual(count_open_files(), 1)
        fd1.write("Foo")

        dev_han.close()
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

    def test_with_open(self):
        dev_han = FileHandleCM(TEST_FILE, {"mode": "w"})
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

        with dev_han as fd:
            self.assertEqual(dev_han.status, FileHandleStatus.ToBeClosed)
            self.assertEqual(count_open_files(), 1)
            fd.write("Foo")

            open_fd = dev_han.open()
            self.assertEqual(count_open_files(), 1)
            self.assertEqual(fd.fileno(), open_fd.fileno())
            self.assertEqual(dev_han.status, FileHandleStatus.Opened)
            open_fd.write("Foo")

        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        self.assertEqual(count_open_files(), 1)
        fd.write("Foo")

        dev_han.close()
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

    def test_open_with(self):
        dev_han = FileHandleCM(TEST_FILE, {"mode": "w"})
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

        fd_open = dev_han.open()
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        self.assertEqual(count_open_files(), 1)
        fd_open.write("Foo")

        with dev_han as fd_with:
            self.assertEqual(count_open_files(), 1)
            self.assertEqual(dev_han.status, FileHandleStatus.Opened)
            fd_with.write("Foo")

        self.assertEqual(count_open_files(), 1)
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        fd_open.write("Foo")

        dev_han.close()
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

    def tearDown(self):
        self.assertEqual(count_open_files(), 0)


class FileHandleErrorTest(TestCase):
    def test_overwrite_handle(self):
        dev_han = FileHandleCM(TEST_FILE, {"mode": "w"})
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

        fd_open = dev_han.open()
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        fd_open.write("Foo")
        self.assertEqual(count_open_files(), 1)

        dev_han = None
        fd_open.write("Foo")

    def test_delete_handle(self):
        dev_han = FileHandleCM(TEST_FILE, {"mode": "w"})
        self.assertEqual(dev_han.status, FileHandleStatus.Closed)
        self.assertEqual(count_open_files(), 0)

        fd_open = dev_han.open()
        self.assertEqual(dev_han.status, FileHandleStatus.Opened)
        fd_open.write("Foo")
        self.assertEqual(count_open_files(), 1)

        del dev_han
        fd_open.write("Foo")

    def tearDown(self):
        self.assertEqual(count_open_files(), 0)


if __name__ == "__main__":
    run_tests()

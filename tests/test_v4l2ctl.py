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
from unittest import TestCase, SkipTest, main as run_tests
import site
from v4l2ctlinterface import V4l2CtlInterface
from pathlib import Path

site.addsitedir(r".")  # For running with pytest
site.addsitedir(r"..")  # For executing this file as is.

from v4l2ctl import V4l2Device  # noqa E402


class CapabilitiesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            v4l2ctl_cli = V4l2CtlInterface()
        except FileNotFoundError:
            raise SkipTest("v4l2-ctl not found.") from None
        else:
            if len(v4l2ctl_cli) < 1:
                raise SkipTest("No video devices found on this system.")

    def test_basic_info(self):
        v4l2ctl_cli = V4l2CtlInterface()
        for device_file, device in v4l2ctl_cli.items():
            with self.subTest(device=device_file):
                vid = V4l2Device(device_file)
                self.assertIsInstance(vid, V4l2Device)

                with self.subTest(device=device_file, property="name"):
                    self.assertIn(device.name, vid.name)

                with self.subTest(device=device_file, property="driver"):
                    self.assertIn(device.driver, vid.driver)

                with self.subTest(device=device_file, property="bus"):
                    self.assertIn(device.bus, vid.bus)

                with self.subTest(device=device_file, property="version"):
                    self.assertEqual(device.version, vid.version)

                with self.subTest(device=device_file, property="capabilities"):
                    self.assertEqual(device.capabilities, vid.capabilities)

                with self.subTest(device=device_file,
                                  property="physical_capabilities"):
                    self.assertEqual(device.physical_capabilities,
                                     vid.physical_capabilities,
                                     )


class DeviceListTest(TestCase):
    # For now only one test case is present, because testing the skipping of
    # links without workarounds or hacks will require root-permissions and we
    # surely don't want that here.
    def test_list(self):
        try:
            v4l2ctl_cli = V4l2CtlInterface()
        except FileNotFoundError:
            raise SkipTest("v4l2-ctl not found.") from None
        else:
            auto_list = map(lambda x: str(x.device),
                            V4l2Device.iter_devices(False))
            self.assertEqual(set(v4l2ctl_cli.keys()), set(auto_list))


class IOInterfaceTest(TestCase):
    """Tests for the I/O interface."""

    def test_context_management(self):
        """Test with statement"""
        for device in V4l2Device.iter_devices():
            self.assertTrue(device.closed)
            with device as device:
                self.assertFalse(device.closed)
            self.assertTrue(device.closed)

    def test_close(self):
        """Test V4l2Device.close()"""
        for device in V4l2Device.iter_devices():
            self.assertTrue(device.closed)
            with device as device:
                self.assertFalse(device.closed)
                device.close()
                self.assertTrue(device.closed)
            self.assertTrue(device.closed)

    def test_io_interface(self):
        """Test the IOBase interface"""
        for device in V4l2Device.iter_devices():
            with device as device:
                self.assertTrue(hasattr(device, "seek"))
                self.assertTrue(hasattr(device, "truncate"))
                self.assertTrue(hasattr(device, "flush"))
                self.assertTrue(hasattr(device, "readline"))
                self.assertTrue(hasattr(device, "readlines"))
                self.assertTrue(hasattr(device, "tell"))
                self.assertTrue(hasattr(device, "writelines"))
                self.assertTrue(hasattr(device, "readable"))
                self.assertTrue(hasattr(device, "writable"))
                self.assertTrue(hasattr(device, "seekable"))
                self.assertTrue(hasattr(device, "isatty"))
                self.assertTrue(hasattr(device, "fileno"))
                self.assertTrue(hasattr(device, "close"))
                self.assertTrue(hasattr(device, "closed"))

    def test_io_features(self):
        """Test the IO features
        For the purpose of this test, it doesn't matter if a feature is
        supported or not, just that the interface is implemented, i.e., the
        method exists and returns a appropriate value.
        """
        for device in V4l2Device.iter_devices():
            with device as device:
                self.assertIsInstance(device.readable(), bool)
                self.assertIsInstance(device.writable(), bool)
                self.assertIsInstance(device.seekable(), bool)
                self.assertIsInstance(device.isatty(), bool)

    def test_fileno(self):
        """Test V4l2Device.fileno()"""
        for device in V4l2Device.iter_devices():
            with device as device:
                self.assertIsInstance(device.fileno(), int)
                # Make sure fileno() returns the right fd.
                self.assertEqual(device.device,
                                 Path(r"/proc/self/fd/").joinpath(
                                     str(device.fileno())).resolve()
                                 )


if __name__ == "__main__":
    run_tests()

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
from pathlib import Path
import subprocess
import site

site.addsitedir(r".")  # For running with pytest
site.addsitedir(r"..")  # For executing this file as is.

from v4l2ctl import V4l2Device  # noqa E402


class V4l2CtlInfo(dict):
    """Helper class to parse v4l2-ctl's output. Might be removed in the future.
    """
    def __init__(self, output):
        super().__init__()

        if isinstance(output, bytes):
            output = output.decode().splitlines()

        # info = []
        while(output):
            line = output.pop(0)
            attrs = line.split(":")
            level = 0
            while attrs[0][0] == "\t":
                level += 1
                attrs[0] = attrs[0][1:]
            attrs[0] = attrs[0].strip()
            # For now!
            try:
                self[attrs[0]] = attrs[1].strip()
            except IndexError:
                # Ignore also for now.
                pass


class CapabilitiesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.video_devices = {}

        # Collect all /dev/video* devices.
        video_devices = list(Path(r"/dev").glob(r"video*"))

        # If none were found, skip test.
        if not video_devices:
            raise SkipTest("No video devices found on this system.")

        for dev in video_devices:
            try:
                proc = subprocess.run(["v4l2-ctl", "-D", "-d", dev],
                                      check=True,
                                      capture_output=True,
                                      )
                cls.video_devices[dev] = V4l2CtlInfo(proc.stdout)
            except FileNotFoundError:
                raise SkipTest("v4l2-ctl not found.") from None

    def test_basic_info(self):
        for device, info in self.video_devices.items():
            with self.subTest(device=device):
                vid = V4l2Device(device)
                self.assertIsInstance(vid, V4l2Device)

                with self.subTest(device=device, property="name"):
                    self.assertIn(info["Card type"], vid.name)

                with self.subTest(device=device, property="driver"):
                    self.assertIn(info["Driver name"], vid.driver)

                with self.subTest(device=device, property="bus"):
                    self.assertIn(info["Bus info"], vid.bus)

                with self.subTest(device=device, property="version"):
                    self.assertEqual(vid.version, info["Driver version"])

                with self.subTest(device=device, property="capabilities"):
                    self.assertEqual(vid.capabilities,
                                     int(info["Device Caps"], 16),
                                     )

                with self.subTest(device=device,
                                  property="physical_capabilities"):
                    self.assertEqual(vid.physical_capabilities,
                                     int(info["Capabilities"], 16),
                                     )


class DeviceListTest(TestCase):
    # For now only one test case is present, because testing the skipping of
    # links without workarounds or hacks will require root-permissions and we
    # surely don't want that here.
    def test_all(self):
        manual_list = []
        for dev_file in Path(r"/dev").glob(r"*"):
            if dev_file.is_dir():
                continue
            try:
                V4l2Device(dev_file)
            except Exception:
                pass
            else:
                manual_list.append(dev_file)

        auto_list = map(lambda x: x.device, V4l2Device.iter_devices(False))

        self.assertEqual(set(manual_list), set(auto_list))


if __name__ == "__main__":
    run_tests()

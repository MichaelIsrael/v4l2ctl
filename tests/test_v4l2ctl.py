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
import site

site.addsitedir(r".")  # For running with pytest
site.addsitedir(r"..")  # For executing this file as is.

from v4l2ctl import V4l2Device  # noqa E402


class CapabilitiesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # Collect all /dev/video* devices.
        cls.video_devices = list(Path(r"/dev").glob(r"video*"))
        # If none were found, skip test.
        if not cls.video_devices:
            raise SkipTest("No video devices found on this system.")

    def test_basic(self):
        for device in self.video_devices:
            with self.subTest(device=device):
                vid = V4l2Device(device)
                self.assertIsInstance(vid, V4l2Device)

                # print(vid.name)
                # print(vid.driver)
                # print(vid.bus)
                # print(vid.version)
                # print(repr(vid.capabilities))
                # print(repr(vid.physical_capabilities))


if __name__ == "__main__":
    run_tests()

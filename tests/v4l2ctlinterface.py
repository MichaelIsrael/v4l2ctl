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
import subprocess


class V4l2CtlInterface(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _, output = self._v4l2_ctrl("--list-devices")
        self._dev_lst = [dev.strip() for dev in output
                         if self._is_valid_device(dev)]

    def _is_valid_device(self, dev):
        dev = dev.strip()
        if not dev.startswith("/dev/"):
            return False
        ret, _ = self._v4l2_ctrl("-d", dev, "-k")
        if ret != 0:
            return False
        return True

    @staticmethod
    def _v4l2_ctrl(*args):
        proc = subprocess.run(["v4l2-ctl", *args],
                              # capture_output=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              encoding="utf-8",
                              )
        return proc.returncode, proc.stdout.splitlines()

    class V4l2CtlDeviceInterface(object):
        def __init__(self, device):
            self._device = device
            self._read_infos()

        def _read_infos(self):
            ret, output = V4l2CtlInterface._v4l2_ctrl("-D", "-d", self._device)

            self._info = {}
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
                    self._info[attrs[0]] = attrs[1].strip()
                except IndexError:
                    # Ignore also for now.
                    pass

        @property
        def name(self):
            return self._info["Card type"]

        @property
        def driver(self):
            return self._info["Driver name"]

        @property
        def bus(self):
            return self._info["Bus info"]

        @property
        def version(self):
            return self._info["Driver version"]

        @property
        def capabilities(self):
            return int(self._info["Device Caps"], 16)

        @property
        def physical_capabilities(self):
            return int(self._info["Capabilities"], 16)

    @property
    def devices(self):
        for dev in self._dev_lst:
            yield self.V4l2CtlDeviceInterface(dev)

    def values(self):
        return self.devices

    def __getitem__(self, key):
        if key not in self._dev_lst:
            raise KeyError(key)
        return self.V4l2CtlDeviceInterface(key)

    def items(self):
        for dev in self._dev_lst:
            yield dev, self.V4l2CtlDeviceInterface(dev)

    def keys(self):
        return iter(self._dev_lst)

    def __len__(self):
        return len(self._dev_lst)

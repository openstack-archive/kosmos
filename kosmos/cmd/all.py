# Copyright 2015 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import sys

from oslo_config import cfg
from oslo_service import service

from kosmos.engine import service as engine
from kosmos.conductor import service as conductor
from kosmos.common import config
from kosmos.common import utils

CONF = cfg.CONF


def main():
    utils.read_config('kosmos', sys.argv)
    config.setup_logging(CONF)

    process_launcher = service.ProcessLauncher(CONF)
    process_launcher.launch_service(engine.Service())
    process_launcher.launch_service(conductor.Service())
    process_launcher.wait()

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
from oslo_service.wsgi import Loader

from kosmos.engine import service as engine
from kosmos.conductor import service as conductor
from kosmos.api import service as api
from kosmos.common import config

CONF = cfg.CONF


def main():

    config.setup_logging(CONF)
    config.init(sys.argv)

    process_launcher = service.ProcessLauncher(CONF)
    process_launcher.launch_service(
        engine.Service(threads=CONF['service:engine'].threads),
        workers=CONF['service:engine'].workers
    )
    process_launcher.launch_service(
        conductor.Service(threads=CONF['service:conductor'].threads),
        workers=CONF['service:conductor'].workers)

    process_launcher.launch_service(
        api.Service(
            CONF,
            'API',
            Loader(CONF).load_app('kosmos'),
            host=CONF['service:api'].bind_host,
            port=CONF['service:api'].bind_port
        ),

        workers=CONF['service:api'].workers)

    process_launcher.wait()

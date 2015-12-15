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
from oslo_config import cfg
import oslo_messaging as messaging
from oslo_log import log as logging

from kosmos import service


LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Service(service.RPCService, service.Service):
    """
    API version history:

        1.0 - Initial version
    """
    RPC_API_VERSION = '2.0'

    target = messaging.Target(version=RPC_API_VERSION)

    @property
    def service_name(self):
        return 'engine'

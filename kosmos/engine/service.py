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

from kosmos.db import api as db_api
from kosmos import service
from kosmos import context
from kosmos import objects

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Service(service.RPCService, service.Service):
    """
    API version history:

        1.0 - Initial version
    """
    RPC_API_VERSION = '1.0'

    target = messaging.Target(version=RPC_API_VERSION)

    @property
    def service_name(self):
        return 'engine'

    def start(self):
        objects.register_all()
        db = db_api.get_instance()
        LOG.info(db.get_loadbalancers(context.KosmosContext()))
        LOG.info(db.get_loadbalancer_by_id(
            context.KosmosContext(),
            "3e3f2faa-dbb8-4c18-ac0d-3d766455ebd6")[0])

        LOG.info(objects.load_balancer.LoadBalancer.get_by_id(
            context.KosmosContext(),
                                                  "3e3f2faa-dbb8-4c18-ac0d-3d766455ebd6"))

        LOG.info(objects.load_balancer.LoadBalancer.find(
            context.KosmosContext(),{'fqdn': '%test.domain.tld.'}))

        super(Service, self).start()




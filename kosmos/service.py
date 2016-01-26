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
import abc
import oslo_messaging as messaging
import six
from kosmos import policy
from kosmos import version
from kosmos._i18n import _
from kosmos.common import rpc
from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service


CONF = cfg.CONF

LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class Service(service.Service):
    """
    Service class to be shared inside Kosmos
    """
    def __init__(self, threads=None):
        threads = threads or 1000

        super(Service, self).__init__(threads)

        self._host = CONF.host
        self._service_config = CONF['service:%s' % self.service_name]

        policy.init()

        if not rpc.initialized():
            rpc.init(CONF)

    @abc.abstractproperty
    def service_name(self):
        pass

    def start(self):
        super(Service, self).start()

        LOG.info(_('Starting %(name)s service (version: %(version)s)'),
                 {'name': self.service_name,
                  'version': version.version_info.version_string()})

    def stop(self):
        LOG.info(_('Stopping %(name)s service'), {'name': self.service_name})

        super(Service, self).stop()


class RPCService(object):
    """
    RPC Service mixin used by all Kosmos RPC Servers
    """
    def __init__(self, *args, **kwargs):
        super(RPCService, self).__init__(*args, **kwargs)

        LOG.debug("Creating RPC Server on topic '%s'" % self._rpc_topic)
        self._rpc_server = rpc.get_server(
            messaging.Target(topic=self._rpc_topic, server=self._host),
            self._rpc_endpoints)

    @property
    def _rpc_endpoints(self):
        return [self]

    @property
    def _rpc_topic(self):
        return self.service_name

    def start(self):
        super(RPCService, self).start()

        LOG.debug("Starting RPC server on topic '%s'" % self._rpc_topic)
        self._rpc_server.start()

        # TODO(kiall): This probably belongs somewhere else, maybe the base
        #              Service class?
        self.notifier = rpc.get_notifier(self.service_name)

        for e in self._rpc_endpoints:
            if e != self and hasattr(e, 'start'):
                e.start()

    def stop(self):
        LOG.debug("Stopping RPC server on topic '%s'" % self._rpc_topic)

        for e in self._rpc_endpoints:
            if e != self and hasattr(e, 'stop'):
                e.stop()

        # Try to shut the connection down, but if we get any sort of
        # errors, go ahead and ignore them.. as we're shutting down anyway
        try:
            self._rpc_server.stop()
        except Exception:
            pass

        super(RPCService, self).stop()

    def wait(self):
        for e in self._rpc_endpoints:
            if e != self and hasattr(e, 'wait'):
                e.wait()

        super(RPCService, self).wait()

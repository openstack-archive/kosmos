# Copyright 2011 VMware, Inc., 2014 A10 Networks
# Copyright 2015 Hewlett Packard Enterprise Development LP
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Routines for configuring Kosmos
"""
import os

from oslo_config import cfg
from oslo_db import options as db_options
from oslo_log import log as logging
import oslo_messaging as messaging

from kosmos._i18n import _, _LI
from kosmos.common import utils
from kosmos import version

LOG = logging.getLogger(__name__)

core_opts = [
    cfg.IPOpt('bind_host', default='0.0.0.0',
              help=_("The host IP to bind to")),
    cfg.PortOpt('bind_port', default=9876,
                help=_("The port to bind to")),
    cfg.StrOpt('host', default=utils.get_hostname(),
               help=_("The hostname Kosmos is running on")),
]

core_cli_opts = []


# Register the configuration options
cfg.CONF.register_opts(core_opts)
cfg.CONF.register_cli_opts(core_cli_opts)


# Ensure that the control exchange is set correctly
messaging.set_transport_defaults(control_exchange='kosmos')
_SQL_CONNECTION_DEFAULT = 'sqlite://'
# Update the default QueuePool parameters. These can be tweaked by the
# configuration variables - max_pool_size, max_overflow and pool_timeout
db_options.set_defaults(cfg.CONF,
                        connection=_SQL_CONNECTION_DEFAULT,
                        sqlite_db='', max_pool_size=10,
                        max_overflow=20, pool_timeout=10)

logging.register_options(cfg.CONF)


def init(args):
    config_files = find_config('kosmos.conf')
    cfg.CONF(args=args[1:], project='kosmos',
             version='%%prog %s' % version.version_info.release_string(),
             default_config_files=config_files)


def setup_logging(conf):
    """Sets up the logging options for a log with supplied name.

    :param conf: a cfg.ConfOpts object
    """
    product_name = "kosmos"
    logging.setup(conf, product_name)
    LOG.info(_LI("Logging enabled!"))


def find_config(config_path):
    """
    Find a configuration file using the given hint.

    Code nabbed from cinder, by designate, then nabbed from designate

    :param config_path: Full or relative path to the config.
    :returns: List of config paths
    """
    possible_locations = [
        config_path,
        os.path.join(cfg.CONF.pybasedir, "etc", "kosmos", config_path),
        os.path.join(cfg.CONF.pybasedir, "etc", config_path),
        os.path.join(cfg.CONF.pybasedir, config_path),
        "/etc/kosmos/%s" % config_path,
    ]

    found_locations = []

    for path in possible_locations:
        LOG.debug('Searching for configuration at path: %s' % path)
        if os.path.exists(path):
            LOG.debug('Found configuration at path: %s' % path)
            found_locations.append(os.path.abspath(path))

    return found_locations


def read_config(prog, argv):
    logging.register_options(cfg.CONF)
    config_files = find_config('%s.conf' % prog)
    cfg.CONF(argv[1:], project='kosmos', prog=prog,
             default_config_files=config_files)

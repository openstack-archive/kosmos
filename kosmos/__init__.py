# -*- coding: utf-8 -*-

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
import os

import pbr.version
from oslo_config import cfg


__version__ = pbr.version.VersionInfo(
    'kosmos').version_string()


cfg.CONF.register_opts([
    cfg.StrOpt(
        'pybasedir',
        default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../')),
        help='Directory where the kosmos python module is installed'
    ),
    cfg.StrOpt('state-path', default='/var/lib/kosmos',
               help='Top-level directory for maintaining kosmos\'s state'),
])

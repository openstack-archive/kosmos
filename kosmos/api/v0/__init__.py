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
from pecan import deploy


def factory(global_config, **local_conf):
    conf = {
        'app': {
            'root': 'kosmos.api.v0.controllers.root.RootController',
            'modules': ['kosmos.api.v0'],
            'errors': {
                404: '/errors/not_found',
                405: '/errors/method_not_allowed',
                '__force_dict__': True
            }
        }
    }

    app = deploy.deploy(conf)

    return app

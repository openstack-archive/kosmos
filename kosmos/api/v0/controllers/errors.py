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
from pecan import expose
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class ErrorsController(object):

    @expose('json')
    def not_found(self):
        return dict(status=404, message="not_found")

    @expose('json')
    def method_not_allowed(self):
        return dict(status=404, message="method_not_allowed")

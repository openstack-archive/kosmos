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
import copy

from oslo_context import context
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class KosmosContext(context.RequestContext):

    def __init__(self, auth_token=None, user=None, tenant=None, domain=None,
                 user_domain=None, project_domain=None, is_admin=False,
                 read_only=False, show_deleted=False, request_id=None,
                 resource_uuid=None, overwrite=True, roles=None,
                 service_catalog=None):

        # NOTE: user_identity may be passed in, but will be silently dropped as
        #       it is a generated field based on several others.
        super(KosmosContext, self).__init__(
            auth_token=auth_token,
            user=user,
            tenant=tenant,
            domain=domain,
            user_domain=user_domain,
            project_domain=project_domain,
            is_admin=is_admin,
            read_only=read_only,
            show_deleted=show_deleted,
            request_id=request_id,
            resource_uuid=resource_uuid,
            overwrite=overwrite)

        self.roles = roles or []
        self.service_catalog = service_catalog

    def deepcopy(self):
        d = self.to_dict()
        return self.from_dict(d)

    def to_dict(self):
        d = super(KosmosContext, self).to_dict()
        return copy.deepcopy(d)

    @classmethod
    def from_dict(cls, values):
        return cls(**values)


def get_current():
    return context.get_current()

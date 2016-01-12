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

from kosmos._i18n import _
from kosmos.objects import base
from kosmos.objects import fields


class LoadBalancerStatus(fields.StateMachineEnforce,
                         fields.PreDefinedEnumType):

    ACTIVE = 'ACTIVE'
    PENDING = 'PENDING'
    ERROR = 'ERROR'
    DELETED = 'DELETED'

    ALLOWED_TRANSITIONS = {
        ACTIVE: {
            ERROR,
            PENDING,
            DELETED
        },
        PENDING: {
            ACTIVE,
            ERROR,
            DELETED
        },
        ERROR: {
            PENDING,
            ACTIVE,
            DELETED
        },
        DELETED: {}
    }

    _TYPES = (ACTIVE, PENDING, ERROR, DELETED)

    _msg = _("'%(value)s' is not a valid status, choose from %(options)r")


@base.VersionedObjectRegistry.register
class LoadBalancer(base.KosmosObject, base.KosmosOwnedObject,
                   base.KosmosPersistentObject):

    VERSION = '1.0'

    fields = {
        'name': fields.StringField(),
        'description': fields.StringField(nullable=True),
        'fqdn': fields.DNSFQDN(),
        'zone_name': fields.DNSZoneName(),
        'flavor': fields.UUIDField(),
        'appliance_id': fields.StringField(),
        'pool': fields.ObjectField('Pool'),
        'status': LoadBalancerStatus(),
        'action': fields.KosmosActions(),
    }

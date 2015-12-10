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


class PoolMemberStatus(fields.StateMachineEnforce, fields.PreDefinedEnumType):

    ACTIVE = 'active'
    PENDING = 'pending'
    DEGRADED = 'degraded'
    DOWN = 'down'
    ERROR = 'error'
    DELETED = 'deleted'

    ALLOWED_TRANSITIONS = {
        ACTIVE: {
            DEGRADED,
            DOWN,
            ERROR,
            PENDING,
            DELETED
        },
        PENDING: {
            ACTIVE,
            ERROR,
            DELETED
        },
        DEGRADED: {
            ERROR,
            ACTIVE,
            DELETED
        },
        DOWN: {
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

    _TYPES = (ACTIVE, PENDING, DEGRADED, DOWN, ERROR, DELETED)
    _msg = _("'%(value)s' is not a valid status, choose from %(options)r")


@base.VersionedObjectRegistry.register
class PoolMember(base.KosmosObject, base.KosmosOwnedObject,
                 base.KosmosPersistentObject):

    VERSION = '1.0'

    fields = {
        'name': fields.StringField(),
        'description': fields.StringField(nullable=True),
        'type': fields.PoolMemberType(nullable=False),
        'parameters': fields.ListOfObjectsField(
            'PoolMemberParameter',
            default=[]),
        'status': PoolMemberStatus(),
        'action': fields.KosmosActions(),
    }

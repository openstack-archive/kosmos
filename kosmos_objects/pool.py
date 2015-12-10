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
from kosmos_objects import base
from kosmos_objects import fields


class PoolStatus(fields.StateMachineEnforce, fields.PreDefinedEnumType):

    ACTIVE = 'active'
    PENDING = 'pending'
    DEGRADED = 'degraded'
    DOWN = 'down'
    ERROR = 'error'

    ALLOWED_TRANSITIONS = {
        ACTIVE: {
            DEGRADED,
            DOWN,
            ERROR,
            PENDING
        },
        PENDING: {
            ACTIVE,
            ERROR
        },
        DEGRADED: {
            ERROR,
            ACTIVE
        },
        DOWN: {
            ACTIVE,
            ERROR
        },
        ERROR: {
            PENDING,
            ACTIVE
        }
    }

    _TYPES = (ACTIVE, PENDING, DEGRADED, DOWN, ERROR)

    _msg = _("'%(value)s' is not a valid status, choose from %(options)r")


@base.VersionedObjectRegistry.register
class Pool(base.KosmosObject, base.KosmosOwnedObject,
           base.KosmosPersistentObject):

    VERSION = '1.0'

    fields = {
        'name': fields.StringField(),
        'description': fields.StringField(nullable=True),
        'members': fields.ListOfObjectsField(
            'PoolMember',
            default=[]),
        'status': PoolStatus(),
        'action': fields.KosmosActions(),
    }

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

from oslo_log import log as logging
from oslo_versionedobjects import base as ovoo_base
from kosmos.objects import fields
from kosmos import objects

LOG = logging.getLogger('object')


class VersionedObjectRegistry(ovoo_base.VersionedObjectRegistry):
    def registration_hook(self, cls, index):
        setattr(objects, cls.obj_name(), cls)


class KosmosObject(ovoo_base.VersionedObject):
    """Base class and object factory.
    This forms the base of all objects that can be remoted or instantiated
    via RPC. Simply defining a class that inherits from this base class
    will make it remotely instantiatable. Objects should implement the
    necessary "get" classmethod routines as well as "save" object methods
    as appropriate.
    """

    OBJ_PROJECT_NAMESPACE = 'kosmos'

    DB_TABLE = ''


class KosmosOwnedObject(object):
    """Mixin class for objects owned by users.
    This adds the fields that we use in common for most object ownership.
    """
    fields = {
        'project_id': fields.StringField(),
        'domain_id': fields.StringField(),
    }


class KosmosPersistentObject(object):
    """Mixin class for Persistent objects.
    This adds the fields that we use in common for most persistent objects.
    """
    fields = {
        'id': fields.UUIDField(read_only=True),
        'version': fields.IntegerField(read_only=True),
        'created_at': fields.DateTimeField(nullable=True),
        'updated_at': fields.DateTimeField(nullable=True),
        'deleted_at': fields.DateTimeField(nullable=True),
        'deleted': fields.BooleanField(default=False),
    }

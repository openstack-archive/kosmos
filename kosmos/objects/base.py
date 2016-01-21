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
import six

from oslo_log import log as logging
from oslo_versionedobjects import base as ovoo_base
from kosmos.objects import fields
from kosmos import objects
from kosmos.db import api as db_api
import sqlalchemy.exc as exc

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

    @classmethod
    def get_by_id(cls, context, id):
        db = db_api.get_instance()
        db_rs = db.get_object_by_id(context, cls.DB_TABLE, id)

        return cls._sqla_to_obj(db_rs)


    @classmethod
    def find(cls, context, criterion):
        db = db_api.get_instance()
        db_rs = db.find_objects(context, cls.DB_TABLE, criterion)

        items = []

        for rs in db_rs:
            items.append(cls._sqla_to_obj(rs))

        return items


    @classmethod
    def _sqla_to_obj(cls, rs):
        obj = cls()

        for field in six.iterkeys(obj.fields):
            try:
                obj.__setattr__(field, rs[field])
            except exc.NoSuchColumnError:
                if '%s_id' % field in rs:
                    inner_cls = objects.base.KosmosObject.obj_class_from_name(
                            'Pool', '1.0')
                    if issubclass(inner_cls, fields.ObjectField):
                        inner_obj \
                            = inner_cls.get_by_id(rs['%s_id' % field])
                        obj.__setattr__(field, inner_obj)

        return obj


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

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
from kosmos_objects import base
from kosmos_objects import fields
import kosmos_objects as objects


@base.VersionedObjectRegistry.register
class Monitor(base.KosmosObject, base.KosmosOwnedObject,
              base.KosmosPersistentObject):

    VERSION = '1.0'

    fields = {
        'name': fields.StringField(),
        'description': fields.StringField(nullable=True),
        'type': fields.MonitorType(),
        'target': fields.StringField(),
        'auth': fields.BooleanField(),
        'parameters': fields.ListOfObjectsField(objects.MonitorParameter)
    }

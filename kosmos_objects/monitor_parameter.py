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
from oslo_versionedobjects.base import VersionedObjectRegistry

from kosmos_objects import base
from kosmos_objects import fields


@VersionedObjectRegistry.register
class MonitorParameter(base.KosmosObject, base.KosmosOwnedObject,
                       base.KosmosPersistentObject):

    VERSION = '1.0'

    fields = {
        'key': fields.StringField(nullable=False),
        'value': fields.StringField(nullable=True),
    }

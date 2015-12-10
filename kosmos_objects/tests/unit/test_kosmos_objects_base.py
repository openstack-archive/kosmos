# -*- coding: utf-8 -*-

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

"""
test_kosmos
----------------------------------

Tests for `kosmos_objects` module.
"""
import uuid
import testtools
from oslo_versionedobjects import exception
from kosmos_objects.tests.unit import base
import kosmos_objects
import kosmos_objects.fields as kosmos_fields


class TestPreDefinedEnumType(kosmos_fields.PreDefinedEnumType):

    _TYPES = (
        'Galactica',
        'Pegasus',
        'Athena',
        'Atlantia',
        'Columbia',
        'Erasmus',
        'Night Flight',
        'Solaria',
        'Triton',
        'Uned',
        'Universal',
        'Valkyrie',
        'Yashuman',
    )


@kosmos_objects.base.VersionedObjectRegistry.register
class TestObject(kosmos_objects.base.KosmosObject):

    fields = {
        'text': kosmos_fields.StringField(),
        'uuid': kosmos_fields.UUIDField(),
        'int': kosmos_fields.IntegerField(),
        'read_only': kosmos_fields.StringField(read_only=True),
        'dns_zone_name': kosmos_fields.DNSZoneName(),
        'dns_fqdn': kosmos_fields.DNSFQDN(),
        'pool_member_type': kosmos_fields.PoolMemberType(),
        'monitor_type': kosmos_fields.MonitorType(),
        'enum': TestPreDefinedEnumType()
    }


@kosmos_objects.base.VersionedObjectRegistry.register_if(False)
class TestOwnedObject(kosmos_objects.base.KosmosObject,
                      kosmos_objects.base.KosmosOwnedObject):

    pass


@kosmos_objects.base.VersionedObjectRegistry.register_if(False)
class TestPersistentObject(kosmos_objects.base.KosmosObject,
                           kosmos_objects.base.KosmosPersistentObject):
    pass


@kosmos_objects.base.VersionedObjectRegistry.register_if(False)
class TestPersistentOwnedObject(kosmos_objects.base.KosmosObject,
                                kosmos_objects.base.KosmosPersistentObject,
                                kosmos_objects.base.KosmosOwnedObject):
    pass


class TestKosmosObjectsBase(base.TestCase):

    def test_basic(self):
        test_object = TestObject()

        self.assertEqual(test_object.OBJ_PROJECT_NAMESPACE, 'kosmos')

    def test_owned_mixin(self):
        test_object = TestOwnedObject()

        set_fields = [x for x in test_object.fields.keys()]

        required_fields = [
            'project_id',
            'domain_id'
        ]

        set_fields.sort()
        required_fields.sort()
        self.assertEqual(required_fields, set_fields)

    def test_persistant_mixin(self):
        test_object = TestPersistentObject()

        set_fields = [x for x in test_object.fields.keys()]

        required_fields = [
            'id',
            'version',
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted',
        ]

        set_fields.sort()
        required_fields.sort()
        self.assertEqual(required_fields, set_fields)

    def test_persistant_owned_mixin(self):
        test_object = TestPersistentOwnedObject()

        set_fields = [x for x in test_object.fields.keys()]

        required_fields = [
            'id',
            'version',
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted',
            'project_id',
            'domain_id'
        ]

        set_fields.sort()
        required_fields.sort()
        self.assertEqual(required_fields, set_fields)

    def test_to_from_dict(self):
        test_object = TestPersistentOwnedObject()

        test_object = TestObject()
        test_object.text = 'test_text'
        test_object.uuid = str(uuid.uuid4())
        test_object.int = 42
        test_object.dns_zone_name = 'dns.zone.tld.'
        test_object.dns_fqdn = '*.dns.zone.tld.'
        test_object.enum = 'Galactica'
        test_object.pool_member_type = 'IP'
        test_object.monitor_type = 'HTTP'

        test_object_2 = kosmos_objects.base.KosmosObject().obj_from_primitive(
            test_object.obj_to_primitive())

        self.assertEqual(
            test_object_2.obj_to_primitive(),
            test_object.obj_to_primitive())


class TestKosmosObjectsFields(base.TestCase):

    def test_basic(self):
        test_object = TestObject()
        test_object.text = 'test_text'
        test_object.uuid = str(uuid.uuid4())
        test_object.int = 42
        test_object.dns_zone_name = 'dns.zone.tld.'
        test_object.dns_fqdn = '*.dns.zone.tld.'

    def test_invalid_data(self):
        test_object = TestObject()

        with testtools.ExpectedException(ValueError):
            test_object.text = TestOwnedObject()
        with testtools.ExpectedException(ValueError):
            test_object.uuid = 'fake_uuid'
        with testtools.ExpectedException(ValueError):
            test_object.int = 'one'
        with testtools.ExpectedException(ValueError):
            test_object.dns_zone_name = 'dns.zone.tld'
        with testtools.ExpectedException(ValueError):
            test_object.dns_fqdn = 'name'

    def test_read_only(self):
        test_object = TestObject()
        # Set initial value - 'read_only' is write once, then read only
        test_object.read_only = 'Initial Value'
        with testtools.ExpectedException(exception.ReadOnlyFieldError):
            test_object.read_only = 'Updated Value'
        self.assertEqual(test_object.read_only, 'Initial Value')

    def test_enums_base(self):
        test_object = TestObject()
        test_object.enum = 'Galactica'
        test_object.enum = 'Athena'
        with testtools.ExpectedException(ValueError):
            test_object.enum = 'Enterprise'

    def test_enums_pool_member(self):
        test_object = TestObject()
        test_object.pool_member_type = 'IP'
        test_object.pool_member_type = 'NEUTRON_PORT'
        with testtools.ExpectedException(ValueError):
            test_object.pool_member_type = 'AMAZON_ELB'

    def test_enums_monitor_type(self):
        test_object = TestObject()
        test_object.monitor_type = 'TCP'
        test_object.monitor_type = 'HTTP'
        with testtools.ExpectedException(ValueError):
            test_object.monitor_type = 'XMPP'

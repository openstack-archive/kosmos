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

"""
test_kosmos
----------------------------------

Tests for `objects` module.
"""
import uuid
import testtools
from oslo_versionedobjects import exception
from kosmos.tests.unit.objects import base as test
from kosmos import objects
import kosmos.objects.fields as kosmos_fields


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


@objects.base.VersionedObjectRegistry.register_if(False)
class TestObject(objects.base.KosmosObject):

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


@objects.base.VersionedObjectRegistry.register_if(False)
class TestOwnedObject(objects.base.KosmosObject,
                      objects.base.KosmosOwnedObject):

    pass


@objects.base.VersionedObjectRegistry.register_if(False)
class TestPersistentObject(objects.base.KosmosObject,
                           objects.base.KosmosPersistentObject):
    pass


@objects.base.VersionedObjectRegistry.register_if(False)
class TestPersistentOwnedObject(objects.base.KosmosObject,
                                objects.base.KosmosPersistentObject,
                                objects.base.KosmosOwnedObject):
    pass


class TestKosmosObjectsBase(test.TestCase):

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
            'deleted_at'
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
            'project_id',
            'domain_id'
        ]

        set_fields.sort()
        required_fields.sort()
        self.assertEqual(required_fields, set_fields)

    def test_to_dict(self):
        test_object = TestPersistentOwnedObject()

        test_object = TestObject()
        test_object.text = 'test_text'
        test_object.uuid = '77c1e75d-ba52-4ec9-a0a8-9d61bfb85407'
        test_object.int = 42
        test_object.dns_zone_name = 'dns.zone.tld.'
        test_object.dns_fqdn = '*.dns.zone.tld.'
        test_object.enum = 'Galactica'
        test_object.pool_member_type = 'IP'
        test_object.monitor_type = 'HTTP'

        test_object.obj_reset_changes()

        expected_output = {
            'versioned_object.name': 'TestObject',
            'versioned_object.namespace': 'kosmos',
            'versioned_object.data': {
                'int': 42,
                'dns_fqdn': '*.dns.zone.tld.',
                'dns_zone_name': 'dns.zone.tld.',
                'text': 'test_text',
                'uuid': '77c1e75d-ba52-4ec9-a0a8-9d61bfb85407',
                'monitor_type': 'HTTP',
                'enum': 'Galactica',
                'pool_member_type': 'IP'
            },
            'versioned_object.version': '1.0'
        }

        self.assertDictEqual(test_object.obj_to_primitive(), expected_output)


class TestKosmosObjectsFields(test.TestCase):

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

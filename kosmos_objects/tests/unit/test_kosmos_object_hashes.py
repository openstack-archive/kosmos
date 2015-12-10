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
from oslo_versionedobjects import fixture
from kosmos_objects.tests.unit import base as test
from kosmos_objects import base


# NOTE: The hashes in this list should only be changed if they come with a
# corresponding version bump in the affected objects.
object_data = {
    'LoadBalancer': '1.0-d0fc9b66f0a34674bea459bf85afc488',
    'Monitor': '1.0-b68ec6081b4a1848c72635853aed56a3',
    'MonitorParameter': '1.0-2ba3fe897a98a80ce01f719cb72a9525',
    'Pool': '1.0-e716d0fc0895e85763dc51b9a23c8568',
    'PoolMember': '1.0-b959a3f87656f7f553eaec573ebaffc7',
    'PoolMemberParameter': '1.0-2ba3fe897a98a80ce01f719cb72a9525',
}


class TestObjectVersions(test.TestCase):

    def test_versions(self):
        checker = fixture.ObjectVersionChecker(
            base.VersionedObjectRegistry.obj_classes())
        expected, actual = checker.test_hashes(object_data)
        self.assertEqual(expected, actual,
                         'Some objects have changed; please make sure the '
                         'versions have been bumped, and then update their '
                         'hashes in the object_data map in this test module.')

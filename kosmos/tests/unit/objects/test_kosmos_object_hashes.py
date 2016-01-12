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
from kosmos.tests.unit.objects import base as test
from kosmos.objects import base


# NOTE: The hashes in this list should only be changed if they come with a
# corresponding version bump in the affected objects.
object_data = {
    'LoadBalancer': '1.0-b1c9ee6d670761a96c72cf664039eaaa',
    'Monitor': '1.0-3e98af74f3c7f366a2c5615de910952d',
    'MonitorParameter': '1.0-07e865a2200abd700ef7101152f0ec40',
    'Pool': '1.0-1e4e0d82db50e6da85154b28faf71f5c',
    'PoolMember': '1.0-9537b1e55498529a36d9ca225e9c5c7c',
    'PoolMemberParameter': '1.0-07e865a2200abd700ef7101152f0ec40',
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

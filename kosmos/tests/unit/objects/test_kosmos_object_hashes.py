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
    'LoadBalancer': '1.0-06538794c851e034ece73694cc4737ad',
    'Monitor': '1.0-1e3dd244093ce14b4b8079ae4deea343',
    'MonitorParameter': '1.0-5fae2adca64543db6c854f6418de7089',
    'Pool': '1.0-fb284fb3826c2c984494a319f91d04b1',
    'PoolMember': '1.0-0586ac99722f74080988aa49113452de',
    'PoolMemberParameter': '1.0-5fae2adca64543db6c854f6418de7089'
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

# -*- coding: utf-8 -*-

# Copyright 2010-2011 OpenStack Foundation
# Copyright 2015-2016 Hewlett Packard Enterprise Development LP
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
from kosmos.tests.unit import base as test
from kosmos import objects


class TestCase(test.TestCase):

    def setUp(self):
        objects.register_all()
        super(TestCase, self).setUp()

    """Test case base class for all unit tests."""
    @staticmethod
    def compare_objects(test_case, obj_1, obj_2):
        for field, value in obj_1.items():
            test.assertEqual(getattr(obj_1, field), getattr(obj_2, field))

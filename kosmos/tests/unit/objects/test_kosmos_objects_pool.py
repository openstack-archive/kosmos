# -*- coding: utf-8 -*-
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

Tests for `kosmos_objects` `Pool` class.
"""
from kosmos.tests.unit.objects import base as test
from kosmos import objects
import kosmos.objects.fields as kosmos_fields


class TestKosmosObjectsPool(test.TestCase):

    def test_basic(self):
        test_object = objects.pool.Pool()

        test_object = objects.pool.Pool()
        test_object.id = '568004ac-e41c-43bc-8a42-c284a7eaea25'
        test_object.name = "Pool Name"
        test_object.description = "Pool Description"
        test_object.members = [
            objects.base.KosmosObject.obj_class_from_name(
                'PoolMember', '1.0')()
        ]
        test_object.members[0].id = 'b47d8499-de07-4344-a9e1-9773375a66e0'
        test_object.members[0].name = "Pool Member Name"
        test_object.members[0].description = "Pool Member Description"
        test_object.members[0].type = kosmos_fields.PoolMemberType.IP
        test_object.members[0].parameters = [
            objects.base.KosmosObject.obj_class_from_name(
                'PoolMemberParameter', '1.0'
            )()
        ]
        test_object.members[0].parameters[0].key = 'address'
        test_object.members[0].parameters[0].value = '10.0.0.1'

        test_object.obj_reset_changes()

        self.assertEqual(test_object.OBJ_PROJECT_NAMESPACE, 'kosmos')

    def test_from_dict(self):

        test_input = {
            'versioned_object.namespace': 'kosmos',
            'versioned_object.data': {
                'id': '568004ac-e41c-43bc-8a42-c284a7eaea25',
                'name': 'Pool Name',
                'description': 'Pool Description',
                'members': [
                    {
                        'versioned_object.namespace': 'kosmos',
                        'versioned_object.data': {
                            'id': 'b47d8499-de07-4344-a9e1-9773375a66e0',
                            'type': 'IP',
                            'name': 'Pool Member Name',
                            'description': 'Pool Member Description',
                            'parameters': [
                                {
                                    'versioned_object.namespace': 'kosmos',
                                    'versioned_object.data': {
                                        'key': 'address',
                                        'value': '10.0.0.1'
                                    },
                                    'versioned_object.version': '1.0',
                                    'versioned_object.name':
                                    'PoolMemberParameter',
                                }
                            ]
                        },
                        'versioned_object.version': '1.0',
                        'versioned_object.name': 'PoolMember',
                    }
                ]
            },
            'versioned_object.version': '1.0',
            'versioned_object.name': 'Pool',
        }

        objects.base.KosmosObject.obj_from_primitive(test_input)

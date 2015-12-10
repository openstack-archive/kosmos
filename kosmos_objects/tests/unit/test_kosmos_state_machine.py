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

import testtools
from kosmos_objects.tests.unit import base
import kosmos_objects
import kosmos_objects.fields as kosmos_fields


class TestStateMachineField(kosmos_fields.StateMachineEnforce,
                            kosmos_fields.PreDefinedEnumType):

    ACTIVE = 'active'
    PENDING = 'pending'
    DEGRADED = 'degraded'
    DOWN = 'down'
    ERROR = 'error'

    ALLOWED_TRANSITIONS = {
        # This is dict of states, that have dicts of states an object is
        # allowed to transition to
        ACTIVE: {
            DEGRADED,
            DOWN,
            ERROR,
            PENDING
        },
        PENDING: {
            ACTIVE,
            ERROR
        },
        DEGRADED: {
            ERROR,
            DOWN,
            ACTIVE
        },
        DOWN: {
            ACTIVE,
            ERROR
        },
        ERROR: {
            PENDING,
            ACTIVE
        }
    }

    _TYPES = (
        ACTIVE,
        PENDING,
        DEGRADED,
        DOWN,
        ERROR
    )


@kosmos_objects.base.VersionedObjectRegistry.register_if(False)
class StateMachineTestObject(kosmos_objects.base.KosmosObject):

    VERSION = '1.0'

    fields = {
        'status': TestStateMachineField()
    }


class TestKosmosObjectsFields(base.TestCase):

    def test_non_existant_states(self):
        test_object = StateMachineTestObject()
        with testtools.ExpectedException(
                ValueError,
                msg="missing is not a valid choice, choose from ('active', "
                "'pending', 'degraded', 'down', 'error')"):
            test_object.status = 'missing'

    def test_allow_transitions(self):
        test_object = StateMachineTestObject()
        test_object.status = TestStateMachineField.PENDING
        test_object.status = TestStateMachineField.ACTIVE
        test_object.status = TestStateMachineField.DOWN
        test_object.status = TestStateMachineField.ERROR
        test_object.status = 'pending'

    def test_disallow_transitions(self):
        test_object = StateMachineTestObject()
        test_object.status = TestStateMachineField.PENDING
        with testtools.ExpectedException(
                ValueError,
                msg="StateMachineTestObject's are not allowed transition out "
                "of 'pending' state to 'down' state, choose from "
                "['error', 'active']"):
            test_object.status = TestStateMachineField.DOWN

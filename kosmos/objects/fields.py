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
from kosmos._i18n import _
import re
import uuid as uuid_tools
from oslo_versionedobjects import fields


# Import field errors from oslo.versionedobjects
KeyTypeError = fields.KeyTypeError
ElementTypeError = fields.ElementTypeError

# Import fields from oslo.versionedobjects
BooleanField = fields.BooleanField
UnspecifiedDefault = fields.UnspecifiedDefault
IntegerField = fields.IntegerField
FloatField = fields.FloatField
StringField = fields.StringField
EnumField = fields.EnumField
DateTimeField = fields.DateTimeField
DictOfStringsField = fields.DictOfStringsField
DictOfNullableStringsField = fields.DictOfNullableStringsField
DictOfIntegersField = fields.DictOfIntegersField
ListOfStringsField = fields.ListOfStringsField
SetOfIntegersField = fields.SetOfIntegersField
ListOfSetsOfIntegersField = fields.ListOfSetsOfIntegersField
ListOfDictOfNullableStringsField = fields.ListOfDictOfNullableStringsField
DictProxyField = fields.DictProxyField
ObjectField = fields.ObjectField
ListOfObjectsField = fields.ListOfObjectsField

# Ripped from designate/schema/format.py
RE_ZONENAME = r'^(?!.{255,})(?:(?!\-)[A-Za-z0-9_\-]{1,63}(?<!\-)\.)+\Z'
RE_HOSTNAME = r'^(?!.{255,})(?:(?:^\*|(?!\-)[A-Za-z0-9_\-]{1,63})(?<!\-)\.)+\Z'


# TODO(graham): Remove this when https://review.openstack.org/#/c/250493
# merges
class UUID(fields.FieldType):

    def coerce(self, obj, attr, value):

        msg = _("%(value)s is not a valid UUID for %(attr)s") % {
            'attr': attr,
            'value': value
        }
        try:
            uuid_tools.UUID(value)
        except ValueError:
            raise ValueError(msg)

        return str(value)


class UUIDField(fields.AutoTypedField):
    AUTO_TYPE = UUID()


class DNSZoneName(StringField):

    def coerce(self, obj, attr, value):

        if not re.match(RE_ZONENAME, value):
            msg = _("'%s' is not valid a valid DNS Zone name") % value
            raise ValueError(msg)

        return super(DNSZoneName, self).coerce(obj, attr, value)


class DNSFQDN(StringField):

    def coerce(self, obj, attr, value):
        if not re.match(RE_HOSTNAME, value):
            msg = _("'%s' is not valid a valid DNS Zone name") % value
            raise ValueError(msg)

        return super(DNSFQDN, self).coerce(obj, attr, value)


class PreDefinedEnumType(EnumField):

    _TYPES = ()
    _msg = _("%(value)s is not a valid choice, choose from %(options)r")

    def __init__(self, **kwargs):
        super(PreDefinedEnumType, self).__init__(self._TYPES, **kwargs)

    def coerce(self, obj, attr, value):
        try:
            return super(PreDefinedEnumType, self).coerce(obj, attr, value)
        except ValueError:
            msg = self._msg % {"value": value, "options": self._TYPES}
            raise ValueError(msg)


class PoolMemberType(PreDefinedEnumType):

    IP = 'IP'
    NEUTRON_LBAAS_V2 = 'NEUTRON_LBAAS_V2'
    NEUTRON_PORT = 'NEUTRON_PORT'

    # TODO(graham): Dynamically Load this list of types from config + plugins
    _TYPES = (IP, NEUTRON_LBAAS_V2, NEUTRON_PORT)


class MonitorType(PreDefinedEnumType):

    TCP = 'TCP'
    UDP = 'UDP'
    ICMP = 'ICMP'
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    SSH = 'SSH'

    # TODO(graham): Dynamically Load this list of types from config + plugins
    _TYPES = (TCP, UDP, ICMP, HTTP, HTTPS, SSH)

    _msg = _("%(value)s is not a valid Monitor Type, choose from %(options)r")


class StateMachineEnforce(object):

    # This is dict of states, that have dicts of states an object is
    # allowed to transition to

    ALLOWED_TRANSITIONS = {}

    def coerce(self, obj, attr, value):
        super(StateMachineEnforce, self).coerce(obj, attr, value)
        msg = _("%(object)s's are not allowed transition out of %(value)s "
                "state")
        # olso.versionedobjects do not create the field until it is first used
        try:
            current_value = getattr(obj, attr)
        except NotImplementedError:
            return value

        if current_value in self.ALLOWED_TRANSITIONS:

            if value in self.ALLOWED_TRANSITIONS[current_value]:
                return value
            else:
                msg = _(
                    "%(object)s's are not allowed transition out of "
                    "'%(current_value)s' state to '%(value)s' state, choose "
                    "from %(options)r")
        msg = msg % {
            'object': obj.obj_name(),
            'current_value': current_value,
            'value': value,
            'options': [x for x in self.ALLOWED_TRANSITIONS[current_value]]
        }
        raise ValueError(msg)


class KosmosActions(StateMachineEnforce, PreDefinedEnumType):

    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    NONE = 'none'

    ALLOWED_TRANSITIONS = {
        CREATE: {
            NONE,
            UPDATE
        },
        UPDATE: {
            NONE
        },
        NONE: {
            UPDATE,
            DELETE
        },
        DELETE: {
            NONE
        }
    }

    _TYPES = (CREATE, UPDATE, DELETE, NONE)

    _msg = _("%(value)s is not a valid Action, choose from %(options)r")

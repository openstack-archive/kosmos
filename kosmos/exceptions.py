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
import six


class Base(Exception):
    error_code = 500
    error_type = None
    error_message = None
    errors = None

    def __init__(self, *args, **kwargs):
        self.errors = kwargs.pop('errors', None)
        self.object = kwargs.pop('object', None)

        super(Base, self).__init__(*args, **kwargs)

        if len(args) > 0 and isinstance(args[0], six.string_types):
            self.error_message = args[0]


# 500 Errors
class NotImplemented(Base, NotImplementedError):
    pass


class ConfigurationError(Base):
    error_type = 'configuration_error'


# 400 Errors
class BadRequest(Base):
    error_code = 400
    error_type = 'bad_request'
    expected = True


class Forbidden(Base):
    error_code = 403
    error_type = 'forbidden'
    expected = True

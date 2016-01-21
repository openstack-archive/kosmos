# Copyright 2016 Hewlett Packard Enterprise Development LP
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
Base classes for storage engines
"""

import abc

from oslo_config import cfg
from oslo_db import api as db_api
import six

_BACKEND_MAPPING = {'sqlalchemy': 'kosmos.db.sqlalchemy.api'}
IMPL = db_api.DBAPI.from_config(cfg.CONF, backend_mapping=_BACKEND_MAPPING,
                                lazy=True)


def get_instance():
    """Return a DB API instance."""
    return IMPL


@six.add_metaclass(abc.ABCMeta)
class Connection(object):
    """Base class for storage system connections."""

    @abc.abstractmethod
    def __init__(self):
        """Constructor."""

    @abc.abstractmethod
    def get_object_by_id(self, context, table, id, *args, **kwargs):
        """Returns a objects for specified id.
        :param context: request context object
        :returns: an object of :class:'KosmosObject' object
        """

    @abc.abstractmethod
    def find_objects(self, context, table, criterion, *args, **kwargs):
        """Returns a list objects for criterion.
        :param context: request context object
        :returns: a list objects of :class:'KosmosObject' object
        """

    @abc.abstractmethod
    def get_loadbalancers(self, context, *args, **kwargs):
        """Returns a list of Loadbalancer objects for specified project_id.
        :param context: request context object
        :returns: a list of :class:'Loadbalancer' object
        """

    @abc.abstractmethod
    def get_loadbalancer_by_id(self, context, id, *args, **kwargs):
        """Returns a Loadbalancer object for specified id.
        :param context: request context object
        :returns: :class:'Loadbalancer' object
        """

    @abc.abstractmethod
    def find_loadbalancers(self, context, filters, find_one=False, *args,
                           **kwargs):
        """Returns a list of Loadbalancer objects for specified project_id.
        :param context: request context object
        :returns: a list of :class:'Loadbalancer' object
        """
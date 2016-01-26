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
        :param table: target data table where object gets info from
        :param id: object id that will be passing
        :returns: an object of :class:'KosmosObject' object
        """

    @abc.abstractmethod
    def get_objects(self, context, table, criterion, *args, **kwargs):
        """Returns a list objects for criterion.

        :param context: request context object
        :param table: target data table where object gets info from
        :param criterion: dictionary of filters to be applied
        :returns: a list objects of :class:'KosmosObject' object
        """

    @abc.abstractmethod
    def apply_criterion(table, query, criterion):
        """Build the query based on criterion.

        :param query: incoming query which needs to apply criterion on
        :param criterion: dictionary of filters to be applied
        :returns: filtered query based on value of criterion
        """
        pass

    @abc.abstractmethod
    def apply_version_increment(self, context, table, query):
        """
        Apply Version Incrementing SQL fragment a Query
        This should be called on all UPDATE queries, as it will ensure the
        version column is correctly incremented.

        :param context: request context object
        :param table: target data table where object gets info from
        :param query: incoming query
        :returns: filtered query based on table's new verion info
        """

    @abc.abstractmethod
    def apply_project_criteria(self, context, table, query):
        """
        Apply project id query fragment a Query
        This should be called on all UPDATE queries, as it will ensure the
        items related to a specific project will be get.

        :param context: request context object
        :param table: target data table where object gets info from
        :param query: incoming query
        :returns: filtered query based on table's project column info
        """

    @abc.abstractmethod
    def apply_deleted_criteria(self, context, table, query):
        """
        Apply deleted criteria fragment to a Query
        This should be called on all queries, as it will ensure those
        items that has been filtered by the deleted criteria will be retrieved.

        :param context: request context object
        :param table: target data table where object gets info from
        :param query: incoming query
        :returns: filtered query based on delete criteria
        """

    @abc.abstractmethod
    def create(self, table, obj):
        """
        Create object into database table.

        :param table: data table item that will be inserted
        :param obj: object that will be created
        """

    @abc.abstractmethod
    def update(self, table, obj):
        """
        Update object in database table.

        :param table: data table item that will be updated
        :param obj: object that will be updated
        """

    @abc.abstractmethod
    def delete(self, table, obj):
        """
        Delete object in database table.

        :param table: data table item that will be deleted
        :param obj: object that will be deleted
        """

    @abc.abstractmethod
    def select_raw(self, context, table, criterion, query=None):

        """
        Build raw query based on criterion and query.

        :param context: request context object
        :param table: target data table where object gets info from
        :param criterion: dictionary of filters to be applied
        :param query: incoming query, it can be none
        :returns: build query based on passing criterion and query
        """

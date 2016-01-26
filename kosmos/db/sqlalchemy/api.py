# Copyright 2011 VMware, Inc.
#    All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Base copied from Neutron
import six

from oslo_config import cfg
from oslo_db import options as db_options
from oslo_db.sqlalchemy import session
from oslo_log import log as logging
from kosmos.common import exceptions
from sqlalchemy import select, or_, between

from kosmos.db import api


CONF = cfg.CONF

CONF.register_opt(cfg.StrOpt('sqlite_db', default='cue.sqlite'))

LOG = logging.getLogger(__name__)

db_options.set_defaults(
    cfg.CONF, connection='mysql+pymysql://kosmos:password@localhost/kosmos')

_FACADE = None


def _create_facade_lazily():
    global _FACADE

    if _FACADE is None:
        _FACADE = session.EngineFacade.from_config(cfg.CONF, sqlite_fk=True)

    return _FACADE


def get_engine():
    """Helper method to grab engine."""
    facade = _create_facade_lazily()
    return facade.get_engine()


def dispose_engine():
    get_engine().dispose()


def get_session(autocommit=True, expire_on_commit=False):
    """Helper method to grab session."""
    facade = _create_facade_lazily()
    return facade.get_session(autocommit=autocommit,
                              expire_on_commit=expire_on_commit)


class Connection(api.Connection):
    """SqlAlchemy connection implementation."""

    def __init__(self):
        pass

    def get_object_by_id(self, context, table, id, *args, **kwargs):

        query = select([table], table.c.id.like(id))

        session = kwargs.get('session') or get_session()

        s = session.execute(query)
        rs = s.fetchone()

        return rs

        """
        Create object into database table.
        """
    def get_objects(self, context, table, criterion, *args, **kwargs):

        query = select([table])

        session = kwargs.get('session') or get_session()

        query = self.apply_criterion(table, query, criterion)

        s = session.execute(query)
        return s.fetchall()

    def apply_criterion(table, query, criterion):
        if criterion is not None:
            for name, value in criterion.items():
                column = getattr(table.c, name)

                # Wildcard value: '%'
                if isinstance(value, six.string_types) and '%' in value:
                    query = query.where(column.like(value))

                elif (isinstance(value, six.string_types) and
                        value.startswith('!')):
                    queryval = value[1:]
                    query = query.where(column != queryval)

                elif (isinstance(value, six.string_types) and
                        value.startswith('<=')):
                    queryval = value[2:]
                    query = query.where(column <= queryval)

                elif (isinstance(value, six.string_types) and
                        value.startswith('<')):
                    queryval = value[1:]
                    query = query.where(column < queryval)

                elif (isinstance(value, six.string_types) and
                        value.startswith('>=')):
                    queryval = value[2:]
                    query = query.where(column >= queryval)

                elif (isinstance(value, six.string_types) and
                        value.startswith('>')):
                    queryval = value[1:]
                    query = query.where(column > queryval)

                elif (isinstance(value, six.string_types) and
                        value.startswith('BETWEEN')):
                    elements = [i.strip(" ") for i in
                                value.split(" ", 1)[1].strip(" ").split(",")]
                    query = query.where(between(
                        column, elements[0], elements[1]))

                elif isinstance(value, list):
                    query = query.where(column.in_(value))

                else:
                    query = query.where(column == value)

        return query

    def apply_version_increment(self, context, table, query):
        """
        Apply Version Incrementing SQL fragment a Query
        This should be called on all UPDATE queries, as it will ensure the
        version column is correctly incremented.
        """
        if hasattr(table.c, 'version'):
            # NOTE(kiall): This will translate into a true SQL increment.
            query = query.values({'version': table.c.version + 1})

        return query

    def apply_project_criteria(self, context, table, query):
        if hasattr(table.c, 'tenant_id'):
            if not context.all_tenants:
                # NOTE: The query doesn't work with table.c.tenant_id is None,
                # so I had to force flake8 to skip the check
                query = query.where(or_(table.c.tenant_id == context.tenant,
                                        table.c.tenant_id == None))  # NOQA

        return query

    def apply_deleted_criteria(self, context, table, query):
        if hasattr(table.c, 'deleted'):
            if context.show_deleted:
                LOG.debug('Including deleted items in query results')
            else:
                query = query.where(table.c.deleted == "0")

        return query

    def select_raw(self, context, table, criterion, query=None):
        # Build the query
        if query is None:
            query = select([table])

        query = self._apply_criterion(table, query, criterion)
        query = self._apply_deleted_criteria(context, table, query)

        try:
            resultproxy = self.session.execute(query)
            return resultproxy.fetchall()
        # Any ValueErrors are propagated back to the user as is.
        # If however central or storage is called directly, invalid values
        # show up as ValueError
        except ValueError as value_error:
            raise exceptions.ValueError(six.text_type(value_error))

    def create(self, table, obj):
        pass

    def update(self, table, obj):
        pass

    def delete(self, table, obj):
        pass

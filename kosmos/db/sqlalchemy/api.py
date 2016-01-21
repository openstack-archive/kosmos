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

from kosmos._i18n import _  # noqa
from oslo_config import cfg
from oslo_db import exception as db_exception
from oslo_db import options as db_options
from oslo_db.sqlalchemy import session
from oslo_utils import timeutils
from sqlalchemy.orm import exc as sql_exception
from kosmos.common import exceptions
from kosmos.db.sqlalchemy import tables
from sqlalchemy import select, or_, between

from kosmos.db import api

CONF = cfg.CONF

CONF.register_opt(cfg.StrOpt('sqlite_db', default='cue.sqlite'))

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


def get_session(autocommit=True, expire_on_commit=False):
    """Helper method to grab session."""
    facade = _create_facade_lazily()
    return facade.get_session(autocommit=autocommit,
                              expire_on_commit=expire_on_commit)


def get_backend():
    """The backend is this module itself."""
    return Connection()


def table_query(context, table, *args, **kwargs):
    """Query helper for simpler session usage.
    :param session: if present, the session to use
    """
    session = kwargs.get('session') or get_session()
    query = session.query(table, *args)

    read_deleted = kwargs.get('read_deleted', False)
    project_only = kwargs.get('project_only', False)

    if not read_deleted:
        query = query.filter_by(deleted=False)

    if project_only:
        # filter by project_id
        if hasattr(table, 'project_id'):
            query = query.filter_by(project_id=context.project_id)

    return query


def soft_delete(record_values):
        """Mark this object as deleted."""
        record_values['deleted'] = record_values['id']
        record_values['deleted_at'] = timeutils.utcnow()


class Connection(api.Connection):
    """SqlAlchemy connection implementation."""

    def __init__(self):
        pass

    @staticmethod
    def _apply_criterion(table, query, criterion):
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

    def get_object_by_id(self, context, table, id, *args, **kwargs):

        query = select([table], table.c.id.like(id))

        session = kwargs.get('session') or get_session()

        s = session.execute(query)
        rs = s.fetchone()

        return rs

    def find_objects(self, context, table, criterion, *args, **kwargs):

        query = select([table])

        session = kwargs.get('session') or get_session()

        query = self._apply_criterion(table, query, criterion)

        s = session.execute(query)
        return s.fetchall()


    def get_loadbalancers(self, context, *args, **kwargs):
        query = table_query(context, tables.loadbalancers, *args, **kwargs)
        return query.all()

    def get_loadbalancer_by_id(self, context, id, *args, **kwargs):

        query = select([tables.loadbalancers, tables.pools]).select_from(
            tables.loadbalancers.join(tables.pools,
                                      tables.loadbalancers.c.id.like(id))
        )


        session = kwargs.get('session') or get_session()
        s = session.execute(query)
        rs = s.fetchall()
        if len(rs) != 1:
            raise exceptions.BadRequest()
        return rs


    def find_loadbalancers(self, context, filters, find_one=False, *args,
                           **kwargs):
        query = table_query(context, tables.loadbalancers, *args, **kwargs)
        return query.all()


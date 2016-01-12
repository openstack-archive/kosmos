# © Copyright 2016 Hewlett Packard Enterprise Development Company LP
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
import sqlalchemy as sa

from oslo_config import cfg
from oslo_utils import timeutils

from kosmos.db.sqla.types import UUID
from kosmos.common import utils


CONF = cfg.CONF

metadata = sa.MetaData()

ACTIONS = sa.Enum(
    'CREATE',
    'UPDATE',
    'DELETE',
    'NONE'
)

POOL_STATUSES = sa.Enum(
    'ACTIVE',
    'PENDING',
    'DEGRADED',
    'DOWN',
    'ERROR',
    'DELETED',
)

MONITOR_STATUSES = sa.Enum(
    'ACTIVE',
    'PENDING',
    'ERROR',
    'DELETED',
)

GENERIC_STATUSES = sa.Enum(
    'ACTIVE',
    'DELETED'
)


monitors = sa.Table(
    'monitors',
    metadata,

    sa.Column('id', UUID, default=utils.generate_uuid, nullable=False),
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('domain_id', sa.String(length=36), nullable=False),

    sa.Column('created_at', sa.DateTime(), default=lambda: timeutils.utcnow(),
              nullable=True),
    sa.Column('updated_at', sa.DateTime(),
              onupdate=lambda: timeutils.utcnow(),
              nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('version', sa.Integer(), default=1, nullable=False),

    sa.Column('action', ACTIONS, default='none', nullable=False),
    sa.Column('status', MONITOR_STATUSES, default='active', nullable=False),

    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),

    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('auth', sa.Boolean, nullable=False, default=False),

    sa.PrimaryKeyConstraint('id', name="monitor_pk"),
)

pools = sa.Table(
    'pools',
    metadata,

    sa.Column('id', UUID, default=utils.generate_uuid, nullable=False),
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('domain_id', sa.String(length=36), nullable=False),

    sa.Column('created_at', sa.DateTime(), default=lambda: timeutils.utcnow(),
              nullable=True),
    sa.Column('updated_at', sa.DateTime(),
              onupdate=lambda: timeutils.utcnow(),
              nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('version', sa.Integer(), default=1, nullable=False),

    sa.Column('action', ACTIONS, default='none', nullable=False),
    sa.Column('status', MONITOR_STATUSES, default='active', nullable=False),

    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),

    sa.PrimaryKeyConstraint('id', name="pool_pk")
)

loadbalancers = sa.Table(
    'loadbalancers',
    metadata,

    sa.Column('id', UUID, default=utils.generate_uuid, nullable=False),
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('domain_id', sa.String(length=36), nullable=False),

    sa.Column('created_at', sa.DateTime(), default=lambda: timeutils.utcnow(),
              nullable=True),
    sa.Column('updated_at', sa.DateTime(),
              onupdate=lambda: timeutils.utcnow(),
              nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('version', sa.Integer(), default=1, nullable=False),

    sa.Column('action', ACTIONS, default='none', nullable=False),
    sa.Column('status', POOL_STATUSES, default='active', nullable=False),

    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),

    sa.Column('fqdn', sa.String(length=255), nullable=False),
    sa.Column('zone_name', sa.String(length=255), nullable=False),
    sa.Column('flavor_id', UUID, nullable=True),
    sa.Column('appliance_id', sa.String(length=255), nullable=True),
    sa.Column('pool_id', UUID, nullable=True),

    sa.PrimaryKeyConstraint('id', name="loadbalancer_pk"),
    sa.ForeignKeyConstraint(
        ['pool_id'],
        ['pools.id'],
        onupdate="CASCADE",
        ondelete="CASCADE",
        name="loadbalancer_pool_fk"
    )
)

pool_members = sa.Table(
    'pool_members',
    metadata,

    sa.Column('id', UUID, default=utils.generate_uuid, nullable=False),
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('domain_id', sa.String(length=36), nullable=False),

    sa.Column('created_at', sa.DateTime(), default=lambda: timeutils.utcnow(),
              nullable=True),
    sa.Column('updated_at', sa.DateTime(),
              onupdate=lambda: timeutils.utcnow(),
              nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('version', sa.Integer(), default=1, nullable=False),

    sa.Column('action', ACTIONS, default='none', nullable=False),
    sa.Column('status', POOL_STATUSES, default='active', nullable=False),

    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),


    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('pool_id', UUID, nullable=False),

    sa.PrimaryKeyConstraint('id', name="pool_member_pk"),
    sa.ForeignKeyConstraint(
        ['pool_id'],
        ['pools.id'],
        onupdate="CASCADE",
        ondelete="CASCADE",
        name="pool_members_pool_fk"
    )
)

pool_member_parameters = sa.Table(
    'pool_member_parameters',
    metadata,


    sa.Column('pool_member_id', UUID, nullable=False),
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=False),

    sa.PrimaryKeyConstraint('pool_member_id', 'key',
                            name="pool_member_parameter_pk"),
    sa.ForeignKeyConstraint(
        ['pool_member_id'],
        ['pool_members.id'],
        onupdate="CASCADE",
        ondelete="CASCADE",
        name="pool_member_parameter_pool_members_fk"
    )
)


monitor_parameters = sa.Table(
    'monitor_parameters',
    metadata,

    sa.Column('monitor_id', UUID, nullable=False),
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('monitor_id', 'key',
                            name="monitor_parameter_pk"),
    sa.ForeignKeyConstraint(
        ['monitor_id'],
        ['monitors.id'],
        onupdate="CASCADE",
        ondelete="CASCADE",
        name="monitor_parameters_monitor_fk"
    )
)

pools_monitors = sa.Table(
    'pools_monitors',
    metadata,

    sa.Column('pool_id', UUID, nullable=False),
    sa.Column('monitor_id', UUID, nullable=False),
    sa.PrimaryKeyConstraint('pool_id', 'monitor_id',
                            name="pool_monitor_pk"),
    sa.ForeignKeyConstraint(
        ['pool_id'],
        ['pools.id'],
        onupdate="CASCADE",
        ondelete="CASCADE",
        name="pool_monitors_pool_fk"
    ),
    sa.ForeignKeyConstraint(
        ['monitor_id'],
        ['monitors.id'],
        onupdate="CASCADE",
        ondelete="CASCADE",
        name="pool_monitors_monitor_fk"
    )
)

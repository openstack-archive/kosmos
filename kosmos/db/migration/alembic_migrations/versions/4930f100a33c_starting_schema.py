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
"""Starting Schema

Revision ID: 4930f100a33c
Revises:
Create Date: 2016-01-12 14:07:30.540955

"""

# revision identifiers, used by Alembic.

revision = '4930f100a33c'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from kosmos.db.sqlalchemy.types import UUID


def upgrade():
    op.create_table('monitors',
                    sa.Column('id', UUID(),
                              nullable=False),
                    sa.Column('project_id', sa.String(length=36),
                              nullable=False),
                    sa.Column('domain_id', sa.String(length=36),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True),
                    sa.Column('version', sa.Integer(), nullable=False),
                    sa.Column('action',
                              sa.Enum('CREATE', 'UPDATE', 'DELETE', 'NONE'),
                              nullable=False),
                    sa.Column('status',
                              sa.Enum('ACTIVE', 'PENDING', 'ERROR', 'DELETED'),
                              nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.String(length=255),
                              nullable=True),
                    sa.Column('type',
                              sa.Enum('TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS',
                                      'SSH'), nullable=False),
                    sa.Column('auth', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name='monitor_pk')
                    )
    op.create_table('pools',
                    sa.Column('id', UUID(),
                              nullable=False),
                    sa.Column('project_id', sa.String(length=36),
                              nullable=False),
                    sa.Column('domain_id', sa.String(length=36),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True),
                    sa.Column('version', sa.Integer(), nullable=False),
                    sa.Column('action',
                              sa.Enum('CREATE', 'UPDATE', 'DELETE', 'NONE'),
                              nullable=False),
                    sa.Column('status',
                              sa.Enum('ACTIVE', 'PENDING', 'ERROR', 'DELETED'),
                              nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.String(length=255),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id', name='pool_pk')
                    )
    op.create_table('loadbalancers',
                    sa.Column('id', UUID(),
                              nullable=False),
                    sa.Column('project_id', sa.String(length=36),
                              nullable=False),
                    sa.Column('domain_id', sa.String(length=36),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('version', sa.Integer(), nullable=False),
                    sa.Column('action',
                              sa.Enum('CREATE', 'UPDATE', 'DELETE', 'NONE'),
                              nullable=False),
                    sa.Column('status',
                              sa.Enum('ACTIVE', 'PENDING', 'DEGRADED', 'DOWN',
                                      'ERROR', 'DELETED'), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.String(length=255),
                              nullable=True),
                    sa.Column('fqdn', sa.String(length=255), nullable=False),
                    sa.Column('zone_name', sa.String(length=255),
                              nullable=False),
                    sa.Column('flavor_id', kosmos.db.sqla.types.UUID(),
                              nullable=False),
                    sa.Column('appliance_id', sa.String(length=255),
                              nullable=True),
                    sa.Column('pool_id', kosmos.db.sqla.types.UUID(),
                              nullable=True),
                    sa.ForeignKeyConstraint(['pool_id'], ['pools.id'],
                                            name='loadbalancer_pool_fk',
                                            onupdate='CASCADE',
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name='loadbalancer_pk')
                    )
    op.create_table('monitor_parameters',
                    sa.Column('monitor_id', kosmos.db.sqla.types.UUID(),
                              nullable=False),
                    sa.Column('key', sa.String(length=255), nullable=False),
                    sa.Column('value', sa.String(length=255), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['monitor_id'], ['monitors.id'],
                        name='monitor_parameters_monitor_fk',
                        onupdate='CASCADE',
                        ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('monitor_id', 'key',
                                            name='monitor_parameter_pk')
                    )
    op.create_table('pool_members',
                    sa.Column('id', UUID(),
                              nullable=False),
                    sa.Column('project_id', sa.String(length=36),
                              nullable=False),
                    sa.Column('domain_id', sa.String(length=36),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True),
                    sa.Column('version', sa.Integer(), nullable=False),
                    sa.Column('action',
                              sa.Enum('CREATE', 'UPDATE', 'DELETE', 'NONE'),
                              nullable=False),
                    sa.Column('status',
                              sa.Enum('ACTIVE', 'PENDING', 'DEGRADED', 'DOWN',
                                      'ERROR', 'DELETED'), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.String(length=255),
                              nullable=True),
                    sa.Column('type', sa.Enum('IP', 'NEUTRON_LBAAS_V2',
                                              'NEUTRON_PORT'), nullable=False),
                    sa.Column('pool_id', sa.String(length=36), nullable=False),
                    sa.ForeignKeyConstraint(['pool_id'], ['pools.id'],
                                            name='pool_members_pool_fk',
                                            onupdate='CASCADE',
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name='pool_member_pk')
                    )
    op.create_table('pools_monitors',
                    sa.Column('pool_id', sa.String(length=36), nullable=False),
                    sa.Column('monitor_id', kosmos.db.sqla.types.UUID(),
                              nullable=False),
                    sa.ForeignKeyConstraint(['monitor_id'], ['monitors.id'],
                                            name='pool_monitors_monitor_fk',
                                            onupdate='CASCADE',
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['pool_id'], ['pools.id'],
                                            name='pool_monitors_pool_fk',
                                            onupdate='CASCADE',
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('pool_id', 'monitor_id',
                                            name='pool_monitor_pk')
                    )
    op.create_table('pool_member_parameters',
                    sa.Column('pool_member_id', kosmos.db.sqla.types.UUID(),
                              nullable=False),
                    sa.Column('key', sa.String(length=255), nullable=False),
                    sa.Column('value', sa.String(length=255), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['pool_member_id'],
                        ['pool_members.id'],
                        name='pool_member_parameter_pool_members_fk',
                        onupdate='CASCADE',
                        ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('pool_member_id', 'key',
                                            name='pool_member_parameter_pk')
                    )

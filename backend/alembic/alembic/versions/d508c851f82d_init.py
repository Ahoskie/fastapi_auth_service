"""init

Revision ID: d508c851f82d
Revises: 
Create Date: 2021-05-18 15:48:38.054948

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from models.permissions import association_table


# revision identifiers, used by Alembic.
revision = 'd508c851f82d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'role',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(64)),
        relationship('Group', secondary=association_table, backref='roles', lazy='joined'),
    )

    op.create_table(
        'group',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(64)),
    )

    op.create_table(
        association_table,
        sa.Column('role_id', sa.Integer, sa.ForeignKey('role.id')),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'))
    )

    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('role.id')),
        relationship('Role', backref='users'),

        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('password', sa.String),
        sa.Column('first_name', sa.String(64), nullable=True, default=''),
        sa.Column('last_name', sa.String(64), nullable=True, default=''),
        sa.Column('email', sa.String),
        sa.Column('is_active', sa.Boolean, default=True)
    )

    op.create_table(
        'settings',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
        relationship('User', backref='settings'),
    )


def downgrade():
    op.drop_table(association_table)
    op.drop_table('group')
    op.drop_table('settings')
    op.drop_table('user')
    op.drop_table('role')

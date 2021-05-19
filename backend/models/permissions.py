from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base


association_table = Table('association_role_group', Base.metadata,
                          Column('role_id', Integer, ForeignKey('role.id')),
                          Column('group_id', Integer, ForeignKey('group.id')))


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    groups = relationship('Group', secondary=association_table, backref='roles', lazy='joined')


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))

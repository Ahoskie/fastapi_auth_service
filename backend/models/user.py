from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import EmailType, URLType

from database import Base
from models.permissions import Group, Role


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship('Role', backref='users')

    name = Column(String(64))
    password = Column(String)
    first_name = Column(String(64), nullable=True, default='')
    last_name = Column(String(64), nullable=True, default='')
    email = Column(EmailType)
    is_active = Column(Boolean, default=True)


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('settings', uselist=False))

    photo = Column(URLType)

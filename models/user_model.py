from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import base


class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    tg_id = Column(String(255), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False)
    id_role = Column(Integer,ForeignKey('roles.id', ondelete='SET DEFAULT'),default=1,nullable=False)
    role = relationship('Role', back_populates='users')


class Role(base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False, unique=True)
    users = relationship('User', back_populates='role')
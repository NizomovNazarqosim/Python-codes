from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from uuid import uuid4, UUID
from datetime import datetime


def generate_uuid():
    return str(uuid4())

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, default=generate_uuid, primary_key=True, index=True, nullable=False)
    name = Column(String(64))
    email = Column(String(128), unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    
    
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(String, default=generate_uuid, primary_key=True, index=True, nullable=False)
    title = Column(String(32))
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    user_id = Column(String,  ForeignKey('users.id'))
    
    
from app.db.session import Base
import datetime
from sqlalchemy import String, Integer, Boolean, Column, ForeignKey, DateTime, LargeBinary
from app.services.totp_service import make_totp_secret


class LoginMethod(Base):
    """
    Model for multi purpose auth type
    """
    __tablename__ = 'LoginMethod'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    image = Column(String(255))
    is_active = Column(Boolean, default=False)


class User(Base):
    """
    User Model with multi purpose auth type
    """
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String, nullable=True, unique=True)
    email = Column(String, nullable=True, unique=True)
    mobile_number = Column(String, nullable=True, unique=True)
    password = Column(String(100), nullable=False)
    totp_secret = Column(String(), default=make_totp_secret, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    login_method = Column(Integer, ForeignKey(
        "LoginMethod.id", ondelete='CASCADE'), nullable=False)
    face_encoding = Column(LargeBinary, nullable=True)


class LoginAttempt(Base):
    """
    Model for login attempet done by user
    """
    __tablename__ = 'LoginAttempt'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'))
    login_method_id = Column(Integer, ForeignKey(
        'LoginMethod.id', ondelete='CASCADE'))
    login_time = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Boolean)
    ip_address = Column(String, nullable=True)

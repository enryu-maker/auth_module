
from app.db.session import Base
from sqlalchemy import String, Integer, Boolean, Column, ForeignKey, DateTime


class Admin(Base):
    __tablename__ = 'Admin'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

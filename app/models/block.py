from app.db.session import Base
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime


class Block(Base):
    """
    Model for blockchain block.
    """
    __tablename__ = 'Block'

    id = Column(Integer, primary_key=True)  # Unique identifier
    index = Column(Integer, nullable=False)  # Index in the chain
    hash = Column(String(255), nullable=False)  # Hash of this block
    # Hash of the previous block
    previous_hash = Column(String(255), nullable=False)
    # Digital signature for this block
    signature = Column(String(255), nullable=False)

    # Foreign key linking the block to a user
    user_id = Column(Integer, ForeignKey(
        'User.id', ondelete='CASCADE'), nullable=False)

    # Timestamp of block creation
    created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Optional relationship to the user model
    # Assuming User model has blocks relationship
    user = relationship("User", back_populates="blocks")

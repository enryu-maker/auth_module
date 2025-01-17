from app.db.session import Base
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
import datetime


class ShareData(Base):
    """
    Model for blockchain data.
    """
    __tablename__ = 'BlockChain'

    # Unique identifier for each block
    id = Column(Integer, primary_key=True)

    # Foreign key linking to the User table
    user_id = Column(Integer, ForeignKey(
        'User.id', ondelete='CASCADE'), nullable=False)

    # Email associated with the block (add any constraints as needed)
    email = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)

    # Timestamp of block creation
    created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Data field for storing a list of blockchain information
    data = Column(JSON, nullable=False)

    # Relationship with the User table
    user = relationship("User")

    def __repr__(self):
        return f"<ShareData(id={self.id}, user_id={self.user_id}, email={self.email}, data={self.data})>"

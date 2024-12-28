from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BlockBase(BaseModel):
    """
    Base schema for a Block, shared fields.
    """
    index: int = Field(..., title="Block Index",
                       description="The position of the block in the chain.")
    hash: str = Field(..., max_length=255, title="Hash",
                      description="The hash of this block.")
    previous_hash: str = Field(..., max_length=255, title="Previous Hash",
                               description="The hash of the previous block.")
    signature: str = Field(..., max_length=255, title="Signature",
                           description="The digital signature of the block.")
    user_id: int = Field(..., title="User ID",
                         description="The ID of the user associated with this block.")


class BlockCreate(BlockBase):
    """
    Schema for creating a Block.
    """
    pass  # Inherits all required fields from BlockBase


class BlockUpdate(BaseModel):
    """
    Schema for updating a Block, all fields optional.
    """
    index: Optional[int] = Field(None, title="Block Index")
    hash: Optional[str] = Field(None, max_length=255, title="Hash")
    previous_hash: Optional[str] = Field(
        None, max_length=255, title="Previous Hash")
    signature: Optional[str] = Field(None, max_length=255, title="Signature")
    user_id: Optional[int] = Field(None, title="User ID")


class BlockResponse(BlockBase):
    """
    Schema for reading a Block, including additional fields.
    """
    id: int = Field(..., title="Block ID",
                    description="The unique identifier of the block.")
    created_at: datetime = Field(..., title="Creation Timestamp",
                                 description="The timestamp when the block was created.")

    class Config:
        orm_mode = True  # Enable ORM mode for seamless integration with SQLAlchemy models

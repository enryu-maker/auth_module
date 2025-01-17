from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime


class ShareDataSchema(BaseModel):
    """
    Pydantic schema for ShareData model.
    """
    id: int
    user_id: int
    email: str
    created_at: datetime
    data: List[Dict]  # List of dictionaries

    class Config:
        orm_mode = True  # Tells Pydantic to treat this model as an ORM model
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 101,
                "email": "user@example.com",
                "created_at": "2025-01-15T12:00:00",
                "data": [
                    {"transaction_id": "txn001", "amount": 100},
                    {"transaction_id": "txn002", "amount": 200}
                ]
            }
        }

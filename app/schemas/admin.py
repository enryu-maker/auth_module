from pydantic import BaseModel


class AdminRequest(BaseModel):
    """
        Schema for Admin Request
    """
    username: str
    password: str

from pydantic import BaseModel


class MethodRequest(BaseModel):
    """
    Request model for the method endpoint
    """
    name: str
    is_active: bool


class RegisterRequest(BaseModel):
    """
        Schema for RegisterRequest
    """
    name: str
    username: str
    email: str
    mobile_number: str
    password: str
    login_method: int
    face_image_base64: str


class LoginRequest(BaseModel):
    """
        Schema for LoginRequest
    """
    username: str
    password: str
    login_type: int


class VerifyRequest(BaseModel):
    """
        Schema for LoginRequest
    """
    username: str
    password: str
    login_type: int
    otp: int
    face_image_base64: str

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, RegisterRequest, VerifyRequest
from app.db.session import SessionLocale
from app.services.user_service import verify_user, check_user, hash_pass, Generate_OTP, verify_otp
from app.models.user import User, LoginAttempt


router = APIRouter(
    prefix="/v1/auth",
    tags=["v1 auth API"],
)


def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


db_depandancy = Annotated[Session, Depends(get_db)]


@router.post("/register")
async def register_user(registerrequest: RegisterRequest, db: db_depandancy):
    print(register_user)
    can_create = check_user(registerrequest, db)
    print(can_create)
    if can_create:
        new_user = User(
            username=registerrequest.username,
            email=registerrequest.email,
            password=hash_pass(registerrequest.password),
            name=registerrequest.name,
            login_method=registerrequest.login_method,
            mobile_number=registerrequest.mobile_number
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        raise HTTPException(
            status_code=201, detail="Account Created Sucessfully")


@router.post("/login")
async def login(loginrequest: LoginRequest, db: db_depandancy,):
    """
        username or email based login method
    """
    user = verify_user(loginrequest, db)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
    byte = Generate_OTP(user)
    return Response(content=byte, media_type="image/png")


@router.post("/verify", status_code=status.HTTP_201_CREATED)
async def verify_login(verifyrequest: VerifyRequest, db: db_depandancy):
    user = verify_user(verifyrequest, db)
    is_verified = verify_otp(user, verifyrequest.otp)
    if is_verified:
        return {"message": "Login Success"}
    else:
        raise HTTPException(
            status_code=401, detail="Invalid OTP")

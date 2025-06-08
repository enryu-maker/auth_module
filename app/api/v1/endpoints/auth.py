from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, RegisterRequest, VerifyRequest
from app.db.session import SessionLocale
from app.services.user_service import verify_user, check_user, hash_pass, Generate_OTP, verify_otp
from app.models.user import User, LoginAttempt
from app.services.aut_service import create_accesss_token, decode_access_token, get_face_encoding_from_base64
from datetime import timedelta
import numpy as np
import face_recognition
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
user_dependancy = Annotated[dict, Depends(decode_access_token)]


@router.post("/register")
async def register_user(registerrequest: RegisterRequest, db: db_depandancy):
    can_create = check_user(registerrequest, db)
    if not can_create:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        face_encoding = get_face_encoding_from_base64(
            registerrequest.face_image_base64)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    new_user = User(
        username=registerrequest.username,
        email=registerrequest.email,
        password=hash_pass(registerrequest.password),
        name=registerrequest.name,
        login_method=registerrequest.login_method,
        mobile_number=registerrequest.mobile_number,
        face_encoding=face_encoding
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    raise HTTPException(status_code=201, detail="Account Created Successfully")


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


@router.post("/verify/", status_code=status.HTTP_201_CREATED)
async def verify_login(verifyrequest: VerifyRequest, db: db_depandancy):
    # Step 1: Get user
    user = verify_user(verifyrequest, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 2: Optional Face Verification
    if verifyrequest.face_image_base64:
        try:
            if not user.face_encoding:
                raise HTTPException(
                    status_code=422, detail="Face data not registered for this user")

            known_encoding = np.frombuffer(
                user.face_encoding, dtype=np.float64)
            input_encoding = get_face_encoding_from_base64(
                verifyrequest.face_image_base64)

            is_face_match = face_recognition.compare_faces(
                [known_encoding], input_encoding)[0]
            if not is_face_match:
                raise HTTPException(
                    status_code=401, detail="Face verification failed")
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    # Step 3: OTP Verification
    is_verified = verify_otp(user, verifyrequest.otp)
    if is_verified:
        access = create_accesss_token(user.name, user.id, timedelta(days=90))
        return {
            "message": "Login Success",
            "access_token": access
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid OTP")


@router.get("/profile/",)
async def read_users(user: user_dependancy, db: Session = Depends(get_db)):
    print(user)
    db_user = db.query(User).filter(User.id == user['user_id']).first()
    print(db_user)
    if db_user:
        return db_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

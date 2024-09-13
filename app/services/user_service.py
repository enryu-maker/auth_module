
from jose import JWTError, jwt
from app.models.user import User, LoginAttempt
from sqlalchemy import or_
from passlib.context import CryptContext
from fastapi import HTTPException
import pyotp
import qrcode
import io
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_pass(password: str):
    return bcrypt_context.hash(password)


def verify_user(loginrequest, db):
    """
    Function for verifying user credentials
    """
    user = db.query(User).filter(
        or_(User.username == loginrequest.username, User.email == loginrequest.username)).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt_context.verify(loginrequest.password, user.password):
        failattempt = LoginAttempt(
            user_id=user.id,
            login_method_id=loginrequest.login_type,
            status=False,
            ip_address="127.0.0.1"
        )
        db.add(failattempt)
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid Password")
    successattempt = LoginAttempt(
        user_id=user.id,
        login_method_id=loginrequest.login_type,
        status=True,
        ip_address="127.0.0.1"
    )
    db.add(successattempt)
    db.commit()
    return user


def check_user(registerrequest, db):
    """
    Function for checking if user already exists
    """
    user = db.query(User).filter(
        or_(User.username == registerrequest.username, User.email == registerrequest.email)).first()

    if user:
        raise HTTPException(
            status_code=400, detail="Username or Email already exists")
    return True


def Generate_OTP(user):
    qr_code = qrcode.make(
        pyotp.totp.TOTP(user.totp_secret).provisioning_uri(
            name=user.email, issuer_name="www.sharify.com")
    )
    img_byte_arr = io.BytesIO()
    qr_code.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def verify_otp(user, otp):
    return pyotp.TOTP(user.totp_secret).verify(otp)

from jose import JWTError, jwt
from app.models.admin import Admin
from sqlalchemy import or_
from passlib.context import CryptContext
from fastapi import HTTPException

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_user(registerrequest, db):
    """
    Function for checking if admin already exists
    """
    user = db.query(Admin).filter(
        Admin.username == registerrequest.username
    ).first()

    if user:
        raise HTTPException(
            status_code=400, detail="Username exists")
    return True


def verify_user(loginrequest, db):
    """
    Function for verifying admin credentials
    """
    user = db.query(Admin).filter(Admin.username ==
                                  loginrequest.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt_context.verify(loginrequest.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Password")
    return user

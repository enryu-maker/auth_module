import datetime
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from typing import Annotated
from passlib.context import CryptContext
import face_recognition
import base64
import numpy as np
from io import BytesIO
from PIL import Image

load_dotenv()


SECRET_KEY = "e15a39ceb9a4d577df8cc72c2e4462c980fb1459f16af8bbbe92d900e79a0934"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/api/user/verify-user')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_pass(password: str):
    return bcrypt_context.hash(password)


def verify_user(loginrequest, db, Model):
    """
    Function for verifying user credentials
    """
    user = db.query(Model).filter(
        Model.email == loginrequest.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt_context.verify(loginrequest.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Password")
    return user


def create_accesss_token(name: str, user_id: int, expiry: timedelta):
    encode = {
        'sub':  name,
        'id': user_id
    }
    expires = datetime.datetime.utcnow() + expiry
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get('sub')
        user_id: int = payload.get('id')
        if name is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid access token")
        return {
            'name': name,
            'user_id': user_id
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")


def get_face_encoding_from_base64(base64_str: str) -> bytes:
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data)).convert("RGB")
    image_np = np.array(image)

    face_encodings = face_recognition.face_encodings(image_np)

    if not face_encodings:
        raise ValueError("No face found in the image.")

    # Serialize encoding
    return face_encodings[0].tobytes()

from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException,  File, UploadFile, Form
from sqlalchemy.orm import Session
from app.models.user import LoginMethod, User, LoginAttempt
from app.schemas.admin import AdminRequest
from app.db.session import SessionLocale
from app.services.admin_service import check_user, verify_user
from app.services.user_service import hash_pass
from app.models.admin import Admin
import os
from uuid import uuid4

IMAGE_UPLOAD_DIR = os.path.join(os.getcwd(), 'static', 'images')
os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)
BASE_URL = 'http://127.0.0.1:8000/images/'

router = APIRouter(
    prefix="/v1/admin",
    tags=["v1 Admin API"],
)


def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


db_depandancy = Annotated[Session, Depends(get_db)]


@router.get('/get_all_user')
async def get_all_user(db: db_depandancy):
    user = db.query(User).all()
    return user


@router.get('/get_all_login_attempt')
async def get_all(db: db_depandancy):
    user = db.query(LoginAttempt).all()
    return user


@router.delete("/delete-user")
async def delete_user(db: db_depandancy, id: int):
    # delete user
    try:
        # Query the database to find the record with the given id
        user_to_delete = db.query(User).filter(
            User.id == id).first()

        if user_to_delete is None:
            raise HTTPException(status_code=404, detail="Method not found")

        # Delete the record
        db.delete(user_to_delete)
        db.commit()

        return {"status": "success", "message": "User deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error deleting method: {str(e)}")


@router.post('/register-admin')
async def create_admin(registerrequest: AdminRequest, db: db_depandancy):
    can_create = check_user(registerrequest, db)
    if can_create:
        new_user = Admin(
            username=registerrequest.username,
            password=hash_pass(registerrequest.password),

        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        raise HTTPException(
            status_code=201, detail="Account Created Sucessfully")


@router.post("/login")
async def login(loginrequest: AdminRequest, db: db_depandancy,):
    """
        username or email based login method
    """
    user = verify_user(loginrequest, db)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
    return {
        "message": "Login Success",
        "data": {
            "access": user.id
        }

    }


@router.get('/get_all_methods')
async def get_all(db: db_depandancy):
    method = db.query(LoginMethod).all()
    return method


@router.delete('/delete-method')
async def delete(db: db_depandancy, id: int):
    try:
        # Query the database to find the record with the given id
        method_to_delete = db.query(LoginMethod).filter(
            LoginMethod.id == id).first()

        if method_to_delete is None:
            raise HTTPException(status_code=404, detail="Method not found")

        # Delete the record
        db.delete(method_to_delete)
        db.commit()

        return {"status": "success", "message": "Method deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error deleting method: {str(e)}")


@router.post('/create_method')
async def create_method(name: str = Form(...),  # Use Form for non-file fields
                        is_active: bool = Form(False),
                        # Use File for the image upload
                        image: UploadFile = File(...),
                        db: Session = Depends(get_db)):
    try:
        new_method = LoginMethod(name=name, is_active=is_active)

        # If an image is uploaded, save it to the file system and store the URL
        if image:
            # Unique file name
            filename = f"{uuid4()}.{image.filename.split('.')[-1]}"
            filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(await image.read())

            # Generate the URL to access the uploaded image
            image_url = f"{BASE_URL}{filename}"
            new_method.image = image_url  # Store the image URL in the database

        db.add(new_method)
        db.commit()
        db.refresh(new_method)

        return {"status": "success", "method": new_method}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error creating method: {str(e)}")


@router.put('/toggle-method/{id}')
async def toggle_method(db: db_depandancy, id: int):
    try:
        # Fetch the login method by ID
        method_to_toggle = db.query(LoginMethod).filter(
            LoginMethod.id == id).first()

        if method_to_toggle:
            # Toggle the is_active status
            method_to_toggle.is_active = not method_to_toggle.is_active
            db.commit()
            # Refresh to return the updated method
            db.refresh(method_to_toggle)
            return {
                "status": "success",
                "message": "Method toggled successfully",
                "method": {
                    "id": method_to_toggle.id,
                    "name": method_to_toggle.name,
                    "is_active": method_to_toggle.is_active
                }
            }
        else:
            # Return a 404 if the method is not found
            raise HTTPException(status_code=404, detail="Method not found")
    except Exception as e:
        # Rollback in case of any error
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error toggling method: {str(e)}"
        )

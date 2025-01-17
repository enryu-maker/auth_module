from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.schemas.block import ShareDataSchema
from app.db.session import SessionLocale
from app.models.block import ShareData
from app.models.user import User
from app.services.aut_service import decode_access_token


router = APIRouter(
    prefix="/v1/sharedata",
    tags=["v1 Share API"],
)


def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


db_depandancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(decode_access_token)]


@router.post("/share/")
async def create_sharedata(user: user_dependancy, body: Dict, db: db_depandancy):
    db_user = db.query(User).filter(User.id == user['user_id']).first()
    if db_user:
        try:
            # Extract data from the body dictionary
            # Default to user_id from the token
            user_id = body.get('user_id', user['user_id'])
            email = body.get('email', '')
            data = body.get('data', [])
            file_name = body.get('file_name', '')

            # Log the extracted values for debugging
            print(f"User ID: {user_id}, Email: {email}, Data: {data}")

            # Create a new Block entry
            new_block = ShareData(
                user_id=user_id,
                email=email,
                data=data,
                file_name=file_name
            )
            db.add(new_block)
            db.commit()
            db.refresh(new_block)
            return {"message": "Data received", "data": body}
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the data."
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.get("/get-files/")
async def get_file(user: user_dependancy, db: db_depandancy):
    """
    API to retrieve file data for the authenticated user, sorted by created_at.

    :param user: The authenticated user details (from JWT).
    :param db: Database session dependency.
    :return: JSON response with sorted file data.
    """

    # Fetch the user from the database
    db_user = db.query(User).filter(User.id == user['user_id']).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

        # Fetch and sort files by created_at in descending order (latest first)
    files = (
        db.query(ShareData)
        .filter(ShareData.email == db_user.email)
        .order_by(ShareData.created_at.desc())
        .all()
    )

    if not files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No files found for the user."
        )

    result = []
    for file in files:
        user_secret = db.query(User).filter(
            User.id == file.user_id).first()
        result.append({
            "id": file.id,
            "user_id": file.user_id,
            "email": file.email,
            "file_name": file.file_name,
            "created_at": file.created_at,
            "data": file.data,
            "top_secret": user_secret.totp_secret
        })

    return {"message": "Files retrieved successfully", "files": result}


@router.get("/get-shared-files/")
async def get_file(user: user_dependancy, db: db_depandancy):
    """
    API to retrieve file data for the authenticated user, sorted by created_at.

    :param user: The authenticated user details (from JWT).
    :param db: Database session dependency.
    :return: JSON response with sorted file data.
    """

    # Fetch the user from the database
    db_user = db.query(User).filter(User.id == user['user_id']).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

        # Fetch and sort files by created_at in descending order (latest first)
    files = (
        db.query(ShareData)
        .filter(ShareData.user_id == db_user.id)
        .order_by(ShareData.created_at.desc())
        .all()
    )

    if not files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No files found for the user."
        )

    result = []
    for file in files:
        user_secret = db.query(User).filter(
            User.id == file.user_id).first()
        result.append({
            "id": file.id,
            "user_id": file.user_id,
            "email": file.email,
            "file_name": file.file_name,
            "created_at": file.created_at,
            "data": file.data,
            "top_secret": user_secret.totp_secret
        })

    return {"message": "Files retrieved successfully", "files": result}

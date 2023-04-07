import sys

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

sys.path.append("..")
import models  # noqa: E402
from database import get_db  # noqa: E402

from .auth import get_current_user, get_password_hash  # noqa: E402

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)


class NewPassword(BaseModel):
    new_password: str


@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    """
    Returns all users in the application
    """
    return db.query(models.Users).all()


@router.get("/user")
async def get_single_user_by_query_param(user_id: int, db: Session = Depends(get_db)):
    """
    Returns a single user for the given user_id using path parameter
    """
    return get_user(user_id, db)


@router.get("/{user_id}")
async def get_single_user_by_path_param(user_id: int, db: Session = Depends(get_db)):
    """
    Returns a single user for the given user_id using query parameter
    """
    return get_user(user_id, db)


@router.put("/change_password")
async def change_password(
    new_password: NewPassword,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Allows a user to change their password
    """
    user_model = get_user(user.get("id"), db)
    user_model.hashed_password = get_password_hash(new_password.new_password)
    db.add(user_model)
    db.commit()
    return successful_response(200)


@router.delete("/")
async def delete_me(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Deletes the logged in user
    """
    # First delete all todos for the user
    db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).delete()

    db.query(models.Users).filter(models.Users.id == user.get("id")).delete()
    db.commit()
    return successful_response(200)


def get_user(user_id: int, db: Session) -> models.Users:
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is None:
        raise http_exception()
    return user_model


def successful_response(status_code: int):
    return {"status": status_code, "transaction": "Successful"}


def http_exception():
    return HTTPException(status_code=404, detail="User not found")

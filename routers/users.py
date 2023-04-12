import sys
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

sys.path.append("..")
import models  # noqa: E402

from .auth import get_current_user, get_password_hash  # noqa: E402

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://mustansir:12345678@localhost/todos"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)
async_local_session = sessionmaker(bind=async_engine, class_=AsyncSession)


# @asynccontextmanager
async def get_db():
    try:
        session = async_local_session
        async with session() as db:
            yield db
    except Exception:
        await db.rollback()
    finally:
        await db.close()


router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)


class NewPassword(BaseModel):
    new_password: str


@router.get("/")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """
    Returns all users in the application
    """
    async with db:
        q = await db.execute(select(models.Users).order_by(models.Users.id))
        return q.scalars().all()


@router.get("/user")
async def get_single_user_by_query_param(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Returns a single user for the given user_id using path parameter
    """
    async with db:
        return await get_user(user_id, db)


@router.get("/{user_id}")
async def get_single_user_by_path_param(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Returns a single user for the given user_id using query parameter
    """
    async with db:
        return await get_user(user_id, db)


@router.put("/change_password")
async def change_password(
    new_password: NewPassword,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Allows a user to change their password
    """
    async with db:
        user_model = await get_user(user.get("id"), db)
        user_model.hashed_password = get_password_hash(new_password.new_password)
        db.add(user_model)
        await db.commit()
        return successful_response(200)


@router.delete("/")
async def delete_me(
    user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    Deletes the logged in user
    """
    async with db:
        # First delete all todos for the user
        await db.execute(
            delete(models.Todos).where(models.Todos.owner_id == user.get("id"))
        )
        await db.execute(delete(models.Users).where(models.Users.id == user.get("id")))
        await db.commit()
        return successful_response(200)


async def get_user(user_id: int, db: AsyncSession) -> models.Users:
    q = await db.execute(select(models.Users).where(models.Users.id == user_id))
    user_model = q.scalar_one()
    if user_model is None:
        raise http_exception()
    return user_model


def successful_response(status_code: int):
    return {"status": status_code, "transaction": "Successful"}


def http_exception():
    return HTTPException(status_code=404, detail="User not found")

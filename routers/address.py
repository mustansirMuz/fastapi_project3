import sys
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

sys.path.append("..")
import models  # noqa: E402
from database import engine, get_db  # noqa: E402

from .auth import get_current_user, get_user_exception  # noqa: E402

router = APIRouter(
    prefix="/address", tags=["address"], responses={404: {"description": "Not found"}}
)


class Address(BaseModel):
    address1: str
    address2: str
    city: str
    state: str
    country: str
    postalcode: str
    apt_num: Optional[int]


@router.post("/")
async def create_address(
    address: Address,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create an address for the logged in user
    """
    address_model = models.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode
    address_model.apt_num = address.apt_num

    db.add(address_model)
    db.flush()

    user_model = (
        db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    )

    user_model.address_id = address_model.id

    db.add(user_model)
    db.commit()

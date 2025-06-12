from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.models.office_user_model import OfficeUserCreate, OfficeUserDB
from app.database import (
    office_user_collection,
    find_office_user_by_username,
    insert_user,
)
from app.services.office_user_service import create_office_user
from app.core import security
from app.constants import ADMIN_ROLE

router = APIRouter(prefix="/admin", tags=["Admin"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/create-office-user")
async def create_office_user(user: OfficeUserCreate):
    if await find_office_user_by_username(user.id):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = security.hash_password(user.password)
    new_user = OfficeUserDB(
        id=user.id,
        role=user.role,
        hashed_password=hashed_password,
        is_active=True,
    )
    result = await insert_user(new_user)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return {"id": str(result.inserted_id), "message": "Office user created"}


@router.delete("/terminate-office-user/{user_id}")
def terminate_office_user(user_id: str):
    result = office_user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Office user not found")
    return {"message": "Office user terminated"}


@router.post("/backup")
def perform_backup():
    return {"message": "Backup triggered (stub)"}


@router.post("/restore")
def perform_restore():
    return {"message": "Restore initiated (stub)"}


@router.post("/add-parish")
def add_parish(parish_name: str):
    return {"message": f"Parish '{parish_name}' added (stub)"}

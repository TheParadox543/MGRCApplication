from passlib.context import CryptContext
from app.models.office_user_model import OfficeUserCreate, OfficeUserDB, OfficeUserBase
from app.database import office_user_collection
from fastapi import HTTPException
from app.core.security import hash_password


async def create_office_user(user_data: OfficeUserCreate):
    """Create a new office user with hashed password and save to DB."""
    hashed_pw = hash_password(user_data.password)

    # Create the DB model (with hashed password)
    user_db = OfficeUserDB(
        user_id=user_data.user_id,
        role=user_data.role,
        is_active=user_data.is_active,
        hashed_password=hashed_pw,
    )

    # Insert into the MongoDB collection
    result = await office_user_collection.insert_one(user_db.model_dump(by_alias=True))
    return result.inserted_id  # Returning the inserted document ID


async def get_office_user(user_id: str):
    """Fetch user details from the database by user_id."""
    doc = await office_user_collection.find_one({"_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert to OfficeUserDB model to access all fields, then return the public info
    user = OfficeUserDB(**doc)

    # Return public model without sensitive data (hashed password)
    return OfficeUserBase(**user.user_dump())  # Excludes hashed_password

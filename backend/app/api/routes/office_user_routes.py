from fastapi import APIRouter, HTTPException, status, Depends
from app.models.office_user_model import OfficeUserCreate, OfficeUserBase
from app.database import office_user_collection
from app.core import security
from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/office_users", tags=["Office Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_office_user(token: str = Depends(oauth2_scheme)):
    payload = security.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user = office_user_collection.find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
    }


@router.post("/login")
def login(form_data: OfficeUserCreate):
    user = office_user_collection.find_one({"email": form_data.email})
    if not user or not security.verify_password(
        form_data.password, user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = security.create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def read_office_users_me(current_user: dict = Depends(get_current_office_user)):
    return current_user

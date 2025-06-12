from pydantic import BaseModel, Field


class OfficeUserBase(BaseModel):
    id: str = Field(..., min_length=3, max_length=50)
    role: str
    is_active: bool = True

    class Config:
        validate_by_name = True
        from_attributes = True

    def model_dump(self, **kwargs):
        obj_dict = super().model_dump(**kwargs)
        obj_dict["_id"] = obj_dict.pop("id")
        return obj_dict


class OfficeUserDB(OfficeUserBase):
    hashed_password: str


class OfficeUserCreate(OfficeUserBase):
    password: str

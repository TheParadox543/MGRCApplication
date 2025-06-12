from pydantic import BaseModel, Field


class LifeMemberBase(BaseModel):
    life_member_id: int = Field(alias="_id")
    name: str
    display_name: str 
    address: str
    parish: str
    phone: list[str]
    email: str
    aadhar_number: str
    pan: str
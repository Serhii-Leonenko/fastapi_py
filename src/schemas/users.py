from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreateSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    created_at: datetime

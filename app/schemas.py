from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr, validator
from bson.objectid import ObjectId


class UserBaseSchema(BaseModel):
    name: str
    email: str
    photo: str
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class FilteredUserResponse(UserBaseSchema):
    id: str


class ObjectIdField(str):
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string", format="ObjectId")


class HolidayBaseSchema(BaseModel):
    name: str
    date: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class HolidayResponseSchema(HolidayBaseSchema):
    id: str


class HolidayResponse(BaseModel):
    status: str
    holiday: HolidayResponseSchema


class FilteredHolidayResponse(HolidayBaseSchema):
    id: str

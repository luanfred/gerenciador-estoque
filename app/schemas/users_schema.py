from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class UsersSchemaBase(BaseModel):
    name: str
    email: EmailStr
    password: str


class UsersSchemaResponse(UsersSchemaBase):
    id: int
    created_at: datetime


class UsersSchemaCreate(UsersSchemaBase):
    @field_validator('name')
    def validate_name_length(cls, name):
        if len(name) > 50:  # noqa
            raise ValueError('Name must be less than 50 characters')
        return name

    @field_validator('email')
    def validate_email_length(cls, email):
        if len(email) > 50:  # noqa
            raise ValueError('Email must be less than 50 characters')
        return email

    @field_validator('password')
    def validate_password_length(cls, password):
        if len(password) > 50:  # noqa
            raise ValueError('Password must be less than 50 characters')
        return password


class UsersSchemaUpdate(UsersSchemaBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

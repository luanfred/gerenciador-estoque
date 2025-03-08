from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class UsersSchemaResponse(BaseModel):
    id: int | None
    name: str
    email: str
    password: str
    created_at: datetime


class UsersSchemaCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

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

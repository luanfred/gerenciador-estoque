from datetime import datetime

from pydantic import BaseModel


class UsersSchema(BaseModel):
    id: int | None
    name: str
    email: str
    password: str
    created_at: datetime

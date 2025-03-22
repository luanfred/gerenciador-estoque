from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50), unique=True)
    email: Mapped[str] = mapped_column(String(length=50), unique=True)
    password: Mapped[str] = mapped_column(String(length=256))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), init=False)

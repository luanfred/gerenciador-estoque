from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.users_model import UsersModel


class ProductModel(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50), unique=True)
    description: Mapped[str] = mapped_column(String(length=256))
    provider: Mapped[str | None] = mapped_column(String(length=50), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(length=30), nullable=True)
    size: Mapped[str | None] = mapped_column(String(length=6), nullable=True)
    photo_link: Mapped[str | None] = mapped_column(String(length=256), nullable=True)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)

    # chava estrangeira de users
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped[Optional[UsersModel]] = relationship(
        'UsersModel',
        init=False,
    )

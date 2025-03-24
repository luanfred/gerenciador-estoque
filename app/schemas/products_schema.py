from typing import Union

from pydantic import BaseModel


class ProductSchemaBase(BaseModel):
    name: str
    description: str
    provider: Union[str, None] = None
    brand: Union[str, None] = None
    size: Union[str, None] = None
    photo_link: Union[str, None] = None
    price: float
    quantity: int


class ProductSchemaCreate(ProductSchemaBase):
    pass


class ProductSchemaResponse(ProductSchemaBase):
    id: int

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import db_dependency
from app.models.products_model import ProductModel
from app.models.users_model import UsersModel
from app.schemas.products_schema import ProductSchemaCreate, ProductSchemaResponse

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProductSchemaResponse,
)
def create_product(
    product: ProductSchemaCreate,
    db: Session = db_dependency,
    current_user: UsersModel = Depends(get_current_user),
):
    new_product = ProductModel(
        name=product.name,
        description=product.description,
        provider=product.provider,
        brand=product.brand,
        size=product.size,
        photo_link=product.photo_link,
        price=product.price,
        quantity=product.quantity,
        user_id=current_user.id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[ProductSchemaResponse],
)
def get_all_products(
    db: Session = db_dependency, current_user: UsersModel = Depends(get_current_user)
):
    products = db.query(ProductModel).filter(ProductModel.user_id == current_user.id).all()
    return products


@router.get(
    '/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductSchemaResponse,
)
def get_product_by_id(
    product_id: int,
    db: Session = db_dependency,
    current_user: UsersModel = Depends(get_current_user),
):
    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id, ProductModel.user_id == current_user.id)
        .first()
    )
    if product:
        return product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')


@router.put(
    '/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductSchemaResponse,
)
def update_product(
    product_id: int,
    product: ProductSchemaCreate,
    db: Session = db_dependency,
    current_user: UsersModel = Depends(get_current_user),
):
    existing_product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id, ProductModel.user_id == current_user.id)
        .first()
    )
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.provider = product.provider
    existing_product.brand = product.brand
    existing_product.size = product.size
    existing_product.photo_link = product.photo_link
    existing_product.price = product.price
    existing_product.quantity = product.quantity

    db.commit()
    db.refresh(existing_product)

    return existing_product


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = db_dependency,
    current_user: UsersModel = Depends(get_current_user),
):
    existing_product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id, ProductModel.user_id == current_user.id)
        .first()
    )
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    db.delete(existing_product)
    db.commit()

from fastapi import APIRouter

from .endpoints.products import router as products_router
from .endpoints.users import router as users_router

api_router = APIRouter()

api_router.include_router(users_router, prefix='/users', tags=['Usuários'])
api_router.include_router(products_router, prefix='/products', tags=['Produtos'])

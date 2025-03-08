from fastapi import APIRouter

from .endpoints.users import router

api_router = APIRouter()

api_router.include_router(router, prefix='/users', tags=['Usuários'])

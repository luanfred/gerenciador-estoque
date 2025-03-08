from fastapi import FastAPI

from app.api.api import api_router

app = FastAPI(
    title='Gerenciador de Estoque',
    description='API para gerenciamento de estoque',
)

app.include_router(api_router)

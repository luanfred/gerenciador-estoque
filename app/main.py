from http import HTTPStatus

from fastapi import FastAPI

from app.core.deps import create_all_tables
from app.schemas.users_schema import UsersSchema

app = FastAPI()

create_all_tables()


@app.get('/', status_code=HTTPStatus.OK, response_model=UsersSchema)
def read_root():
    user = UsersSchema(name='Hello', email='World', password='123456')
    return user

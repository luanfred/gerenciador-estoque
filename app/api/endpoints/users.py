from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user, create_access_token, get_current_user
from app.core.database import db_dependency
from app.core.security import Security
from app.models.users_model import UsersModel
from app.schemas.users_schema import UsersSchemaCreate, UsersSchemaResponse, UsersSchemaUpdate
from app.services.validate_user_exists import (
    validate_user_exists,
    validate_user_exists_excluded_authenticated,
)

router = APIRouter()


@router.post('/register/', status_code=status.HTTP_201_CREATED, response_model=UsersSchemaResponse)
def create_user(user: UsersSchemaCreate, db: Session = db_dependency):
    user_exists = validate_user_exists(user.name, user.email, db)

    if user_exists['exists']:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User already registered with this {user_exists["field"]}',
        )

    user.password = Security.create_hash_password(user.password)
    new_user = UsersModel(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login/', status_code=status.HTTP_200_OK)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(str(user.id))
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get(
    '/{user_id}/',
    status_code=status.HTTP_200_OK,
    response_model=UsersSchemaResponse,
    dependencies=[Depends(get_current_user)],
)
def get_user_by_id(user_id: int, db: Session = db_dependency):
    user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.put(
    '/{user_id}/',
    status_code=status.HTTP_200_OK,
    response_model=UsersSchemaResponse,
    dependencies=[Depends(get_current_user)],
)
def update_user(user_id: int, user: UsersSchemaUpdate, db: Session = db_dependency):
    user_to_update = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    if user_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    user_exists = validate_user_exists_excluded_authenticated(user.name, user.email, db, user_id)
    if user_exists['exists']:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User already registered with this {user_exists["field"]}',
        )

    if user.name:
        user_to_update.name = user.name
    if user.email:
        user_to_update.email = user.email
    if user.password:
        user_to_update.password = Security.create_hash_password(user.password)

    db.commit()
    db.refresh(user_to_update)
    return user_to_update


@router.delete(
    '/{user_id}/', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)]
)
def delete_user(user_id: int, db: Session = db_dependency):
    user_to_delete = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    db.delete(user_to_delete)
    db.commit()

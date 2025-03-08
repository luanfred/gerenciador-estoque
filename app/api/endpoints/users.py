from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import db_dependency
from app.models.users_model import UsersModel
from app.schemas.users_schema import UsersSchemaCreate, UsersSchemaResponse

router = APIRouter()


@router.post('/register/', status_code=status.HTTP_201_CREATED, response_model=UsersSchemaResponse)
def create_user(user: UsersSchemaCreate, db: Session = db_dependency):
    try:
        new_user = UsersModel(name=user.name, email=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print('Error: ', e)
        db.rollback()
        user_is_registered = (
            db.query(UsersModel)
            .filter((UsersModel.email == user.email) | (UsersModel.name == user.name))
            .first()
        )
        if user_is_registered:
            if user_is_registered.email == user.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Email already registered',
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Name already registered',
            )


@router.get('/{user_id}/', status_code=status.HTTP_200_OK, response_model=UsersSchemaResponse)
def get_user_by_id(user_id: int, db: Session = db_dependency):
    user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[UsersSchemaResponse])
def get_all_users(db: Session = db_dependency):
    users = db.query(UsersModel).all()
    if users:
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No users found')


@router.put('/{user_id}/', status_code=status.HTTP_200_OK, response_model=UsersSchemaResponse)
def update_user(user_id: int, user: UsersSchemaCreate, db: Session = db_dependency):
    user_to_update = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    if user_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    user_to_update.name = user.name
    user_to_update.email = user.email
    user_to_update.password = user.password
    db.commit()
    db.refresh(user_to_update)
    return user_to_update


@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = db_dependency):
    user_to_delete = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    db.delete(user_to_delete)
    db.commit()

from datetime import datetime, timedelta

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from pydantic import EmailStr
from pytz import timezone
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.users_model import UsersModel
from app.schemas.token_data import TokenData

from .configs import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET
from .database import get_session
from .security import Security

auth2_schema = OAuth2PasswordBearer(tokenUrl='/users/login/')


def authenticate_user(email: EmailStr, password: str, db: Session):
    with db:
        user = db.execute(select(UsersModel).filter(UsersModel.email == email)).scalar_one_or_none()

        if not user:
            return None

        if not Security.verify_password(password, user.password):
            return None

        return user


def _create_token(type_token: str, expires_delta: timedelta, sub: str):
    payload = {}
    sp = timezone('America/Sao_Paulo')
    expires = datetime.now(sp) + expires_delta
    payload.update({
        'type': type_token,
        'exp': expires,
        'iat': datetime.now(sp),
        'sub': sub,
    })
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_access_token(sub: str):
    return _create_token(
        type_token='access', expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), sub=sub
    )


def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(auth2_schema)
) -> UsersModel:
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM], options={'verify_aud': False}
        )
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWSError:
        raise credentials_exception

    query = select(UsersModel).filter(UsersModel.id == int(token_data.username))
    result = db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

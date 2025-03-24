from sqlalchemy.orm import Session

from app.models.users_model import UsersModel


def validate_user_exists(name: str | None, email: str | None, db: Session) -> dict:
    user_is_registered = (
        db.query(UsersModel).filter((UsersModel.email == email) | (UsersModel.name == name)).first()
    )
    if user_is_registered:
        if user_is_registered.email == email:
            return {
                'exists': True,
                'field': 'email',
            }
        else:
            return {
                'exists': True,
                'field': 'name',
            }
    return {
        'exists': False,
        'field': None,
    }


def validate_user_exists_excluded_authenticated(
    name: str | None, email: str | None, db: Session, user_id: int
) -> dict:
    user_is_registered = (
        db.query(UsersModel)
        .filter((UsersModel.email == email) | (UsersModel.name == name))
        .filter(UsersModel.id != user_id)
        .first()
    )
    if user_is_registered:
        if user_is_registered.email == email:
            return {
                'exists': True,
                'field': 'email',
            }
        else:
            return {
                'exists': True,
                'field': 'name',
            }
    return {
        'exists': False,
        'field': None,
    }

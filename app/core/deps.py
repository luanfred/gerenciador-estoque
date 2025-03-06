from fastapi import Depends

from .database import Base, SessionLocal, engine


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Depends(get_session)


def create_all_tables():
    import app.models.all_models  # noqa

    Base.metadata.create_all(bind=engine)
    print('Todas as tabelas foram criadas com sucesso!')

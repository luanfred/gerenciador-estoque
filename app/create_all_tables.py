from app.core.database import Base, engine


def create_all_tables():
    import app.models.all_models  # noqa

    Base.metadata.create_all(bind=engine)
    print('Todas as tabelas foram criadas com sucesso!')


if __name__ == '__main__':
    create_all_tables()

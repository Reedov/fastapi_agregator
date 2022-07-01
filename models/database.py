""" подключние к БД """

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from settings import settings

engine = create_engine(settings.db_host, connect_args={'check_same_thread': False})

Session = sessionmaker(engine, autocommit=False, autoflush=False)


def create_tables():
    """первоначальное создание таблиц из моделей """
    meta = MetaData()
    meta.create_all(bind=engine)


def get_session() -> Session:
    """ генератор создаия сессии подключения к БД """
    session = Session()
    try:
        yield session
    finally:
        session.close()

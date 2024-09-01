"""TODO: нужно добавить функцию для инициализации
параметров из окружения."""

from typing import Any, Generator
from logging import getLogger
from functools import lru_cache

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


logger = getLogger(__name__)


def init_dependencies(app: FastAPI) -> None:
    pass


@lru_cache(maxsize=None)
def get_engine() -> Engine:
    return create_engine(
        # os.getenv('SQLALCHEMY_DATABASE_URL'),
        'mysql+pymysql://ipanov:ipanov@127.0.0.1/tg_stat',
        pool_pre_ping=True,
    )


def new_session() -> Generator[Session, None, Any]:
    session_maker = sessionmaker(bind=get_engine())
    session = session_maker()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

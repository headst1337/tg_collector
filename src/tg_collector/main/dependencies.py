import os
from typing import Any, Generator
from logging import getLogger
from functools import lru_cache

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from tg_collector.adapters.sqlalchemy_db.models import (
    metadata_obj,
    mapper_registry,
)

logger = getLogger(__name__)


def init_dependencies(app: FastAPI) -> None:
    pass

@lru_cache(maxsize=None)
def get_engine() -> Engine:
    return create_engine(
        #os.getenv('SQLALCHEMY_DATABASE_URL'),
        'mysql+pymysql://devops:0ZRHrpTQVgc3z1cR@85.234.107.240/dev',
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

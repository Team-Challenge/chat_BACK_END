from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./chat.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
    # def __repr__(self):
    #     if hasattr(self, "id"):
    #         return '<%s: id=%r>' % (type(self).__name__, self.id)
    #     return DeclarativeBase.__repr__(self)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dbDep = Annotated[get_db, Depends()]

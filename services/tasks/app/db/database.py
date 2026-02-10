from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from app import settings
from app.models import Base
from typing import Iterator


engine = create_engine(settings.DB_URL, pool_pre_ping=True)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db_session() -> Iterator[Session]:
    db = sessionLocal()
    
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Transaction Failed: {e}")
    finally:
        db.close()
    
    


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()

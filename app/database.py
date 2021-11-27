from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .creds import PASSWORD, USERNAME

SQL_ALCHEMY_DATABASE = f"postgresql://{USERNAME}:{PASSWORD}@localhost/api"

engine = create_engine(SQL_ALCHEMY_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

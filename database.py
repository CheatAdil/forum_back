from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from my_package.environment_variables import get_var
SQLALCHEMY_DATABASE_URL = get_var("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

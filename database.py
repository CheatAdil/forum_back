from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres_user:UHJAEIDFPRbrNkW1xxb3imDgWw3PHgru@dpg-cpo2c7lds78s73b90al0-a.oregon-postgres.render.com/postgres_db_19w1'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = {
    "johndoe": {
        "user_id": "4",
        "user_name": "johndoe",
        "user_password": "$2b$12$nEJAhpawf5bjcIY5VqwWn.HGFGVeDPd75GnIg4/Ec9fmoOPGAquxi",
        "user_email": "johndoe@example.com"
    }
}
from sqlalchemy.orm import Session

from .entities import models

def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.user_email == user_email).first()

print("auth")


# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 
 
# accessing and printing value
print("SECRET_KEY = " + str(os.getenv("SECRET_KEY")))


from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from sqlalchemy.orm import Session

from . import schemas, auth
from .crud import get_user_by_email


import jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError

from .database import SessionLocal

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        print("got db")
        yield db
    finally:
        db.close()

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, user_password):
    print("plain password = " + str(plain_password))
    print("user password = " + str(user_password))
    return pwd_context.verify(plain_password, user_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, user_name: str, ):
    
    if get_user_by_email(db, user_email=user_name):
        user_dict = db[user_name]
        return schemas.User(**user_dict)


def authenticate_user(db_user, user_name: str, password: str):

    print("works")
    #user = get_user(db, user_name)

    if not db_user:
        print("not user")
        return False
    if not verify_password(password, db_user.user_password):
        return False
    return db_user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
#async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("get current user")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("ohuet")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            print("blya")
            raise credentials_exception
        token_data = auth.TokenData(user_email=user_email)
    except InvalidTokenError:
        print("pizdec")
        raise credentials_exception
    user = get_user_by_email(db, user_email=token_data.user_email)
    if user is None:
        print("user is none")
        raise credentials_exception
    yield user


async def get_current_active_user( 
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    #if current_user.disabled:
        #raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



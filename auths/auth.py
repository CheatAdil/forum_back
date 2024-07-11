from datetime import datetime, timedelta, timezone
from typing import Union

from ..auths import password_handler
from ..entities.schemas import user_schemas
from ..cruds.user_crud import get_user_by_email
from ..environment_variables import get_var
from ..auths.password_bearer import OAuth2PasswordBearerWithCookie


import jwt
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = get_var("SECRET_KEY")
ALGORITHM = get_var("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_var("ACCESS_TOKEN_EXPIRE_MINUTES"))
CRYPT_SCHEME = get_var("CRYPT_SCHEME")




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, user_name: str, ):
    
    if get_user_by_email(db, user_email=user_name):
        user_dict = db[user_name]
        return user_schemas.User(**user_dict)

def authenticate_user(db_user, user_name: str, password: str):

    #print("works")
    #user = get_user(db, user_name)

    if not db_user:
        #print("not user")
        return False
    if not password_handler.verify_password(password, db_user.user_password):
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

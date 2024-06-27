from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash(plain_text):
    return pwd_context.hash(plain_text)

def verify_hash(plain_text, hash):
    return pwd_context.verify(plain_text, hash)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class hash_handler:
    def _get_hash(plain_text):
        return pwd_context.hash(plain_text)

    def _verify_hash(plain_text, hash):
        return pwd_context.verify(plain_text, hash)

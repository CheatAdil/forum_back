from . import hash

def verify_password(plain_password, user_password):
    return hash.pwd_context.verify(plain_password, user_password)


def get_password_hash(password):
    return hash.get_hash(password)
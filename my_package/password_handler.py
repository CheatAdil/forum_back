from .auths import hash



def get_password_hash(password):
    return hash.get_hash(password)

def verify_password(plain_password, user_password):
    return hash.verify_hash(plain_password, user_password)


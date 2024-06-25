from .hash_handler import hash_handler

class password_handler(hash_handler):

    def get_password_hash(password):
        return super()._get_hash(password)

    def verify_password(plain_password, user_password):
        return super()._verify_hash(plain_password, user_password)


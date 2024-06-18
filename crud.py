import schemas.py

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$nEJAhpawf5bjcIY5VqwWn.HGFGVeDPd75GnIg4/Ec9fmoOPGAquxi",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$R3bI67AMaiMpbZBNW4z3W.RVc/4A826M4ByPF7wbM72TjGhOUUM9y",
        "disabled": True,
    },
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
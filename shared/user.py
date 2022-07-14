import hashlib
from os import environ
from typing import NamedTuple


class User(NamedTuple):
    user_name: str
    password_hash: str
    role: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


def hash_password(password: str):
    salt = environ.get("QUIZ_SALT", "").encode()
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 10000)
    return digest.hex()

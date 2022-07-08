from typing import NamedTuple


class User(NamedTuple):
    user_name: str
    password_hash: str
    role: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

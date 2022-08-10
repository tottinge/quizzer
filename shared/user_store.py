from typing import Iterable, Protocol

from shared.user import User


class UserStore(Protocol):
    def create_user(self, user_name: str, password: str, role: str):
        ...

    def find_user_by_name(self, user_name) -> Iterable[User]:
        ...



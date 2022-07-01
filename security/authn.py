from datetime import timedelta, datetime
from hmac import compare_digest
from typing import Optional

import jwt

from security.authz import SECRET_KEY
from shared.user import User
from shared.user_store_file import UserStore_File


def make_bearer_token(user: User, hours_to_live: int = 4) -> str:
    time_to_live = timedelta(hours=hours_to_live)
    claims = dict(
        sub=user.user_name,
        exp=(datetime.utcnow() + time_to_live),
        iat=datetime.utcnow()
    )
    user_data = {k: v for k, v in user._asdict().items() if k != 'password'}
    payload = {**user_data, **claims}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def authenticate(user_name: str,
                 password: str,
                 db: UserStore_File = None) -> Optional[User]:
    db = db or UserStore_File()
    try:
        [found] = db.find_user_by_name(user_name)
        if compare_digest(password, found.password):
            return found
        return None
    except ValueError:
        return User(user_name=user_name, role="guest", password="")

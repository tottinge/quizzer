import logging
from datetime import timedelta, datetime
from hmac import compare_digest
from os import environ
from typing import Optional

import jwt

from security.authz import SECRET_KEY
from shared.user import User, hash_password
from shared.user_store import UserStore
from shared.user_store_file import UserStoreFile
from shared.user_store_mongo import UserStoreMongo

logger = logging.getLogger(__name__)


def make_bearer_token(user: User, hours_to_live: int = 4) -> str:
    time_to_live = timedelta(hours=hours_to_live)
    claims = dict(
        sub=user.user_name,
        exp=(datetime.utcnow() + time_to_live),
        iat=datetime.utcnow(),
    )
    user_data = {k: v for k, v in user._asdict().items() if k != "password"}
    payload = {**user_data, **claims}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def authenticate(user_name: str, password: str, db: UserStore = None) -> Optional[User]:
    db = db or get_user_store()
    logger.info("User DB is %s", db)
    try:
        [found] = db.find_user_by_name(user_name)
        password_hash = hash_password(password)
        if compare_digest(password_hash, found.password_hash):
            return found
        return None
    except ValueError:
        return User(user_name=user_name, role="guest", password_hash="")


def get_user_store() -> UserStore:
    if environ.get("QUIZ_MONGO_URL"):
        return UserStoreMongo()
    return UserStoreFile(environ.get("QUIZ_USER_PATH"))

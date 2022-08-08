from shared.mongo_connection import db_connection


def get_collection():
    return db_connection()['users']


class UserStoreMongo:

    def create_user(self, user_name: str, password: str, role: str):
        ...

    def find_user_by_name(self, user_name):
        with get_collection() as users:
            user = users.find({"user_name":user_name})
            return user
        # ToDo:  Should this return a user object or a list of Profiles

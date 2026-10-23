from enum import StrEnum


class Action(StrEnum):

    EXIT = "exit"
    LOGIN = "login"
    BROWSE = "browse"
    ORDER = "order"
    LOGOUT = "logout"
    MY_PRODUCTS = "my_products"
    SET_PRICE = "set_price"
    LIST_USERS = "list_users"
    DISABLE_USER = "disable_user"
    CHANGE_ROLE = "change_role"
    DISCOUNT = "discount"


class ActionExcutor:
    def __init__(self, users: list[dict], products: list[dict]):
        self._users = users
        self._products = products

    def login(self, username: str, password: str) -> tuple[dict | None, str]:
        for user in self._users:
            if username == user.get("username"):
                if user.get("active") is not True:
                    return None, "Account is disabled"
                if password != user.get("password"):
                    return None, "Incorrect password"
                return user, f"Welcome {user.get("username")}"
        return None, "User not found"


def handle_action(action: str, current_user: dict) -> dict: ...

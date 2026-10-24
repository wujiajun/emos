from enum import StrEnum
from getpass import getpass

from emos.domian.models import Role
from emos.outputs import Printer


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


MENUS: dict[str | None, list[tuple[str, str]]] = {
    # None = guest (not logged in)
    None: [
        (Action.LOGIN.value, "Login"),
        (Action.BROWSE.value, "Browse and filter products"),
    ],
    "Buyer": [
        (Action.BROWSE.value, "Browse and filter products"),
        (Action.ORDER.value, "Place order"),
        (Action.LOGOUT.value, "Logout"),
    ],
    "Seller": [
        (Action.BROWSE.value, "Browse and filter products"),
        (Action.MY_PRODUCTS.value, "View my products"),
        (Action.SET_PRICE.value, "Update product price"),
        (Action.LOGOUT.value, "Logout"),
    ],
    "Admin": [
        (Action.BROWSE.value, "Browse and filter products"),
        (Action.LIST_USERS.value, "View users"),
        (Action.DISABLE_USER.value, "Disable a user"),
        (Action.CHANGE_ROLE.value, "Change a user's role"),
        (Action.DISCOUNT.value, "Configure discount rule"),
        (Action.LOGOUT.value, "Logout"),
    ],
}


class ActionExcutor:
    def __init__(self, users: list[dict], products: list[dict], discount_rule: dict):
        self._users = users
        self._products = products
        self._discount_rule = discount_rule

    def handle_action(self, action: str, current_user: dict) -> dict:
        allowed, error_message = self._check_permission(user=current_user, action=action)
        if allowed is False:
            Printer.deny_error(error_message)
            return current_user

        if Action.LOGIN.value == action:
            print("\n=== Login ===")
            username = input("Username: ").strip()
            password = getpass("Password: ")
            logged_in_user, message = self._login(username=username, password=password)
            if logged_in_user is None:
                Printer.error(message)
            else:
                Printer.success(message)
                return logged_in_user
        elif Action.BROWSE.value == action:
            print("\n=== Browse ===")
            print("Press Enter to skip any filter.")
            keyword = input("Product name contains: ").strip()
            min_price = None
            max_price = None
            try:
                min_raw = input("Minimum price: ").strip()
                min_price = float(min_raw) if min_raw else None
                max_raw = input("Maximum price: ").strip()
                max_price = float(max_raw) if max_raw else None
            except ValueError:
                Printer.error("Invalid price. Please enter a number, or press Enter to skip.")
                return current_user

            result: list = self._browse(keyword=keyword, min_price=min_price, max_price=max_price)
            Printer.products(result)
        elif Action.LOGOUT.value == action:
            current_user = None
        elif Action.MY_PRODUCTS.value == action:
            result: list = self._my_products(current_user=current_user)
            Printer.products(result)
        elif Action.SET_PRICE.value == action:
            product_name = input("Product name to update: ").strip()
            new_price = None
            try:
                price_raw = input("New price: ").strip()
                new_price = float(price_raw) if price_raw else None
                if new_price <= 0:
                    Printer.error("Price must be greater than 0.")
                    return current_user
            except ValueError:
                Printer.error("Invalid price. Please enter a number.")
                return current_user
            successed, message = self._set_price(
                current_user=current_user, product_name=product_name, new_price=new_price
            )
            if successed is False:
                Printer.error(message)
            else:
                Printer.success(message)
                Printer.products(self._my_products(current_user=current_user))
        elif Action.LIST_USERS.value == action:
            Printer.users(self._list_users())
        elif Action.DISABLE_USER.value == action:
            disable_username = input("User name to disable: ").strip()
            successed, message = self._disable_user(disable_username)
            if successed is False:
                Printer.error(message)
            else:
                Printer.success(message)
                Printer.users(self._list_users())
        elif Action.CHANGE_ROLE.value == action:
            change_role_username = input("Username to change: ").strip()
            new_role = None
            try:
                new_role_raw = input("New role (Buyer / Seller / Admin): ").strip().capitalize()
                new_role = Role(new_role_raw)
            except ValueError:
                Printer.error("Invalid role. Choose Buyer, Seller or Admin.")
                return current_user
            successed, message = self._change_role(change_role_username, new_role)
            if successed is False:
                Printer.error(message)
            else:
                Printer.success(message)
                Printer.users(self._list_users())
        elif Action.DISCOUNT.value == action:
            new_threshold = None
            new_percentage = None
            try:
                new_threshold_raw = input("New discount threshold ($): ").strip()
                new_threshold = float(new_threshold_raw)
                new_percentage_raw = input("New discount percentage (%): ").strip()
                new_percentage = float(new_percentage_raw)
            except ValueError:
                Printer.error("Please enter numbers only, without '$' or '%' signs.")
                return current_user
            successed, message = self._discount(new_threshold=new_threshold, new_percentage=new_percentage)
            if successed is False:
                Printer.error(message)
            else:
                Printer.success(message)
                Printer.discount_rule(self._discount_rule)
        return current_user

    def _check_permission(self, user: dict, action: str) -> tuple[bool, str]:
        required_role: Role = None

        match action:
            case Action.LOGIN.value:
                required_role = Role.GUEST
            case Action.ORDER.value:
                required_role = Role.BUYER
            case Action.MY_PRODUCTS.value:
                required_role = Role.SELLER
            case Action.SET_PRICE.value:
                required_role = Role.SELLER
            case Action.LIST_USERS.value:
                required_role = Role.ADMIN
            case Action.DISABLE_USER.value:
                required_role = Role.ADMIN
            case Action.CHANGE_ROLE.value:
                required_role = Role.ADMIN
            case Action.DISCOUNT.value:
                required_role = Role.ADMIN

        # All users have this permission
        if required_role is None:
            return True, ""

        # Only guests have this permission
        if required_role == Role.GUEST:
            if user is None:
                return True, ""
            else:
                return False, f"You are already logged in as {user['username']}. Please log out first."

        # Only logged-in users have this permission
        if user is None:
            return False, "Please log in first"

        if required_role.value != user.get("role"):
            return False, f"Access denied for your role[{user.get("role")}]"

        return True, ""

    def _login(
        self,
        username: str,
        password: str,
    ) -> tuple[dict | None, str]:
        for user in self._users:
            if username == user.get("username"):
                if user.get("active") is not True:
                    return None, "Account is disabled"
                if password != user.get("password"):
                    return None, "Incorrect password"
                return user, f"Login successful. Welcome {user.get("username")}"
        return None, "User not found"

    def _browse(
        self,
        keyword: str | None,
        min_price: float | None,
        max_price: float | None,
    ) -> list:
        return [
            product
            for product in self._products
            if (not keyword or keyword in product.get("name"))
            and (min_price is None or product["price"] >= min_price)
            and (max_price is None or product["price"] <= max_price)
        ]

    def _my_products(self, current_user: dict) -> list:
        username = current_user.get("username")
        if not username:
            return []
        return [product for product in self._products if product.get("seller") == username]

    def _set_price(self, current_user: dict, product_name: str, new_price: float) -> tuple[bool, str]:
        username = current_user.get("username")
        product = None
        for p in self._products:
            if p.get("name") == product_name:
                product = p
                break

        if product is None:
            return False, "Product not found."

        if product.get("seller") != username:
            return False, "You can only change your own products."

        old_price = product["price"]
        product["price"] = new_price
        return True, f"Price updated. '{product['name']}': {old_price:.2f} -> {new_price:.2f}"

    def _list_users(self) -> list:
        return self._users

    def _disable_user(self, username: str) -> tuple[bool, str]:
        user = self._find_user(username=username)

        if user is None:
            return False, "User not found."

        if user.get("role") == Role.ADMIN.value:
            return False, "Admin accounts cannot be disabled."

        user["active"] = False
        return True, f"User '{username}' has been disabled."

    def _change_role(self, username: str, role: Role) -> tuple[bool, str]:
        user = self._find_user(username=username)
        if user is None:
            return False, "User not found."

        if user.get("role") == Role.ADMIN.value:
            return False, "Admin accounts cannot have their role changed."

        old_role = user["role"]
        user["role"] = role.value
        return True, f"Role of '{username}' changed: {old_role} -> {role.value}."

    def _find_user(self, username: str) -> dict:
        for u in self._users:
            if u.get("username") == username:
                return u

    def _discount(self, new_threshold: float, new_percentage: float) -> tuple[bool, str]:
        if new_threshold <= 0 or new_percentage <= 0 or new_percentage > 100:
            return (
                False,
                "Invalid discount rule. Threshold must be greater than 0, and percentage must be between 1 and 100.",
            )
        self._discount_rule["threshold"] = new_threshold
        self._discount_rule["percentage"] = new_percentage
        return True, "Discount rule updated."

# role: Buyer, Seller, Admin
from enum import StrEnum


class Role(StrEnum):
    GUEST = "Guest"
    BUYER = "Buyer"
    SELLER = "Seller"
    ADMIN = "Admin"


def user(
    username: str,
    password: str,
    role: str,
    active: bool,
) -> dict:
    return {
        "username": username,
        "password": password,
        "role": role,
        "active": active,
    }


def product(
    name: str,
    price: float,
    seller: str,
    stock: int,
) -> dict:
    return {
        "name": name,
        "price": price,
        "seller": seller,
        "stock": stock,
    }


def discount_rule(
    threshold: float,
    percentage: float,
) -> dict:
    return {
        "threshold": threshold,
        "percentage": percentage,
    }

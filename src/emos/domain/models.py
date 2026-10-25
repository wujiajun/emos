# role: Buyer, Seller, Admin
from enum import StrEnum


class Role(StrEnum):
    GUEST = "Guest"
    BUYER = "Buyer"
    SELLER = "Seller"
    ADMIN = "Admin"


class OrderStatus(StrEnum):
    CONFIRMED = "Confirmed"


def user(
    username: str,
    password: str,
    role: str,
    balance: float,
    active: bool,
) -> dict:
    return {
        "username": username,
        "password": password,
        "role": role,
        "balance": balance,  # buyer's available funds
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


def rule(
    threshold: float,
    percentage: float,
) -> dict:
    return {
        "threshold": threshold,
        "percentage": percentage,
    }


def order(
    order_id: int,
    buyer: str,
    items: list[dict],
    subtotal: float,
    discount: float,
    total: float,
    payment_method: str,
    status: str,
) -> dict:
    return {
        "id": order_id,
        "buyer": buyer,
        "items": items,
        "subtotal": subtotal,
        "discount": discount,
        "total": total,
        "payment_method": payment_method,
        "status": status,
    }

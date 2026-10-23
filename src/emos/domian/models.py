# role: Buyer, Seller, Admin
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

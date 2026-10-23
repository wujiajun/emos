MENUS: dict[str | None, list[tuple[str, str]]] = {
    # None = guest (not logged in)
    None: [
        ("login", "Login"),
        ("browse", "Browse and filter products"),
    ],
    "Buyer": [
        ("browse", "Browse and filter products"),
        ("order", "Place order"),
        ("logout", "Logout"),
    ],
    "Seller": [
        ("browse", "Browse and filter products"),
        ("my_products", "View my products"),
        ("set_price", "Update product price"),
        ("logout", "Logout"),
    ],
    "Admin": [
        ("browse", "Browse and filter products"),
        ("list_users", "View users"),
        ("disable_user", "Disable a user"),
        ("change_role", "Change a user's role"),
        ("discount", "Configure discount rule"),
        ("logout", "Logout"),
    ],
}


class Printer:

    @staticmethod
    def welcome() -> None:
        line = "=" * 56
        print(line)
        print("  Welcome to EMOS")
        print("  E-Commerce Order Management System")
        print("  CMPS-3000 Project 1 · Group 3")
        print(line)

    def users(users: list[dict]) -> None:
        print("\n=== Users ===")
        print(f"{'#':<3} {'Username':<10} {'Role':<8} {'Status':<8}")
        print("-" * 32)
        for i, u in enumerate(users, start=1):
            status = "Active" if u["active"] else "Disabled"
            print(f"{i:<3} {u['username']:<10} {u['role']:<8} {status:<8}")

    def products(products: list[dict]) -> None:
        print("\n=== Products ===")
        print(f"{'#':<3} {'Name':<28} {'Price':>8}  {'Seller':<7} {'Stock':>5}")
        print("-" * 56)
        for i, p in enumerate(products, start=1):
            stock = "OUT" if p["stock"] == 0 else p["stock"]
            print(f"{i:<3} {p['name']:<28} {p['price']:>8.2f}  {p['seller']:<7} {stock:>5}")

    def goodbye(user: dict | None) -> None:
        name = user["username"] if user else "guest"
        print("\n" + "=" * 56)
        print(f"  Goodbye, {name}. Thank you for using EMOS.")
        print("=" * 56)

    def menus(logged_in_user: dict) -> list[str]:
        role = logged_in_user["role"] if logged_in_user else None
        title = f"{logged_in_user['username']}, {role}" if logged_in_user else "guest"
        items = MENUS.get(role)

        commands: list[str] = []
        print(f"\n=== Main Menu ({title}) ===")
        for i, item in enumerate(items, start=1):
            print(f"[{i}] {item[1]}")
            commands.append(item[0])
        print("[0] Exit")
        commands.insert(0, "exit")
        return commands

    def error(error_info: str) -> None:
        print(f"[ERROR] {error_info}")

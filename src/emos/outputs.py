class Printer:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    @staticmethod
    def welcome() -> None:
        line = "=" * 56
        print(line)
        print("  Welcome to EMOS")
        print("  E-Commerce Order Management System")
        print("  CMPS-3000 Project 1 · Group 3")
        print(line)

    @staticmethod
    def users(users: list[dict]) -> None:
        print("\n=== Users ===")
        print(f"{'#':<3} {'Username':<10} {'Role':<8} {'Status':<8}")
        print("-" * 32)
        for i, u in enumerate(users, start=1):
            status = "Active" if u["active"] else "Disabled"
            print(f"{i:<3} {u['username']:<10} {u['role']:<8} {status:<8}")

    @staticmethod
    def products(products: list[dict]) -> None:
        print("\n=== Products ===")
        print(f"{'#':<3} {'Name':<28} {'Price':>8}  {'Seller':<7} {'Stock':>5}")
        print("-" * 56)
        if len(products) == 0:
            print("[INFO] No products found.")
        else:
            for i, p in enumerate(products, start=1):
                stock = "OUT" if p["stock"] == 0 else p["stock"]
                print(f"{i:<3} {p['name']:<28} {p['price']:>8.2f}  {p['seller']:<7} {stock:>5}")

    @staticmethod
    def discount_rule(rule: dict) -> None:
        print("\n=== Discount Rule ===")
        print(f"Orders of ${rule['threshold']:.2f} or more get {rule['percentage']}% off.")

    @staticmethod
    def order_review(
        items: list[dict],
        subtotal: float,
        discount: float,
        total: float,
        percentage: float,
        payment_method: str,
    ) -> None:
        print("\n=== Order Review ===")
        for item in items:
            line_total = item["price"] * item["quantity"]
            print(f"{item['name']:<28} x {item['quantity']:<3} {line_total:>14.2f}")
        print("-" * 56)
        print(f"{'Subtotal':<34} {subtotal:>14.2f}")
        if discount > 0:
            print(f"{f'Discount ({percentage:g}%)':<34} {-discount:>14.2f}")
        else:
            print(f"{'Discount':<34} {0:>14.2f}")
        print(f"{'Total':<34} {total:>14.2f}")
        print(f"\nPayment method: {payment_method}")

    @staticmethod
    def user_balance(user: dict) -> None:
        Printer.info(f"Remaining balance: {user['balance']:.2f}")

    @staticmethod
    def goodbye(user: dict | None) -> None:
        name = user["username"] if user else "guest"
        print("\n" + "=" * 56)
        print(f"  Goodbye, {name}. Thank you for using EMOS.")
        print("=" * 56)

    @staticmethod
    def menus(logged_in_user: dict, menus: dict[str | None, list[tuple[str, str]]]) -> list[str]:
        role = logged_in_user["role"] if logged_in_user else None
        title = f"{logged_in_user['username']}, {role}" if logged_in_user else "guest"
        items = menus.get(role)

        commands: list[str] = []
        print(f"\n=== Main Menu ({title}) ===")
        for i, item in enumerate(items, start=1):
            print(f"[{i}] {item[1]}")
            commands.append(item[0])
        print("[0] Exit")
        commands.insert(0, "exit")
        return commands

    @staticmethod
    def error(error_info: str) -> None:
        print(f"{Printer.YELLOW}[ERROR]{Printer.RESET} {error_info}")

    @staticmethod
    def success(info: str) -> None:
        print(f"{Printer.GREEN}[SUCCESS]{Printer.RESET} {info}")

    @staticmethod
    def deny_error(error_info: str) -> None:
        print(f"{Printer.RED}[ACCESS DENIED]{Printer.RESET} {error_info}")

    @staticmethod
    def info(info: str) -> None:
        print(f"{Printer.CYAN}[INFO]{Printer.RESET} {info}")

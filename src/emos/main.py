from emos.application.actions import MENUS, ActionExecutor
from emos.domain.models import Role, product, rule, user
from emos.outputs import Printer


def main() -> None:
    # so Ctrl+C / Ctrl+D do not print a traceback
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print()
        Printer.info("Interrupted. Exiting.")


def run() -> None:
    """Set up the data, then run the menu loop until the user exits."""
    users: list[dict] = []
    products: list[dict] = []
    discount_rule: dict = {}
    orders: list[dict] = []
    init(users, products, discount_rule)
    Printer.welcome()
    Printer.users(users=users)
    Printer.products(products=products)
    Printer.discount_rule(discount_rule)

    current_user = None  # None = guest
    running = True

    while running is True:
        actions = Printer.menus(current_user, MENUS)
        user_input = input("Select an option > ").strip()
        try:
            choice = int(user_input)
        except ValueError:
            Printer.error("Invalid option. Please choose a number from the menu.")
            continue
        if choice == 0:
            running = False
        elif not (0 <= choice <= len(actions)):
            Printer.error("Invalid option. Please choose a number from the menu.")
        else:
            # actions[0] is "exit", so the menu number is also the list index
            action = actions[choice]
            # login and logout return a different current_user
            actionExecutor = ActionExecutor(users=users, products=products, discount_rule=discount_rule, orders=orders)
            current_user = actionExecutor.handle_action(action=action, current_user=current_user)

    Printer.goodbye(current_user)


def init(
    users: list[dict],
    products: list[dict],
    discount_rule: dict,
) -> None:
    """Fill in the sample users, products and discount rule."""
    # Users: 2 buyers, 2 sellers, 1 admin, 1 disabled buyer
    users.append(user(username="alice", password="alice123", role=Role.BUYER.value, active=True, balance=500.0))
    users.append(user(username="bob", password="bob123", role=Role.BUYER.value, active=True, balance=20.0))
    users.append(user(username="sam", password="sam123", role=Role.SELLER.value, active=True, balance=0.0))
    users.append(user(username="sara", password="sara123", role=Role.SELLER.value, active=True, balance=0.0))
    users.append(user(username="ada", password="ada123", role=Role.ADMIN.value, active=True, balance=0.0))
    users.append(user(username="dave", password="dave123", role=Role.BUYER.value, active=False, balance=100.0))

    # Products: sam's items
    products.append(product(name="USB Cable", price=9.99, seller="sam", stock=50))
    products.append(product(name="Wireless Mouse", price=24.99, seller="sam", stock=30))
    products.append(product(name="Wireless Charger", price=29.99, seller="sam", stock=20))
    products.append(product(name="Mechanical Keyboard", price=79.99, seller="sam", stock=10))
    products.append(product(name="Phone Case", price=12.50, seller="sam", stock=0))

    # Products: sara's items
    products.append(product(name="Desk Lamp", price=34.99, seller="sara", stock=2))
    products.append(product(name="Laptop Stand", price=50.00, seller="sara", stock=15))
    products.append(product(name="Webcam", price=59.99, seller="sara", stock=8))
    products.append(product(name="Noise-Cancelling Headphones", price=149.99, seller="sara", stock=5))

    # Discount rule (threshold=100.0, percentage=10)
    discount_rule.update(rule(threshold=100.0, percentage=10))


if __name__ == "__main__":
    main()

# Test for the permission cases that cannot be reached from the menu
# (the menu hides options a role cannot use). Run with: uv run python test.py
from emos.application.actions import Action, ActionExecutor
from emos.main import init


def find_user(users: list[dict], username: str) -> dict:
    return next(u for u in users if u["username"] == username)


def main() -> None:
    users: list[dict] = []
    products: list[dict] = []
    discount_rule: dict = {}
    orders: list[dict] = []
    init(users, products, discount_rule)
    executor = ActionExecutor(users=users, products=products, discount_rule=discount_rule, orders=orders)

    alice = find_user(users, "alice")  # Buyer
    sam = find_user(users, "sam")  # Seller
    ada = find_user(users, "ada")  # Admin

    print("=== Guest places an order ===")
    executor.handle_action(action=Action.ORDER.value, current_user=None)

    print("\n=== Seller and Admin place an order ===")
    for person in (sam, ada):
        print(f"As {person['username']} ({person['role']}):")
        executor.handle_action(action=Action.ORDER.value, current_user=person)

    print("\n=== Buyer and Seller use Admin features ===")
    for person in (alice, sam):
        print(f"As {person['username']} ({person['role']}):")
        for action in (Action.LIST_USERS, Action.DISABLE_USER, Action.CHANGE_ROLE, Action.DISCOUNT):
            print(f"  {action.value}:", end=" ")
            executor.handle_action(action=action.value, current_user=person)

    print("\n=== Check: nothing was changed ===")
    print(f"Orders saved: {len(orders)}")
    print(f"alice balance: {alice['balance']:.2f}")
    print(f"Discount rule: {discount_rule['threshold']:.2f} / {discount_rule['percentage']}%")


if __name__ == "__main__":
    main()

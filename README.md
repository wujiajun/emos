# EMOS

E-Commerce Order Management System, a command-line simulation built for
CMPS-3000 Computational Thinking and Problem Solving (Project 1, Group 3).

The program models three roles (Buyer, Seller, Admin) plus guests, with
login validation, role-based menus and permission checks, product
filtering, and a configurable discount rule.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) (optional, recommended)

No third-party packages are needed.

## Run

```bash
uv run emos
```

Without uv:

```bash
cd src
python3 -m emos.main
```

## Demo accounts

| Username | Password | Role   | Status   |
|----------|----------|--------|----------|
| alice    | alice123 | Buyer  | Active   |
| bob      | bob123   | Buyer  | Active   |
| sam      | sam123   | Seller | Active   |
| sara     | sara123  | Seller | Active   |
| ada      | ada123   | Admin  | Active   |
| dave     | dave123  | Buyer  | Disabled |

These are sample data for the simulation only. Passwords are stored in
plain text to keep the model simple; a real system would store hashes.

## Features

- Guests: browse and filter products by name and price range, log in
- Buyers: browse and filter products
- Sellers: view their own products and update their prices
- Admins: view users, disable accounts, change roles, configure the
  discount rule (Admin accounts are protected from both)
- Every action is permission-checked, and every result is reported with a
  colored status label: `[SUCCESS]`, `[ERROR]`, `[ACCESS DENIED]`

## Project structure

```
src/emos/
  main.py              entry point, sample data, main menu loop
  application/
    actions.py         menus, permission checks, action handlers
  domain/
    models.py          Role enum and user / product / discount rule dicts
  outputs.py           Printer: all formatted console output
```

State is kept in memory, so all data resets when the program restarts.
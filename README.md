# Bean Counter Cafe

A small point-of-sale program for a coffee shop. It reads an order, checks the items against today's stock, prices each drink by size and add-ons, applies any time-based promotions, adds tax, and works out how many loyalty points the customer earned. Then it prints a receipt.

This is a practice repo for a lesson on **codebase navigation**: following a command from its entry point through every file it touches. There are no bugs to fix here; the only task is to trace.

It's plain Python. There's no web framework, no database and nothing to install except `pytest`. The "database" is a folder of JSON files that are only ever read, so every command gives the same output every time you run it.

## App Structure

```
coffee-order-navigation-starter/
├── main.py                  # Command line entry point: `menu` and `receipt`
├── models.py                # Dataclasses for every kind of thing in the app
├── store.py                 # Loads the JSON files in data/ into model objects
├── services/
│   ├── receipt.py           # Runs an order through every step, formats the receipt
│   ├── inventory.py         # Stock checks: remove sold-out items, swap sold-out add-ons
│   ├── pricing.py           # Size prices, add-on prices, tax
│   ├── promotions.py        # Time-window promos (e.g. Happy Hour)
│   ├── loyalty.py           # Loyalty points and tier multipliers
│   └── menu_board.py        # Builds the printable menu
├── data/
│   ├── menu.json            # Items, base prices, size upcharges, add-ons
│   ├── stock.json           # How many of each item / add-on are left today
│   ├── customers.json       # Customers and their loyalty tier
│   ├── promos.json          # Promotions and their time windows
│   └── orders/              # One JSON file per order
├── tests/
└── requirements.txt
```

`main.py` is deliberately thin. It reads the command, calls one service and prints the result. None of the interesting logic (stock substitutions, promo windows, point rounding) lives there. To find out what a command actually does, you have to follow it into `services/`.

## Setup

You need Python 3.10 or newer. Check with `python --version` (on some Macs it's `python3`).

The app itself uses only the standard library, so you can run it straight away:

```
python main.py menu
python main.py receipt data/orders/maya.json
```

To run the tests you'll need `pytest`. A virtual environment is optional but recommended:

```
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Windows (Git Bash)
source .venv/Scripts/activate
```

```
pip install -r requirements.txt
pytest tests/
```

## How to Read the Code

1. **Start with `models.py`.** It defines every noun in the app: `MenuItem`, `Modifier` (an add-on like Oat Milk), `Customer`, `OrderLine`, `Order` and `Promo`. It also has the objects the services produce: `PricedLine`, `Discount` and `Receipt`. Notice that an `OrderLine` only holds *ids* (`"latte"`, `["oat_milk"]`), while a `PricedLine` holds the real objects plus a price.
2. **Skim `store.py`.** This is where JSON turns into those objects. When you want to know where a value comes from, like a price or a time window, the answer is often in a file in `data/` and not in the code.
3. **Pick a command and trace it.** For example:

> `python main.py receipt data/orders/maya.json` → `main.py: show_receipt()` → `services/receipt.py: build_receipt()` → for each line: `services/inventory.py: check_line()`, then `services/pricing.py: price_line()` → `pricing.py: size_price()` (reads `size_upcharges` from `data/menu.json`) + `pricing.py: _modifier_total()` → back in `build_receipt()`: `promotions.apply_promos()`, `pricing.apply_tax()`, `loyalty.points_for()` → `receipt.py: format_receipt()`

Notice that `build_receipt()` is a coordinator. It calls four different services, **and the order it calls them in matters**. When you trace, don't stop at the first service function you find. Go back to the caller and check what it does next, and with what values.

One more thing: **all money is stored as integer cents.** `425` means $4.25. It only becomes dollars in `receipt.py: _money()` and `menu_board.py` when it's printed.

## Practice Paths

For each one, run the command, then write down every file and function the command passes through, in order. Don't jump straight to the service that sounds right. Confirm that something actually calls it first.

0. **Warm-up: the menu board.** Oat Milk and the Butter Croissant show `SOLD OUT`. Which file decides that, and where do the three Latte prices come from? (Even the simplest command uses two services.)
   `python main.py menu`

1. **Maya's large latte with an extra shot costs $6.00.** The menu lists a Latte starting at $4.25. Account for every cent of that $6.00. Which function adds each part, and where does each number live?
   `python main.py receipt data/orders/maya.json`

2. **Sam ordered at 4:00 PM, but Happy Hour runs "2 to 4" and he didn't get the discount.** Where is that decided? Is the answer in the code, in the data, or both?
   `python main.py receipt data/orders/sam.json`

3. **Priya is a Gold member and earned 18 points.** Her total was $13.07. Why isn't it 19 (13 × 1.5, rounded down) or 21 (the $14.25 subtotal × 1.5)? Exactly what amount are points calculated on, and who decides that?
   `python main.py receipt data/orders/priya.json`

4. **Leo ordered a latte with oat milk and a croissant, but both are out.** One of them disappears from the receipt and the other gets swapped. Why doesn't Leo pay the $0.75 oat-milk charge? Which step runs first, the stock check or pricing, and how does that affect what pricing sees?
   `python main.py receipt data/orders/leo.json`

## Coming from (or going to) the Flask version

This repo has the same shape as the course-registration Flask app, just without the web and database layers:

| Here                       | In the Flask app                        |
| -------------------------- | --------------------------------------- |
| `main.py` command function | `routes/*.py` route function            |
| `services/*.py`            | `services/*.py`                         |
| `models.py` dataclasses    | `models.py` SQLAlchemy models           |
| `store.py` + `data/*.json` | the SQLite database + `seed_data.py`    |
| running a command          | sending an HTTP request with `curl`     |

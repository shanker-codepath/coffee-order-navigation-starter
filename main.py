"""Bean Counter Cafe command line.

    python main.py menu
    python main.py receipt data/orders/maya.json

Each command just calls one service and prints what comes back.
"""

import argparse
import sys

import store
from services import menu_board, pricing, receipt


def show_menu(args):
    print("\n".join(menu_board.build_menu()))


def show_receipt(args):
    try:
        result = receipt.build_receipt(args.order_file)
    except (
        store.OrderFileNotFoundError,
        receipt.CustomerNotFoundError,
        pricing.MenuItemNotFoundError,
    ) as error:
        print(f"Error: {error}")
        sys.exit(1)

    print(receipt.format_receipt(result))


def main():
    parser = argparse.ArgumentParser(description="Bean Counter Cafe")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("menu", help="print the menu").set_defaults(run=show_menu)

    receipt_parser = commands.add_parser("receipt", help="price an order and print its receipt")
    receipt_parser.add_argument("order_file", help="path to an order JSON file")
    receipt_parser.set_defaults(run=show_receipt)

    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()

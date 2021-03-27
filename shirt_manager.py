"""
This is a simple shirt order management program 
to practice basic python coding.
"""

import os
import json

class OrderData():
    """A clas to hold order attributes."""
    def __init__(self, name, size, text, status='PENDING'):
        """
        Parameters:
        status: Order status (initialized to PENDING)
        name: Name of the client who made the order
        size: Size of the shirt ordered
        text: Custome text to be printed on the shirt
        """
        self.status = status
        self.name = name
        self.size = size 
        self.text = text


def clr_scrn():
    """Clear the terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def display_orders(order_list):
    """Print order attributes in a tab delineated table with headers."""
    print("We have these orders in the system:\n")
    # Print padded, tab separated table headers
    print("{:<10}\t{:<15}\t{:<15}\t{:<15}\t{:<15}".format(
            "Order ID", "Order Status", "Client", "Shirt size",
            "Custom Text"))
    for orderID, orderdata in order_list.items():
        print("{:<10}\t{:<15}\t{:<15}\t{:<15}\t{:<15}\t".format(
               orderID, orderdata.status, orderdata.name, orderdata.size,
               orderdata.text))
    print("")


def print_main_menu(order_list, MAIN_MENU):
    """
    Print orders and possible actions. Captures & returns valid menu choice.
    """
    choice = ""
    while choice not in MAIN_MENU.keys():
        clr_scrn()
        display_orders(order_list)
        print("What do you want to do?")
        for number, choice in MAIN_MENU.items():
            print(f"{number}: {choice}")
        choice = input()
    return choice


def new_order(order_list):
    """
    Capture user input, and create and persist new OrderData object.
    """
    confirm = ''
    while confirm.lower() not in ['y', 'q']:
        name = valid_string("What's the name of the client? ")
        size = valid_size(VALID_SHIRT_SIZES)
        text = valid_string("What do they want it to say on the front? ")
        print("")
        print("{:>13}{:<16}\n{:>13}{:<16}\n{:>13}{:<16}".format(
            "Name: ", name, "Shirt Size: ", size, "Custom Text: ", text))
        confirm = input("\nIs this OK? Input 'y' to continue, " +
                        "'q' to cancel, or any other key to try again: ")
    if confirm.lower() == 'y':
        orderID = max(get_orderIDs(order_list)) + 1
        order_list[orderID] = OrderData(name, size, text)
        persist_orders(SAVE_FILE_NAME, order_list)


def valid_string(prompt):
    """
    Prompt for input, and return input as string only if input < 16 chars.
    """
    while True:
        clr_scrn()
        display_orders(order_list)
        user_input = input(prompt)
        if len(user_input) < 16:
            break
        else:
            print("Please enter valid text less than 16 characters")
    return user_input


def valid_size(VALID_SHIRT_SIZES):
    """Return user input only if it is defines as a valid size."""
    user_input = ""
    while user_input not in VALID_SHIRT_SIZES:
        clr_scrn()
        display_orders(order_list)
        print(f"What size shirt do they need? " +
               f"({', '.join(VALID_SHIRT_SIZES)}) ", end = '')
        user_input = input()
    return user_input


def get_orderIDs(order_list):
    """Return all orderIDs as integers in a list from order_list"""
    orderIDs = [0]
    for orderID in order_list:
        orderIDs.append(int(orderID))
    return orderIDs


def update_order_status(order_list):
    """Update status for a specified Order, and persist that change."""
    confirm = ""
    while confirm.lower() not in ["y", "q"]:
        orderID = select_valid_orderID(order_list)
        status = input("Enter the status of this order: ")
        confirm = input("\nIs this OK? Input 'y' to continue, " +
                        "'q' to cancel, or any other key to try again: ")
    if confirm.lower() == "y":
        order = order_list[orderID]
        order.status = status
        persist_orders(SAVE_FILE_NAME, order_list)


def remove_order(order_list):
    """Remove an order from order_list, and persist order_list to file."""
    confirm = ""
    while confirm.lower() not in ["y", "q"]:
        orderID = select_valid_orderID(order_list)
        confirm = input("\nIs this OK? Input 'y' to continue, " +
                        "'q' to cancel, or any other key to try again: ")
    if confirm.lower() == "y":
        del order_list[orderID]
        persist_orders(SAVE_FILE_NAME, order_list)


def select_valid_orderID(order_list):
    """Return user input orderID only if it exists in order_list."""
    orderID = -1
    failed = False
    while orderID not in get_orderIDs(order_list):
        clr_scrn()
        display_orders(order_list)
        if failed:
            print ("Please enter a valid Order ID")
        try:
            orderID = int(input(("Enter the Order ID: ")))
        except ValueError:
            failed = True
    return orderID


def persist_orders(SAVE_FILE_NAME, order_list):
    """Persist order_list to file as JSON data."""
    persist_data = []
    for orderID, orderdata in order_list.items():
        data = {}
        data["orderID"] = orderID
        data["status"] = orderdata.status
        data["name"] = orderdata.name
        data["size"] = orderdata.size
        data["text"] = orderdata.text
        persist_data.append(data)
    with open(SAVE_FILE_NAME, 'w') as save_file:
        json.dump(persist_data, save_file, indent=2)


def import_orders(SAVE_FILE_NAME):
    """Populate order_list with OrderData objects re-built from saved data."""
    order_list = {}
    if os.path.isfile(SAVE_FILE_NAME):
        with open(SAVE_FILE_NAME) as save_file:
            savedorderlist = json.load(save_file)
        for savedorder in savedorderlist:
            orderID = savedorder["orderID"]
            order_list[orderID] = OrderData(
                savedorder["name"], savedorder["size"], 
                savedorder["text"], savedorder["status"])
    return order_list


# Iniitalize constants
MAIN_MENU = {"1": "Input new order",
                 "2": "Update order status",
                 "3": "Remove order",
                 "q": "Exit"}
VALID_SHIRT_SIZES = ['small', 'medium', 'large']
SAVE_FILE_NAME = "orders.sav"

# Print welcome message & populate order_list from save file
clr_scrn()
print("\nWelcome to my shirt production management program.")
print("I'm using it to practice basic classes, loops, functions, " +
      "and storing and retrieving data\n")
input("Press any key to continue")

order_list = import_orders(SAVE_FILE_NAME)

# Main loop
while True:
    clr_scrn()
    choice = print_main_menu(order_list, MAIN_MENU)
    if choice == '1':
        new_order(order_list)
    if choice == '2':
        update_order_status(order_list)
    if choice == '3':
        remove_order(order_list)
    elif choice == 'q':
        print("Thanks for using this program!")
        break

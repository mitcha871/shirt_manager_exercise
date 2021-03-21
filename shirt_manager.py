import os
import json

class OrderData():
    def __init__(self, name, size, text, status='PENDING'):
        self.status = status
        self.name = name
        self.size = size
        self.text = text

def clr_scrn():
    os.system("clear")

def display_orders(order_list):
    print("We have these orders in the system:\n")
    print("{:<10}\t{:<15}\t{:<15}\t{:<15}\t{:<15}".format("Order ID", "Order Status", "Client", "Shirt size", "Custom Text"))
    for orderID, orderdata in order_list.items():
        print("{:<15}\t{:<15}\t{:<15}\t{:<15}\t{:<15}\t".format(orderID, orderdata.status, orderdata.name, orderdata.size, orderdata.text))
    print("")

def main_menu(order_list, VALID_CHOICES):
    choice = ""
    while choice not in VALID_CHOICES.keys():
        clr_scrn()
        display_orders(order_list)
        print("What do you want to do?")
        for number, choice in VALID_CHOICES.items():
            print(f"{number}: {choice}")
        choice = input()
    return choice

def new_order(order_list):
    confirm = ''
    while confirm.lower() not in ['y', 'q']:
        name = valid_string("What's the name of the client? ")
        size = valid_size(VALID_SHIRT_SIZES)
        text = valid_string("What do they want it to say on the front? ")
        print("")
        print("{:>13}{:<16}\n{:>13}{:<16}\n{:>13}{:<16}".format("Name: ", name, "Shirt Size: ", size, "Custom Text: ", text))
        confirm = input("\nIs this OK? Input 'y' to continue, 'q' to cancel, or any other key to try again: ")
    if confirm.lower() == 'y':
        orderID = max(get_orderIDs(order_list)) + 1
        order_list[orderID] = OrderData(name, size, text)
        persist_orders(SAVE_FILE_NAME, order_list)

def valid_string(prompt):
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
    user_input = ""
    while user_input not in VALID_SHIRT_SIZES:
        clr_scrn()
        display_orders(order_list)
        print(f"What size shirt do they need? ({', '.join(VALID_SHIRT_SIZES)}) ", end = '')
        user_input = input()
    return user_input

def get_orderIDs(order_list):
    orderIDs = [0]
    for orderID in order_list:
        orderIDs.append(int(orderID))
    return orderIDs

def update_order_status(order_list):
    confirm = ""
    while confirm.lower() not in ["y", "q"]:
        orderID = select_valid_orderID(order_list)
        status = input("Enter the status of this order: ")
        confirm = input("\nIs this OK? Input 'y' to continue, 'q' to cancel, or any other key to try again: ")
    if confirm.lower() == "y":
        order = order_list[orderID]
        order.status = status
        persist_orders(SAVE_FILE_NAME, order_list)

def remove_order(order_list):
    confirm = ""
    while confirm.lower() not in ["y", "q"]:
        orderID = select_valid_orderID(order_list)
        confirm = input("\nIs this OK? Input 'y' to continue, 'q' to cancel, or any other key to try again: ")
    if confirm.lower() == "y":
        del order_list[orderID]
        persist_orders(SAVE_FILE_NAME, order_list)

def select_valid_orderID(order_list):
    orderID = -1
    failed = False
    while orderID not in get_orderIDs(order_list):
        clr_scrn()
        display_orders(order_list)
        if failed == True:
            print ("Please enter a valid Order ID")
        try:
            orderID = int(input(("Enter the Order ID: ")))
        except ValueError:
            failed = True
    return orderID

def persist_orders(SAVE_FILE_NAME, order_list):
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
    order_list = {}
    if os.path.isfile(SAVE_FILE_NAME):
        with open(SAVE_FILE_NAME) as save_file:
            savedorderlist = json.load(save_file)
        for savedorder in savedorderlist:
            orderID = savedorder["orderID"]
            order_list[orderID] = OrderData(savedorder["name"], savedorder["size"], savedorder["text"], savedorder["status"])
    return order_list

# Iniitalize constants and variables, and load save
VALID_CHOICES = {"1": "Input new order",
                 "2": "Update order status",
                 "3": "Remove order",
                 "q": "Exit"}
VALID_SHIRT_SIZES = ['small', 'medium', 'large']
SAVE_FILE_NAME = "orders.sav"

# Print welcome message & load save file
clr_scrn()
print("\nWelcome to my shirt production management program.")
print("I'm using it to practice basic classes, loops, functions, and storing and retrieving data\n")
input("Press any key to continue")

order_list = import_orders(SAVE_FILE_NAME)

# Main loop
while True:
    clr_scrn()
    choice = main_menu(order_list, VALID_CHOICES)
    if choice == '1':
        new_order(order_list)
    if choice == '2':
        update_order_status(order_list)
    if choice == '3':
        remove_order(order_list)
    elif choice == 'q':
        print("Thanks for using this program!")
        break

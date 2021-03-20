import os
import json

class Order():
    def __init__(self, name, size, text, orderID, status='PENDING'):
        self.orderID = orderID
        self.status = status
        self.name = name
        self.size = size
        self.text = text

def clr_scrn():
    os.system("clear")

def display_orders(orders):
    print("We have these orders in the system:\n")
    print("{:<10}\t{:<15}\t{:<15}\t{:<15}\t{:<15}".format("Order ID", "Order Status", "Client", "Shirt size", "Custom Text"))
    for order in orders:
        print("{:<15}\t{:<15}\t{:<15}\t{:<15}\t{:<15}\t".format(order.orderID, order.status, order.name, order.size, order.text))
    print("")

def main_menu(orders, VALID_CHOICES):
    choice = ""
    while choice not in VALID_CHOICES.keys():
        clr_scrn()
        display_orders(orders)
        print("What do you want to do?")
        for number, choice in VALID_CHOICES.items():
            print(f"{number}: {choice}")
        choice = input()
    return choice

def new_order(orders):
    confirm = ''
    while confirm.lower() not in ['y', 'q']:
        clr_scrn()
        display_orders(orders)
        name = valid_string("What's the name of the client? ")
        size = valid_size(VALID_SHIRT_SIZES)
        text = valid_string("What do they want it to say on the front? ")
        print("")
        display_input("Name: ", name)
        display_input("Shirt Size: ", size)
        display_input("Custom Text: ", text) 
        confirm = input("\nIs this OK? Input 'y' to continue, 'q' to cancel, or any other key to try again: ")
    if confirm.lower() == 'y':
        orderID = max(get_orderIDs(orders)) + 1
        orders.append(Order(name, size, text, orderID))
        persist_orders(SAVE_FILE_NAME, orders)

def display_input(field, text):
    print("{:>13}{:<16}".format(field, text))

def valid_string(prompt):
    while True:
        user_input = input(prompt)
        if len(user_input) < 16:
            break
        else:
            print("Please enter valid text less than 16 characters")
    return user_input

def valid_size(VALID_SHIRT_SIZES):
    user_input = ""
    while user_input not in VALID_SHIRT_SIZES:
        print(f"What size shirt do they need? ({', '.join(VALID_SHIRT_SIZES)}) ", end = '')
        user_input = input()
    return user_input

def get_orderIDs(orders):
    orderIDs = [0]
    for order in orders:
        orderIDs.append(int(order.orderID))
    return orderIDs

def persist_orders(SAVE_FILE_NAME, orders):
    order_list = []
    for order in orders:
        data = {}
        data["orderID"] = order.orderID
        data["status"] = order.status
        data["name"] = order.name
        data["size"] = order.size
        data["text"] = order.text
        order_list.append(data)
    with open(SAVE_FILE_NAME, 'w') as save_file:
        json.dump(order_list, save_file, indent=2)

def import_orders(SAVE_FILE_NAME):
    orders = []
    if os.path.isfile(SAVE_FILE_NAME):
        with open(SAVE_FILE_NAME) as save_file:
            order_list = json.load(save_file)
        for order in order_list:
            orders.append(Order(order['name'], order['size'], order['text'], order['orderID'], order['status']))
    return orders

# Iniitalize constants and variables, and load save
VALID_CHOICES = {"1": "Input new order",
                 "q": "Exit"}
VALID_SHIRT_SIZES = ['small', 'medium', 'large']
SAVE_FILE_NAME = "orders.sav"

# Print welcome message & load save file
clr_scrn()
print("\nWelcome to my shirt production management program.")
print("I'm using it to practice basic classes, loops, functions, and storing and retrieving data\n")
input("Press any key to continue")

orders = import_orders(SAVE_FILE_NAME)

# Main loop
while True:
    clr_scrn()
    choice = main_menu(orders, VALID_CHOICES)
    if choice == '1':
        clr_scrn()
        new_order(orders)
    elif choice == 'q':
        print("Thanks for using this program!")
        break

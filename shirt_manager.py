import os
import json

def clr_scrn():
    os.system("clear")

def init_data(SAVE_FILE_NAME):
    if not os.path.isfile(SAVE_FILE_NAME):
        with open(SAVE_FILE_NAME, 'w') as save_file:
            json.dump([], save_file)
    return json.load(open(SAVE_FILE_NAME))

def order_shirt():
    confirm = ''
    while confirm.lower() != 'y':
        clr_scrn()
        order = get_order()
        print(f"Name: {order['name']}\nShirt size: {order['size']}\nText: {order['text']}")
        confirm = input("Is this OK? Input 'y' to continue or any other key to try again ")
    return order

def get_order():
    order = {}
    order['status'] = 'PENDING'
    order['name'] = valid_string("What's your name? ")
    order['size'] = valid_size(VALID_SHIRT_SIZES)
    order['text'] = valid_string("What do you want it to say on the front? ")
    return order

def valid_string(prompt):
    while True:
        user_input = input(prompt)
        if len(user_input) < 16:
            break
        else:
            clr_scrn()
            print("Please enter valid text less than 16 characters")
    return user_input

def valid_size(VALID_SHIRT_SIZES):
    user_input = ""
    while user_input not in VALID_SHIRT_SIZES:
        print(f"What size shirt do you want? ({', '.join(VALID_SHIRT_SIZES)})")
        user_input = input()
    return user_input

def persist_orders(SAVE_FILE_NAME, orders):
    with open(SAVE_FILE_NAME, 'w') as save_file:
        json.dump(orders, save_file, indent=2)

def display_orders(orders):
    print("We have these orders in the system:\n")
    print("{:<16}\t{:<16}\t{:<16}\t{:<16}".format("Order Status", "Client", "Shirt size", "Custom Text"))
    for order in orders:
        print("{:<16}\t{:<16}\t{:<16}\t{:<16}".format(*order.values()))
    input("\nPress Enter to return to the menu")

def select_action(VALID_CHOICES):
    choice = ""
    while choice not in VALID_CHOICES.keys():
        clr_scrn()
        print("What do you want to do?")
        for number, choice in VALID_CHOICES.items():
            print(f"{number}: {choice}")
        choice = input()
    return choice

# Iniitalize constants and variables, and load save
VALID_CHOICES = {"1": "Order shirt",
                 "2": "Check orders",
                 "3": "Exit"}
VALID_SHIRT_SIZES = ['small', 'medium', 'large']
SAVE_FILE_NAME = "orders.sav"

# Print welcome message & load save file
clr_scrn()
print("\nWelcome to my shirt maker program.")
print("I'm using it to practice loops, functions, and storing and retrieving data\n")
input("Press any key to continue")

orders = init_data(SAVE_FILE_NAME)

# Main loop
while True:
    clr_scrn()
    choice = select_action(VALID_CHOICES)
    if choice == '1':
        clr_scrn()
        orders.append(order_shirt())
        persist_orders(SAVE_FILE_NAME, orders)
    elif choice == '2':
        clr_scrn()
        display_orders(orders)
    elif choice == '3':
        print("Thanks for using this program!")
        break

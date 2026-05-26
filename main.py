import os
import platform
from models.models import db, Account, EventHall, Ticket
from modules.auth import login, logout, register
from modules.halls import list_halls, create_hall, update_hall, delete_hall
from modules.tickets import list_tickets, create_ticket, update_ticket, delete_ticket, search_tickets
from structures.queue import Queue
from structures.stack import Stack

db.connect()
db.create_tables([Account, EventHall, Ticket])

current_account = None
sales_history = Stack()
refund_queue = Queue()


def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def list_halls_and_tickets():
    clear()
    print("\n── All Halls and Purchased Tickets ──")
    list_halls()
    list_tickets()
    input("  Press Enter to continue...")


def show_recent_sales_history():
    clear()
    print("\n── Recent Sales History (Stack) ────")
    if sales_history.is_empty():
        print("  No recent sales.")
    else:
        for index, ticket in enumerate(reversed(sales_history.items()), start=1):
            seat_info = f"Row {ticket.row}, Seat {ticket.seat}" if ticket.row and ticket.seat else "No seat assigned"
            hall_info = f"Hall [{ticket.hall_id}]" if ticket.hall_id else "No hall"
            print(f"  {index}. [{ticket.id}] {ticket.person} | {ticket.date} | ${ticket.price} | {seat_info} | {hall_info}")
    input("  Press Enter to continue...")


def show_refund_queue():
    clear()
    print("\n── Refund Queue ─────────────────────")
    if refund_queue.is_empty():
        print("  No customers in the refund queue.")
    else:
        for index, customer in enumerate(refund_queue.items(), start=1):
            print(f"  {index}. {customer}")
    input("  Press Enter to continue...")


def add_refund_request():
    clear()
    print("\n── Add Refund Request ─────────────")
    customer = input("  Customer name for refund: ").strip()
    if not customer:
        print("  Refund request cancelled.")
    else:
        refund_queue.enqueue(customer)
        print(f"  Added refund request for {customer}.")
    input("  Press Enter to continue...")


def process_refund_request():
    clear()
    print("\n── Process Next Refund ─────────────")
    customer = refund_queue.dequeue()
    if customer is None:
        print("  No refund requests in queue.")
    else:
        print(f"  Processing refund request for {customer}.")
    input("  Press Enter to continue...")


def refund_queue_menu():
    while True:
        clear()
        print("\n── Refund Queue Menu ───────────────")
        print("  1. Show refund queue")
        print("  2. Add refund request")
        print("  3. Process next refund")
        print("  4. Back")
        choice = input("  > ").strip()
        if choice == '1':
            show_refund_queue()
        elif choice == '2':
            add_refund_request()
        elif choice == '3':
            process_refund_request()
        elif choice == '4':
            break
        else:
            print("  Invalid choice.")


def hall_menu():
    while True:
        clear()
        print("\n── Hall Menu ────────────────────────")
        print("  1. List all halls")
        print("  2. Create hall")
        print("  3. Update hall")
        print("  4. Delete hall")
        print("  5. Back")
        choice = input("  > ").strip()
        if choice == '1':
            clear()
            list_halls()
            input("  Press Enter to continue...")
        elif choice == '2':
            clear()
            create_hall()
            input("  Press Enter to continue...")
        elif choice == '3':
            clear()
            update_hall()
            input("  Press Enter to continue...")
        elif choice == '4':
            clear()
            delete_hall()
            input("  Press Enter to continue...")
        elif choice == '5':
            break
        else:
            print("  Invalid choice.")


def ticket_menu():
    while True:
        clear()
        print("\n── Ticket Menu ──────────────────────")
        print("  1. List all tickets")
        print("  2. Create ticket")
        print("  3. Search ticket by person")
        print("  4. Update ticket")
        print("  5. Delete ticket")
        print("  6. Back")
        choice = input("  > ").strip()
        if choice == '1':
            clear()
            list_tickets()
            input("  Press Enter to continue...")
        elif choice == '2':
            clear()
            create_ticket(sales_history)
            input("  Press Enter to continue...")
        elif choice == '3':
            clear()
            search_tickets()
            input("  Press Enter to continue...")
        elif choice == '4':
            clear()
            update_ticket()
            input("  Press Enter to continue...")
        elif choice == '5':
            clear()
            delete_ticket()
            input("  Press Enter to continue...")
        elif choice == '6':
            break
        else:
            print("  Invalid choice.")


def main_menu():
    global current_account
    while True:
        clear()
        print("\n── Main Menu ────────────────────────")
        print(f"  Logged in as: {current_account.username}")
        print("  1. List all halls and tickets")
        print("  2. Manage halls")
        print("  3. Manage tickets")
        print("  4. Refund queue")
        print("  5. Recent sales history")
        print("  6. Log out")
        choice = input("  > ").strip()
        if choice == '1':
            list_halls_and_tickets()
        elif choice == '2':
            hall_menu()
        elif choice == '3':
            ticket_menu()
        elif choice == '4':
            refund_queue_menu()
        elif choice == '5':
            show_recent_sales_history()
        elif choice == '6':
            logout(current_account)
            current_account = None
            break
        else:
            print("  Invalid choice.")


def auth_menu():
    global current_account
    while True:
        clear()
        print("\n── Ticket Program ───────────────────")
        print("  1. Log in to account")
        print("  2. Register new account")
        print("  3. Exit")
        choice = input("  > ").strip()
        if choice == '1':
            clear()
            current_account = login()
            if current_account:
                main_menu()
            else:
                input("  Press Enter to continue...")
        elif choice == '2':
            clear()
            register()
            input("  Press Enter to continue...")
        elif choice == '3':
            clear()
            print("  Goodbye!")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    auth_menu()
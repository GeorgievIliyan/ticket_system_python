import os
import platform
from models.models import db, Account, EventHall, Ticket
from modules.auth import login, logout, register
from modules.halls import list_halls, create_hall, update_hall, delete_hall
from modules.tickets import list_tickets, create_ticket, update_ticket, delete_ticket

db.connect()
db.create_tables([Account, EventHall, Ticket])

current_account = None


def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


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
        print("  3. Update ticket")
        print("  4. Delete ticket")
        print("  5. Back")
        choice = input("  > ").strip()
        if choice == '1':
            clear()
            list_tickets()
            input("  Press Enter to continue...")
        elif choice == '2':
            clear()
            create_ticket()
            input("  Press Enter to continue...")
        elif choice == '3':
            clear()
            update_ticket()
            input("  Press Enter to continue...")
        elif choice == '4':
            clear()
            delete_ticket()
            input("  Press Enter to continue...")
        elif choice == '5':
            break
        else:
            print("  Invalid choice.")


def main_menu():
    global current_account
    while True:
        clear()
        print("\n── Main Menu ────────────────────────")
        print(f"  Logged in as: {current_account.username}")
        print("  1. Manage halls")
        print("  2. Manage tickets")
        print("  3. Log out")
        choice = input("  > ").strip()
        if choice == '1':
            hall_menu()
        elif choice == '2':
            ticket_menu()
        elif choice == '3':
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
from datetime import date
from models.models import EventHall, Ticket


def list_halls():
    halls = list(EventHall.select())
    if not halls:
        print("  No event halls found.")
        return
    print("\n  ── Event Halls ──────────────────────")
    for h in halls:
        print(f"  [{h.id}] Capacity: {h.capacity} | Rows: {h.rows} | Created: {h.created_on}")
    print()


def create_hall():
    try:
        capacity = int(input("  Capacity: ").strip())
        rows = int(input("  Number of rows: ").strip())
    except ValueError:
        print("  Invalid input — capacity and rows must be numbers.")
        return
    hall = EventHall.create(capacity=capacity, rows=rows, created_on=date.today())
    print(f"  Hall [{hall.id}] created successfully.")


def update_hall():
    list_halls()
    try:
        hall_id = int(input("  Hall ID to update: ").strip())
        hall = EventHall.get_or_none(EventHall.id == hall_id)
        if not hall:
            print("  Hall not found.")
            return
        capacity = input(f"  New capacity [{hall.capacity}]: ").strip()
        rows = input(f"  New rows [{hall.rows}]: ").strip()
        if capacity:
            hall.capacity = int(capacity)
        if rows:
            hall.rows = int(rows)
        hall.save()
        print(f"  Hall [{hall_id}] updated successfully.")
    except ValueError:
        print("  Invalid input.")


def delete_hall():
    list_halls()
    try:
        hall_id = int(input("  Hall ID to delete: ").strip())
        hall = EventHall.get_or_none(EventHall.id == hall_id)
        if not hall:
            print("  Hall not found.")
            return
        confirm = input(f"  Delete hall [{hall_id}]? This will also remove its tickets. (y/n): ").strip().lower()
        if confirm == 'y':
            Ticket.delete().where(Ticket.hall == hall).execute()
            hall.delete_instance()
            print(f"  Hall [{hall_id}] deleted.")
    except ValueError:
        print("  Invalid input.")
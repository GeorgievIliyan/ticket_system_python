import os
import qrcode
from datetime import datetime
from models.models import Ticket, EventHall


QR_DIR = "qr_codes"


def _generate_qr(ticket: Ticket):
    os.makedirs(QR_DIR, exist_ok=True)
    data = (
        f"Ticket ID: {ticket.id}\n"
        f"Person: {ticket.person}\n"
        f"Date: {ticket.date}\n"
        f"Price: ${ticket.price}\n"
        f"Row: {ticket.row or 'N/A'}\n"
        f"Seat: {ticket.seat or 'N/A'}\n"
        f"Hall: {ticket.hall_id or 'N/A'}"
    )
    img = qrcode.make(data)
    path = os.path.join(QR_DIR, f"ticket_{ticket.id}_{ticket.person.replace(' ', '_')}.png")
    img.save(path)
    print(f"  QR code saved to: {path}")


def list_tickets():
    tickets = list(Ticket.select())
    if not tickets:
        print("  No tickets found.")
        return
    print("\n  ── Tickets ──────────────────────────")
    for t in tickets:
        seat_info = f"Row {t.row}, Seat {t.seat}" if t.row and t.seat else "No seat assigned"
        hall_info = f"Hall [{t.hall_id}]" if t.hall_id else "No hall"
        print(f"  [{t.id}] {t.person} | {t.date} | ${t.price} | {seat_info} | {hall_info}")
    print()


def create_ticket():
    person = input("  Person name: ").strip()
    try:
        price = float(input("  Price: ").strip())
        event_date = datetime.strptime(input("  Event date (YYYY-MM-DD): ").strip(), "%Y-%m-%d").date()
    except ValueError:
        print("  Invalid price or date format.")
        return
    row = input("  Row (leave blank if none): ").strip() or None
    seat = input("  Seat (leave blank if none): ").strip() or None

    halls = list(EventHall.select())
    hall = None
    if halls:
        print("  Available halls:")
        for h in halls:
            print(f"    [{h.id}] Capacity: {h.capacity} | Rows: {h.rows}")
        hall_id = input("  Hall ID (leave blank for none): ").strip()
        if hall_id:
            hall = EventHall.get_or_none(EventHall.id == int(hall_id))
            if not hall:
                print("  Hall not found, leaving unassigned.")

    ticket = Ticket.create(person=person, price=price, date=event_date, row=row, seat=seat, hall=hall)
    print(f"  Ticket [{ticket.id}] created for {person}.")
    _generate_qr(ticket)


def update_ticket():
    list_tickets()
    try:
        ticket_id = int(input("  Ticket ID to update: ").strip())
        ticket = Ticket.get_or_none(Ticket.id == ticket_id)
        if not ticket:
            print("  Ticket not found.")
            return
        person = input(f"  Person [{ticket.person}]: ").strip()
        price = input(f"  Price [{ticket.price}]: ").strip()
        event_date = input(f"  Date [{ticket.date}] (YYYY-MM-DD): ").strip()
        row = input(f"  Row [{ticket.row}]: ").strip()
        seat = input(f"  Seat [{ticket.seat}]: ").strip()
        if person:
            ticket.person = person
        if price:
            ticket.price = float(price)
        if event_date:
            ticket.date = datetime.strptime(event_date, "%Y-%m-%d").date()
        if row:
            ticket.row = row
        if seat:
            ticket.seat = seat
        ticket.save()
        _generate_qr(ticket)
        print(f"  Ticket [{ticket_id}] updated.")
    except ValueError:
        print("  Invalid input.")


def delete_ticket():
    list_tickets()
    try:
        ticket_id = int(input("  Ticket ID to delete: ").strip())
        ticket = Ticket.get_or_none(Ticket.id == ticket_id)
        if not ticket:
            print("  Ticket not found.")
            return
        confirm = input(f"  Delete ticket [{ticket_id}] for {ticket.person}? (y/n): ").strip().lower()
        if confirm == 'y':
            # Remove QR code file if it exists
            path = os.path.join(QR_DIR, f"ticket_{ticket.id}_{ticket.person.replace(' ', '_')}.png")
            if os.path.exists(path):
                os.remove(path)
            ticket.delete_instance()
            print(f"  Ticket [{ticket_id}] deleted.")
    except ValueError:
        print("  Invalid input.")
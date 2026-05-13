from datetime import date

class EvenetHall:
    def __init__(self, capacity: int, rows: int, created_on: date):
        self.capacity = capacity
        self.rows = rows
        self.created_on = created_on

    def __str__(self):
        return f"Event hall created on {str(self.created_on)} with capacity of {self.capacity}."
        

class Ticket:
    def __init__(self, price: float | int, date: date, person: str, seat: None | str, row: None | str):
        self.price = price
        self.date = date
        self.person = person
        self.row = row
        self.seat = seat

    def __str__(self):
        return f"Ticket for {self.person} for {self.date}."
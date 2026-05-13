from datetime import date

class EvenetHall:
    def __init__(self, capacity: int, rows: int):
        self.capacity = capacity
        self.rows = rows

class Ticket:
    def __init__(self, price: float | int, date: date, person: str):
        self.price = price
        self.date = date
        self.person = person
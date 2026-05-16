from datetime import date
from peewee import *

db = SqliteDatabase('events.db')


class BaseModel(Model):
    class Meta:
        database = db


class EventHall(BaseModel):
    capacity = IntegerField()
    rows = IntegerField()
    created_on = DateField(default=date.today)

    def __str__(self):
        return f"Event hall created on {str(self.created_on)} with capacity of {self.capacity}."

    class Meta:
        table_name = 'event_halls'


class Ticket(BaseModel):
    price = DecimalField(decimal_places=2)
    date = DateField()
    person = CharField(max_length=255)
    seat = CharField(max_length=50, null=True)
    row = CharField(max_length=50, null=True)
    hall = ForeignKeyField(EventHall, backref='tickets', null=True)

    def __str__(self):
        return f"Ticket for {self.person} for {self.date}."

    class Meta:
        table_name = 'tickets'


class Account(BaseModel):
    username = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)
    created_on = DateField(default=date.today)
    token = CharField(max_length=255, null=True)

    def __str__(self):
        return f"Account with username {self.username} created on {str(self.created_on)}"

    class Meta:
        table_name = 'accounts'
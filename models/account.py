from datetime import date

class Account:
    def __init__(self, username: str, password, created_on: date, token: None):
        self.username = username
        self._password = password
        self.created_on = created_on
        self.token = token

    def __str__(self):
        return f"Account with username {self.username} created on {str(self.created_on)}"
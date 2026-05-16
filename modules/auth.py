import hashlib
import getpass
from datetime import date
from models.models import Account


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def _generate_token(username: str) -> str:
    raw = f"{username}{date.today()}".encode()
    return hashlib.sha256(raw).hexdigest()


def register() -> Account | None:
    username = input("  Username: ").strip()
    if Account.select().where(Account.username == username).exists():
        print(f"  Username '{username}' is already taken.")
        return None
    password = getpass.getpass("  Password: ")
    account = Account.create(
        username=username,
        password=_hash_password(password),
        created_on=date.today(),
        token=None,
    )
    print(f"  Account '{username}' created successfully.")
    return account


def login() -> Account | None:
    username = input("  Username: ").strip()
    password = getpass.getpass("  Password: ")
    account = Account.get_or_none(Account.username == username)
    if account is None or account.password != _hash_password(password):
        print("  Invalid username or password.")
        return None
    account.token = _generate_token(username)
    account.save()
    print(f"  Welcome back, {username}!")
    return account


def logout(account: Account) -> None:
    account.token = None
    account.save()
    print("  Logged out successfully.")
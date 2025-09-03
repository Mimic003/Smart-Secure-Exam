import os
import json
import bcrypt

AUTH_FILE = os.path.join(os.path.dirname(__file__), "data", "admin_auth.json")

def _ensure_dir():
    os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)

def is_registered():
    return os.path.exists(AUTH_FILE)

def signup(username: str, password: str) -> None:
    _ensure_dir()
    if is_registered():
        raise ValueError("Admin already registered. Please log in.")
    if not username or not password:
        raise ValueError("Username and password are required.")
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    data = {"username": username, "pw_hash": pw_hash}
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def login(username: str, password: str) -> bool:
    if not is_registered():
        raise ValueError("No admin registered. Please sign up first.")
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if username != data.get("username"):
        return False
    pw_hash = data.get("pw_hash", "").encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), pw_hash)

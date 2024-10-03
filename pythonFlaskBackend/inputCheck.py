import re


def username_check(username):
    return len(username) >= 8 and len(username) <= 16


def password_check(password):
    return len(password) >= 8 and re.match(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$", password)

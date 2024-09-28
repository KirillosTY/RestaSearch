import re


def usernameCheck(username):
  return  len(username) >= 8 and len(username) <= 16

def passwordCheck(password):
  return len(password) >= 8 and re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$", password)

     
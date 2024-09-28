import os
import userDB
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

def jsonifyUser(username,rawData):
  user_data = {
          "id": rawData[0],
          "isAdmin": rawData[1],
          "password": rawData[2],
          "username": username
      }
  return user_data

def login(username, password):
  result = userDB.login(username)
  user = jsonifyUser(username,(result.fetchone()))
  print(user,"its this alright")
  if not user:
    return False;
  elif check_password_hash(user.get("password"), password):
    
    userSessionSetup(user)

    return True;
  else: 
    return False;


def create(username,password, isAdmin):
    
  hash_password = generate_password_hash(password)
  try:
    print( userDB.create(username,hash_password,isAdmin))

  except:
    return False;

  print("no ei toiminut")
  return  login(username,password);

def checkSession():
      if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def isAdmin():
       if session["isAdmin"] != request.form["True"]:
        abort(403)






def userSessionSetup(user):

  session["user"] = user.get("username")
  session["user_id"] = user.get("id")
  session["isAdmin"] = user.get("isAdmin")
  session["csrf_token"] = secrets.token_hex(16)

def deleteSession():
  del session["user"] 
  del session["user_id"]
  del session["isAdmin"]
  del session["csrf_token"]
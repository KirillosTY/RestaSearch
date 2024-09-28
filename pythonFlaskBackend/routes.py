from app import app
from flask import render_template, request, redirect, session
import users
import  restaurantsHandler as restaurantsHandler
from inputCheck import usernameCheck,passwordCheck
import re
@app.route('/')
def default():
  user = session.get("user")
  print(user)
  if not user:
      return redirect("/login")
      print("käydäänkö?!")
  else:
    print("ei käydä onneksi")
    return render_template("start.html")  

@app.route('/login', methods=['GET','POST'])
def login():
 
  print(request.method)
  if request.method == 'GET':
    return render_template('login.html', currentRoute="login.html")
  username = request.form["username"]
  password = request.form["password"]
  
  if not (passwordCheck(password)):
      return render_template("createUser.html", message="Salasanan pitää olla ainakin 8 merkkiä sisältäen yhden pienen ja ison kirjaimen sekä numeron. Onnea elämään noilla salasanoilla <3.")
  elif not usernameCheck(username):
      return render_template("createUser.html", message="Käyttäjätunnuksen pitää olla 8-16 merkkiä")
    
  if not users.login(username,password):
     #   return render_template("error.html")
     print("error handling login")

  return redirect("/")


@app.route('/logout', methods=['GET','POST'])
def logout():
  print("käydään")
  users.deleteSession()
  return redirect("/")

@app.route('/create', methods=['GET','POST'])
def create():

  print(request.method)
  if request.method == 'GET':
    return render_template('createUser.html')
  
  username = request.form["username"]
  password = request.form["password"]
  passwordRepeat = request.form["passwordRepeat"]
  isAdmin = request.form.get("admin",'false')
  if not (passwordRepeat == password):
    return render_template("createUser.html", message="Salasanan pitää täsmätä")
  elif not usernameCheck(username):
    return render_template("createUser.html", message="Käyttäjätunnuksen pitää olla 8-16 merkkiä")
  elif not (passwordCheck(password) and passwordCheck(passwordRepeat)):
    print("käydään mitä vittua tapahttuu")
    return render_template("createUser.html", message="Salasanan pitää olla ainakin 8 merkkiä sisältäen yhden pienen ja ison kirjaimen sekä numeron. Onnea elämään noilla salasanoilla <3.")
  elif not users.create(username,password, isAdmin):
        return render_template("createUser.html", message="Käyttäjätunnus on jo käytössä tai verkossasi on häiriöitä. Todennäköisesti itse aiheutit.")
    #proper error handling to catch if it's an DB issue or user.

    
  return redirect("/")  


@app.route('/restaurants', methods=['GET','POST'])
def restaurants():
  restaurantList = restaurantsHandler.getAll()
  favouriteRestList= restaurantsHandler.getFavourites(session.get("user_id"))
  if restaurantList== None:
    restaurantList = []
  #restaurantFavourites = restaurantsHandler.getFavourites()
  print(restaurantList, "käydään täällä")
  if request.method == 'GET':
    return render_template('restaurants.html', 
                           restaurants = restaurantList,
                           favouritedRestaurant = favouriteRestList)
  

@app.route('/createRestaurant', methods=['GET','POST'])
def createRestaurant():
  
  if request.method == 'GET':
    return render_template('createRestaurant.html')
  
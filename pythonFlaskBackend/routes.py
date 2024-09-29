from app import app
from flask import render_template, request, redirect, session
import users
import restaurants
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
def restaurantLists():
  restaurantList = restaurants.getAll()
  favouriteRestList= restaurants.getFavourites(session.get("user_id"))
  if restaurantList== None:
    restaurantList = []
  #restaurantFavourites = restaurantsHandler.getFavourites()

  if request.method == 'GET':
    return render_template('restaurants.html', 
                           restaurants = restaurantList,
                           favouritedRestaurant = favouriteRestList)
  

@app.route('/restaurants/<int:restaurant_id>', methods=['GET','POST'])
def single_restaurant(restaurant_id):
  single_rest = restaurants.getSingle(restaurant_id)
  if single_rest== None:
    single_rest = []
  #restaurantFavourites = restaurantsHandler.getFavourites()

  if request.method == 'GET':
    return render_template('singleRestaurant.html', restaurant = single_rest  )
  


@app.route('/createRestaurant', methods=['GET','POST'])
def createRestaurant():
  
  if request.method == 'GET':
    return render_template('createRestaurant.html')
  
  name = request.form["name"]
  description = request.form["description"]
  address = request.form.get("address",None)
  mondayOpen = request.form.get("mondayOpen",None)
  tuesdayOpen = request.form.get("tuesdayOpen",None)
  wednesdayOpen = request.form.get("wednesdayOpen",None)
  thursdayOpen = request.form.get("thursdayOpen",None)
  fridayOpen = request.form.get("fridayOpen",None)
  saturdayOpen = request.form.get("saturdayOpen",None)
  sundayOpen = request.form.get("sundayOpen",None)

  mondayClose = request.form.get("mondayClose",None)
  tuesdayClose =request.form.get("tuesdayClose",None)
  wednesdayClose =request.form.get("wednesdayClose",None)
  thursdayClose =request.form.get("thursdayClose",None)
  fridayClose =request.form.get("fridayClose",None)
  saturdayClose =request.form.get("saturdayClose",None)
  sundayClose =request.form.get("sundayClose",None) 

  genre = request.form.get("genre",None)

  restaurant = restaurants.createRestaurant(name,description, address, 
                               mondayOpen,mondayClose,
                               tuesdayOpen, tuesdayClose,
                               wednesdayOpen,wednesdayClose,
                               thursdayOpen,thursdayClose,
                               fridayOpen, fridayClose,
                               saturdayOpen, saturdayClose,
                               sundayOpen, sundayClose,
                               genre)
  print(restaurant,'seconds')
  return redirect("/restaurants/"+str(restaurant[0]))


  
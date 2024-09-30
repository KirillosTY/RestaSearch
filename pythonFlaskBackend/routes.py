from app import app
from flask import render_template, request, redirect, session, url_for
import users
import restaurants
from inputCheck import usernameCheck,passwordCheck
import re
@app.route('/')
def default(): 
  user = session.get("user")
  print(user)
  favouriteRestList= restaurants.getFavourites(session.get("user_id"))
  friendsFound = users.getFavouriteFriends(session.get("user_id"))
  if not favouriteRestList:
    #Add error hadling for both 
    favouriteRestList = []
  if not user:
      return redirect("/login")
      print("käydäänkö?!")
  else:
    print("ei käydä onneksi")
    return render_template("start.html", favouriteRestaurants = favouriteRestList, friends = friendsFound)  

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
  rest_and_reviews = restaurants.getSingle(restaurant_id)
  single_rest = rest_and_reviews[0]
  single_rest_reviews =  rest_and_reviews[1]
  if single_rest== None:
    single_rest = []
    print("tyhjennetty")

  #restaurantFavourites = restaurantsHandler.getFavourites()
    print("käydään")
  print(single_rest,"käydään?!!t")
  if request.method == 'POST':
    print("käydään post")
    if request.form['edit'] =='muokkaa':
        print(single_rest,"käydään edit")
        print("käydään edit")

    return redirect("/editRestaurants/"+str(single_rest[0]))
  elif request.method == 'GET':
    return render_template('singleRestaurant.html', restaurant = single_rest,
                           reviews = single_rest_reviews  )
  

@app.route('/editRestaurants/<int:restaurant_id>', methods=['GET','POST'])
def edit_restaurant(restaurant_id):
    rest_and_reviews = restaurants.getSingle(restaurant_id)      
    if request.method == 'GET':
      return render_template('singleEditRest.html',id=id, restaurant = rest_and_reviews[0])
    


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

    restaurant_updated = restaurants.update_single(restaurant_id,name,description, address, 
                                mondayOpen,mondayClose,
                                tuesdayOpen, tuesdayClose,
                                wednesdayOpen,wednesdayClose,
                                thursdayOpen,thursdayClose,
                                fridayOpen, fridayClose,
                                saturdayOpen, saturdayClose,
                                sundayOpen, sundayClose,
                                genre)
    print(restaurant_updated,'seconds')

    return render_template('singleEditRest.html',id=id, 
                          restaurant = restaurant_updated[0], 
                          success_message="Tiedot tallentuneet")



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


@app.route('/friends')
def friends(): 
  user = session.get("user")
  print(user)
  friendsFound = users.getFavouriteFriends(session.get("user_id"))
  if not friendsFound:
    #Add error hadling for both 
    friendsFound = []
  if not user:
      return redirect("/login")
      print("käydäänkö?!")
  else:
    print("ei käydä onneksi")
    return render_template("friends.html", friends = friendsFound)  

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
  reviews = restaurants.get_user_reviews(session.get("user_id"))
  if not favouriteRestList:
    #Add error hadling for both 
    favouriteRestList = []
  if not user:
      return redirect("/login")
      print("käydäänkö?!")
  else:
    print("ei käydä onneksi")
    return render_template("start.html", favouriteRestaurants = favouriteRestList, reviews = reviews)  

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

  print('this here', favouriteRestList)
  if not restaurantList:
    restaurantList = []
  if not favouriteRestList:
    favouriteRestList = []
  #restaurantFavourites = restaurantsHandler.getFavourites()
  search_text = request.form.get('restaurant_query',False)
  print(search_text,' catch?')
  if request.method == 'POST' and search_text: 
      rest_found = restaurants.find_restaurant(search_text)
      print(rest_found, "käydääää")
      return render_template('restaurants.html', 
                            restaurants = rest_found,
                            favouritedRestaurant = favouriteRestList,
                            searched = True)      

  elif request.method == 'GET' or search_text == '':
    return render_template('restaurants.html', 
                           restaurants = restaurantList,
                           favouritedRestaurant = favouriteRestList,
                            searched = False)
  
@app.route('/restaurants/requests', methods=['GET','POST'])
def restaurant_requests():
  restaurantList = restaurants.get_all_requests()
  if not restaurantList:
    restaurantList = []
  

  if request.method == 'GET':
    return render_template('restaurant_requested.html', 
                           restaurants = restaurantList)
    
  
  


@app.route('/restaurants/<int:restaurant_id>', methods=['GET','POST'])
def single_restaurant(restaurant_id):
  rest_and_reviews = restaurants.getSingle(restaurant_id)
  single_rest = rest_and_reviews[0]
  single_rest_reviews =  rest_and_reviews[1]
  if single_rest== None:
    single_rest = []
    rest_and_reviews= []

  user_id = session.get('user_id')
  restaurant_favourited = restaurants.check_favourite(user_id, single_rest[0])
  
  left_review = False;
  for review in single_rest_reviews:
    if review[0] == user_id:
      left_review = review;
   
  if request.method == 'POST':
    if request.form.get('edit',False) == 'edit':
      return redirect("/editRestaurants/"+str(single_rest[0]))
    elif request.form.get('remove',False) == 'remove':
      result =restaurants.delete_restaurant(restaurant_id)
      if result:
        return render_template('singleRestaurant.html', restaurant = [],
                           reviews = [], success_message = "Ravintola "+result[1]+" on nyt poistettu")
    elif request.form.get('favourite',False) == 'favourite': 
          user_id = session.get('user_id')
          restaurants.create_favourite(user_id,restaurant_id)
          #succesmessage
          return redirect("/restaurants/"+str(single_rest[0])) 
    elif request.form.get('remove_favourite',False) == 'remove_favourite': 
          
          user_id = session.get('user_id')
          restaurants.remove_favourite(user_id,restaurant_id)
          #succesmessage
          return redirect("/restaurants/"+str(single_rest[0])) 
      
    elif request.form.get('review',False) == 'review': 
          rating = request.form['rating']
          comment = request.form['comment']
          user_id = session.get('user_id')
          restaurants.create_review(user_id,restaurant_id, rating, comment)
          return redirect("/restaurants/"+str(single_rest[0])) 

    elif request.form.get('review_update',False) == 'review_update':
        print("Here!?!")
        rating = request.form['rating']
        comment = request.form['comment']
        user_id = session.get('user_id')
        restaurants.update_review(user_id, restaurant_id, rating, comment)
        return redirect("/restaurants/"+str(single_rest[0])) 
    elif request.form.get('review_delete',False) == 'review_delete':
        user_id = session.get('user_id')
        result = restaurants.delete_review(user_id, restaurant_id)
        single_rest_reviews = restaurants.get_reviews(restaurant_id)
        if result:
          return render_template('singleRestaurant.html', restaurant = single_rest,
                           reviews = [], success_message = "Arvostelu on nyt poistettu")
        return render_template('singleRestaurant.html', restaurant = single_rest,
                           reviews = single_rest_reviews, message = "Jotain meni pieleen, yritä myöhemmin uudelleen")
    else:
        return render_template('singleRestaurant.html', restaurant = single_rest,
                           reviews = single_rest_reviews, message = "Jotain meni pieleen, yritä myöhemmin uudelleen")
  elif request.method == 'GET':
    return render_template('singleRestaurant.html', restaurant = single_rest,
                           reviews = single_rest_reviews, reviewed =  left_review, favourited = restaurant_favourited)
    
  
#def handle_reviews():
   #make sure to implement


@app.route('/editRestaurants/<int:restaurant_id>', methods=['GET','POST'])
def edit_restaurant(restaurant_id):
    if session.get("isAdmin") == False:
       redirect('/')

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

@app.route('/restaurants/<int:restaurant_id>/request', methods=['GET','POST'])
def accept_restaurant(restaurant_id):
    if session.get("isAdmin") == False:
       redirect('/')

    rest= restaurants.get_single_request(restaurant_id)      
    if request.method == 'GET':
      return render_template('single_request.html',id=id, restaurant = rest)
  

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

    restaurant_accepted = restaurants.createRestaurant(name,description, address, 
                                mondayOpen,mondayClose,
                                tuesdayOpen, tuesdayClose,
                                wednesdayOpen,wednesdayClose,
                                thursdayOpen,thursdayClose,
                                fridayOpen, fridayClose,
                                saturdayOpen, saturdayClose,
                                sundayOpen, sundayClose,
                                genre)
    print(restaurant_accepted,'seconds')

    if(restaurant_accepted):
       restaurants.delete_request(restaurant_id)

    return redirect('/restaurants/'+str(restaurant_accepted[0]))




@app.route('/createRestaurant', methods=['GET','POST'])
def createRestaurant():
  isAdmin = session.get("isAdmin")
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
  if(isAdmin):
    restaurant = restaurants.createRestaurant(name,description, address, 
                               mondayOpen,mondayClose,
                               tuesdayOpen, tuesdayClose,
                               wednesdayOpen,wednesdayClose,
                               thursdayOpen,thursdayClose,
                               fridayOpen, fridayClose,
                               saturdayOpen, saturdayClose,
                               sundayOpen, sundayClose,
                               genre)
  else :
     restaurant = restaurants.create_request(name,description, address, 
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

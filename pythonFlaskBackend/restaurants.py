import os
import restaurantDB 
from flask import abort, request, session
import secrets


def getAll():
  restaurants = restaurantDB.getRestaurants().fetchall() 

  if not restaurants:
    print("something went wrong")
    return False;

  return restaurants

def get_all_requests():
  restaurant_requests = restaurantDB.get_all_requests().fetchall()
  if not restaurant_requests:
    print("something went wrong")
    return False;

  return restaurant_requests

def getFavourites(id):
  restaurants = restaurantDB.getFavouriteRestaurants(id).fetchall() 
  if not restaurants:
    print("something went wrong")
    return False;

  return restaurants

def check_favourite(user_id, restaurant_id):
  restaurants = restaurantDB.check_favourite(user_id, restaurant_id).fetchall() 
  if not restaurants:
    print("something went wrong")
    return False;

  return restaurants

def getSingle(id):
  singleRest = restaurantDB.getSingle(id).fetchone()
  singleRestReview = restaurantDB.getReviews(id).fetchall()

  if not singleRest:
    return False
  
  return [singleRest,singleRestReview]

def get_single_request(id):
  singleRest = restaurantDB.get_single_request(id).fetchone()

  if not singleRest:
    return False
  
  return singleRest


    
def get_reviews(restaurant_id):
  singleRestReview = restaurantDB.getReviews(restaurant_id).fetchall()

  return singleRestReview 

def get_user_reviews(user_id):
  singleRestReview = restaurantDB.get_user_reviews(user_id).fetchall()

  return singleRestReview 


def find_restaurant(search_text):
  searched_restaurants = restaurantDB.find_restaurant(search_text).fetchall()
  return searched_restaurants

def createRestaurant(name, description,address, 
                     mondayOpen,mondayClose,
                     tuesdayOpen,tuesdayClose,
                     wednesdayOpen, wednesdayClose,
                     thursdayOpen, thursdayClose,
                     fridayOpen, fridayClose,
                     saturdayOpen, saturdayClose,
                     sundayOpen, sundayClose,
                     genret):

  result = restaurantDB.createRestaurant(name,description,address).fetchone()
  if result:

   hours = restaurantDB.create_hours(result[0],
                      checkNone(mondayOpen),checkNone(mondayClose),
                      checkNone(tuesdayOpen),checkNone(tuesdayClose),
                      checkNone(wednesdayOpen), checkNone(wednesdayClose),
                      checkNone(thursdayOpen), checkNone(thursdayClose),
                      checkNone(fridayOpen), checkNone(fridayClose),
                      checkNone(saturdayOpen), checkNone(saturdayClose),
                      checkNone(sundayOpen), checkNone(sundayClose))
   print(hours,'tunnit')
  return result 

def create_request(name, description,address, 
                     mondayOpen,mondayClose,
                     tuesdayOpen,tuesdayClose,
                     wednesdayOpen, wednesdayClose,
                     thursdayOpen, thursdayClose,
                     fridayOpen, fridayClose,
                     saturdayOpen, saturdayClose,
                     sundayOpen, sundayClose,
                     genret):

  result = restaurantDB.create_restaurant_request(name,description,address).fetchone()
  if result:

   hours = restaurantDB.create_request_hours(result[0],
                      checkNone(mondayOpen),checkNone(mondayClose),
                      checkNone(tuesdayOpen),checkNone(tuesdayClose),
                      checkNone(wednesdayOpen), checkNone(wednesdayClose),
                      checkNone(thursdayOpen), checkNone(thursdayClose),
                      checkNone(fridayOpen), checkNone(fridayClose),
                      checkNone(saturdayOpen), checkNone(saturdayClose),
                      checkNone(sundayOpen), checkNone(sundayClose))
   print(hours,'tunnit')
  return result 

def create_review(user_id, restaurant_id, rating,comment):
  result = restaurantDB.create_review(user_id, restaurant_id, rating, comment).fetchone()
  return result

    
def create_favourite(user_id,restaurant_id):
  favourited = restaurantDB.create_favourite(user_id,restaurant_id).fetchall()

  return favourited 


def update_review(user_id, restaurant_id, rating,comment):
  result = restaurantDB.update_review(user_id, restaurant_id, rating, comment).fetchone()
  print(result)
  return result



def update_single(id,name, description,address, 
                     mondayOpen,mondayClose,
                     tuesdayOpen,tuesdayClose,
                     wednesdayOpen, wednesdayClose,
                     thursdayOpen, thursdayClose,
                     fridayOpen, fridayClose,
                     saturdayOpen, saturdayClose,
                     sundayOpen, sundayClose,
                     genret):

  restaurantDB.update_restaurant(id,name, description,address).fetchone()
  

  restaurantDB.update_hours(id,
                      checkNone(mondayOpen),checkNone(mondayClose),
                      checkNone(tuesdayOpen),checkNone(tuesdayClose),
                      checkNone(wednesdayOpen), checkNone(wednesdayClose),
                      checkNone(thursdayOpen), checkNone(thursdayClose),
                      checkNone(fridayOpen), checkNone(fridayClose),
                      checkNone(saturdayOpen), checkNone(saturdayClose),
                      checkNone(sundayOpen), checkNone(sundayClose))
    
  return getSingle(id)
    

def delete_restaurant(id):
  result = restaurantDB.delete_restaurant(id).fetchone()
  return result

def delete_request(id):
  result = restaurantDB.delete_restaurant_request(id).fetchone()
  print('deleting went to shit', result)
  return result

def delete_review(user_id, restaurant_id):
  result = restaurantDB.delete_review(user_id, restaurant_id).fetchone()
  return result

def remove_favourite(user_id,restaurant_id):
  removed = restaurantDB.delete_favourited(user_id,restaurant_id).fetchone()

  return removed

def checkNone(time):
  if time == "":
    return None
  
  return time
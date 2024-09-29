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


def getFavourites(id):
  restaurants = restaurantDB.getFavouriteRestaurants(id).fetchall() 
  if not restaurants:
    print("something went wrong")
    return False;

  return restaurants

def getSingle(id):
  singleRest = restaurantDB.getSingle(id).fetchone()
  if not singleRest:
    return False
  
  return singleRest

def createRestaurant(name, description,address, 
                     mondayOpen,mondayClose,
                     tuesdayOpen,tuesdayClose,
                     wednesdayOpen, wednesdayClose,
                     thursdayOpen, thursdayClose,
                     fridayOpen, fridayClose,
                     saturdayOpen, saturdayClose,
                     sundayOpen, sundayClose,
                     genret):

  result = restaurantDB.createRestaurant(name, description,address).fetchone()
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
    

def checkNone(time):
  if time == "":
    return None
  
  return time
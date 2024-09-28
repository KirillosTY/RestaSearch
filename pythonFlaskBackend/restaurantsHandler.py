import os
import restaurantDB 
from flask import abort, request, session
import secrets


def getAll():
  restaurants = restaurantDB.getRestaurants().fetchall() 
  print(restaurants, 'here')

  if not restaurants:
    print("something went wrong")
    return False;

  return restaurants


def getFavourites(id):
  restaurants = restaurantDB.getFavouriteRestaurants(id).fetchall() 
  print(restaurants, 'here Favorites')

  if not restaurants:
    print("something went wrong")
    return False;

  return restaurants
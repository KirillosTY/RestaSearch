from random import randint
from db import db
from sqlalchemy.sql import text


def getRestaurants():
  sql = text("""
    SELECT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gpsLocation,
      r.added,
      rh.monday,
      rh.tuesday,
      rh.wednesday,
      rh.thursday,
      rh.friday,
      rh.saturday,
      rh.sunday
    FROM
      restaurant r
    LEFT JOIN
      restaurant_hours rh
    ON
      r.id = rh.restaurant_id;
    
    
                    
                """)
  return db.session.execute(sql)


def getFavouriteRestaurants(id):
  sql = text("""
    SELECT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gpsLocation,
      r.added,
      rh.monday,
      rh.tuesday,
      rh.wednesday,
      rh.thursday,
      rh.friday,
      rh.saturday,
      rh.sunday
    FROM
      restaurant r
     LEFT JOIN
      restaurant_hours rh
    ON
      r.id = rh.restaurant_id;
    
    
                    
                """)

  
  return db.session.execute(sql, {"id":id})
  #
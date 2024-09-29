from random import randint
from db import db
from sqlalchemy.sql import text


def getRestaurants():
  sql = text("""
    SELECT DISTINCT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gpsLocation,
      r.added,
      rh.mondayopen,
      rh.tuesdayopen,
      rh.wednesdayopen,
      rh.thursdayopen,
      rh.fridayopen,
      rh.saturdayopen,
      rh.sundayopen,
      rh.mondayclose,
      rh.tuesdayclose,
      rh.wednesdayclose,
      rh.thursdayclose,
      rh.fridayclose,
      rh.saturdayclose,
      rh.sundayclose
    FROM
      restaurant r
    LEFT JOIN
      restaurant_hours rh
    ON
      r.id = rh.restaurant_id
    ORDER BY 
      r.added
    
    
                    
                """)
  return db.session.execute(sql)


def getFavouriteRestaurants(id):
  sql = text("""
    SELECT DISTINCT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gpsLocation,
      r.added,
      rh.mondayopen,
      rh.tuesdayopen,
      rh.wednesdayopen,
      rh.thursdayopen,
      rh.fridayopen,
      rh.saturdayopen,
      rh.sundayopen,
      rh.mondayclose,
      rh.tuesdayclose,
      rh.wednesdayclose,
      rh.thursdayclose,
      rh.fridayclose,
      rh.saturdayclose,
      rh.sundayclose
    FROM
      restaurant r
     left JOIN
      restaurant_hours rh
    ON
      r.id = rh.restaurant_id
    ORDER BY 
    r.added
                    
                """)

  
  return db.session.execute(sql, {"id":id})
  #

def getSingle(id):
  sql = text("""
    SELECT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gpsLocation,
      r.added,
      rh.mondayopen,
      rh.tuesdayopen,
      rh.wednesdayopen,
      rh.thursdayopen,
      rh.fridayopen,
      rh.saturdayopen,
      rh.sundayopen,
      rh.mondayclose,
      rh.tuesdayclose,
      rh.wednesdayclose,
      rh.thursdayclose,
      rh.fridayclose,
      rh.saturdayclose,
      rh.sundayclose
    FROM
      restaurant r
      left JOIN
      restaurant_hours rh
    ON
      r.id = rh.restaurant_id
    
    WHERE r.id=:id
                    
    """)


  return db.session.execute(sql, {"id":id})
    #

def createRestaurant(name, description,address):
  sql = text("""
  INSERT INTO RESTAURANT
  (name, description, address)
  VALUES 
  (:name, :description, :address)
  RETURNING id;
  """)
  result = db.session.execute(sql,{"name":name,"address":address, "description":description})
  db.session.commit()
  
  

  return result


def create_restaurant(name, description, address):
    sql = text("""
        INSERT INTO RESTAURANT (name, description, address)
        VALUES (:name, :description, :address)
        RETURNING *;
    """)
    
    result = db.session.execute(sql, {"name": name, "description": description, "address": address})
    db.session.commit()
    return result.fetchone()  


def create_hours(restaurant_id
                 ,mondayOpen,mondayClose,
                  tuesdayOpen,tuesdayClose,
                  wednesdayOpen, wednesdayClose,
                  thursdayOpen, thursdayClose,
                  fridayOpen, fridayClose,
                  saturdayOpen, saturdayClose,
                  sundayOpen, sundayClose):

    sql = text("""
    INSERT INTO restaurant_hours
    (restaurant_id,
    mondayOpen,mondayClose,
    tuesdayOpen,tuesdayClose,
    wednesdayOpen, wednesdayClose,
    thursdayOpen, thursdayClose,
    fridayOpen, fridayClose,
    saturdayOpen, saturdayClose,
    sundayOpen, sundayClose)  
    VALUES 
    (:id,
    :mondayOpen,:mondayClose,
    :tuesdayOpen,:tuesdayClose,
    :wednesdayOpen, :wednesdayClose,
    :thursdayOpen, :thursdayClose,
    :fridayOpen, :fridayClose,
    :saturdayOpen, :saturdayClose,
    :sundayOpen, :sundayClose)
    RETURNING *;
    """)
    result = db.session.execute(sql,
      {
        "id":restaurant_id,
        "mondayOpen": mondayOpen,
        "mondayClose": mondayClose,
        "tuesdayOpen": tuesdayOpen,
        "tuesdayClose": tuesdayClose,
        "wednesdayOpen": wednesdayOpen,
        "wednesdayClose": wednesdayClose,
        "thursdayOpen": thursdayOpen,
        "thursdayClose": thursdayClose,
        "fridayOpen": fridayOpen,
        "fridayClose": fridayClose,
        "saturdayOpen": saturdayOpen,
        "saturdayClose": saturdayClose,
        "sundayOpen": sundayOpen,
        "sundayClose": sundayClose
      }
    )
    db.session.commit()
    return result.fetchone()
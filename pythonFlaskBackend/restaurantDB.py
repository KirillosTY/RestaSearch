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
      r.added
    FROM
      restaurant r
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
      r.added
    FROM
      restaurant r
     JOIN 
       favoriteRestaurants fr
    ON
      r.id = fr.restaurant_id
    WHERE 
    fr.user_id=:id
     ORDER BY 
    r.added
                    
                """)

  
  return db.session.execute(sql, {"id":id})
  #

def get_all_requests():
  sql = text("""
    SELECT DISTINCT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gpsLocation,
      r.requested,
      us.username
    FROM
      restaurant_tobe_accepted r
    LEFT JOIN
      users us
    ON
      us.id = r.user_id
        
    ORDER BY 
      r.requested
    
    
                    
      """)
    
  return db.session.execute(sql)

   

def check_favourite(user_id,restaurant_id):
  sql = text("""
    SELECT
      added
    FROM
       favoriteRestaurants fr
    WHERE 
    fr.user_id=:user_id AND fr.restaurant_id=:restaurant_id
    
                    
                """)

  
  return db.session.execute(sql, {"user_id":user_id,"restaurant_id":restaurant_id})
  
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

  
def get_single_request(id):

    sql = text("""
      SELECT
        r.id,
        r.name,
        r.address,
        r.description,
        r.gpsLocation,
        r.requested,
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
        restaurant_tobe_accepted r
        left JOIN
        restaurant_hours rh

      ON
        r.id = rh.restaurant_id
      
      WHERE r.id=:id
                      
      """)


    return db.session.execute(sql, {"id":id})
    #


def getReviews(restaurant_id):
  sql = text("""
    SELECT
      us.id,
      us.username,
      r.rating,
      r.comment,
      r.added
    FROM
      reviews r
      left JOIN
      users us
    ON
      r.user_id = us.id
    
    WHERE r.restaurant_id=:restaurant_id
                    
    """)


  return db.session.execute(sql, {"restaurant_id":restaurant_id})
    #

def get_user_reviews(user_id):
  sql = text("""
    SELECT
      us.id,
      us.username,
      re.name,
      r.rating,
      r.comment,
      r.added
    FROM
      reviews r
      left JOIN
      users us
    ON
      r.user_id = us.id
    LEFT JOIN 
      restaurant re
    ON
      r.restaurant_id = re.id
    
    WHERE us.id=:user_id
    ORDER BY 
      added

    LIMIT 5    
    """)


  return db.session.execute(sql, {"user_id":user_id})
    #



def find_restaurant(search_text):
  sql = text("""
    SELECT DISTINCT
      id,
      name,
      address,
      description,
      gpsLocation,
      added
    FROM
      restaurant
    WHERE 
      name ILIKE '%' || :search_text || '%' 
    OR
      description ILIKE '%' || :search_text || '%'
    ORDER BY 
      added          
    """)
   
  result = db.session.execute(sql, {"search_text":search_text})
  return result


def createRestaurant(name, description,address):
  sql = text("""
  INSERT INTO RESTAURANT
  (name, description, address, added)
  VALUES 
  (:name, :description, :address, NOW())
  RETURNING id;
  """)
  result = db.session.execute(sql,{"name":name,"address":address, "description":description})
  db.session.commit()
  
  

  return result

def create_restaurant_request(name, description,address):
  sql = text("""
  INSERT INTO restaurant_tobe_accepted
  (name, description, address, requested)
  VALUES 
  (:name, :description, :address, NOW())
  RETURNING id;
  """)
  result = db.session.execute(sql,{"name":name,"address":address, "description":description})
  db.session.commit()
  
  

  return result

def create_review(user_id,restaurant_id, rating,comment):
  sql = text("""
    INSERT INTO reviews
    (user_id, restaurant_id, rating, comment, added)
    VALUES 
    (:user_id, :restaurant_id,:rating,:comment, NOW())
    RETURNING *;
    """)
  result = db.session.execute(sql, {"user_id":user_id, "restaurant_id":restaurant_id, "rating": rating, "comment":comment})
  db.session.commit()
  return result;
  

def create_favourite(user_id,restaurant_id):
  sql = text("""
    INSERT INTO favoriteRestaurants
    (user_id, restaurant_id, added)
    VALUES 
    (:user_id, :restaurant_id, NOW())
    RETURNING True;
    """)
  result = db.session.execute(sql, {"user_id":user_id, "restaurant_id":restaurant_id,})
  db.session.commit()
  return result;


def update_restaurant(id,name, description, address):
    sql = text("""
        UPDATE RESTAURANT 
        SET name=:name, description=:description, address=:address
        WHERE id=:id
        RETURNING *;
    """)
    
    result = db.session.execute(sql, {"id":id,"name": name, "description": description, "address": address})
    db.session.commit()
    return result  

def update_review(user_id,restaurant_id, rating,comment):
    sql = text("""
        UPDATE reviews 
        SET user_id=:user_id, restaurant_id=:restaurant_id, rating=:rating, comment=:comment, added=NOW()
        WHERE user_id=:user_id AND restaurant_id=:restaurant_id
        RETURNING *;
    """)
    
    result = db.session.execute(sql, {"user_id":user_id, "restaurant_id":restaurant_id, "rating": rating, "comment":comment})
    db.session.commit()
    return result  



def create_hours(restaurant_id
                 ,mondayOpen,mondayClose,
                  tuesdayOpen,tuesdayClose,
                  wednesdayOpen, wednesdayClose,
                  thursdayOpen, thursdayClose,
                  fridayOpen, fridayClose,
                  saturdayOpen, saturdayClose,
                  sundayOpen, sundayClose):

    sql = text("""
    UPDATE restaurant_hours
SET 
    mondayOpen = :mondayOpen,
    mondayClose = :mondayClose,
    tuesdayOpen = :tuesdayOpen,
    tuesdayClose = :tuesdayClose,
    wednesdayOpen = :wednesdayOpen,
    wednesdayClose = :wednesdayClose,
    thursdayOpen = :thursdayOpen,
    thursdayClose = :thursdayClose,
    fridayOpen = :fridayOpen,
    fridayClose = :fridayClose,
    saturdayOpen = :saturdayOpen,
    saturdayClose = :saturdayClose,
    sundayOpen = :sundayOpen,
    sundayClose = :sundayClose
WHERE restaurant_id = :id
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



def create_request_hours(restaurant_id
                 ,mondayOpen,mondayClose,
                  tuesdayOpen,tuesdayClose,
                  wednesdayOpen, wednesdayClose,
                  thursdayOpen, thursdayClose,
                  fridayOpen, fridayClose,
                  saturdayOpen, saturdayClose,
                  sundayOpen, sundayClose):

    sql = text("""
    UPDATE restaurant_request_hours
SET 
    mondayOpen = :mondayOpen,
    mondayClose = :mondayClose,
    tuesdayOpen = :tuesdayOpen,
    tuesdayClose = :tuesdayClose,
    wednesdayOpen = :wednesdayOpen,
    wednesdayClose = :wednesdayClose,
    thursdayOpen = :thursdayOpen,
    thursdayClose = :thursdayClose,
    fridayOpen = :fridayOpen,
    fridayClose = :fridayClose,
    saturdayOpen = :saturdayOpen,
    saturdayClose = :saturdayClose,
    sundayOpen = :sundayOpen,
    sundayClose = :sundayClose
WHERE restaurant_id = :id
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

def update_hours(restaurant_id
                 ,mondayOpen,mondayClose,
                  tuesdayOpen,tuesdayClose,
                  wednesdayOpen, wednesdayClose,
                  thursdayOpen, thursdayClose,
                  fridayOpen, fridayClose,
                  saturdayOpen, saturdayClose,
                  sundayOpen, sundayClose):

    sql = text("""
    UPDATE restaurant_hours
    SET 
      mondayOpen = :mondayOpen,
      mondayClose = :mondayClose,
      tuesdayOpen = :tuesdayOpen,
      tuesdayClose = :tuesdayClose,
      wednesdayOpen = :wednesdayOpen,
      wednesdayClose = :wednesdayClose,
      thursdayOpen = :thursdayOpen,
      thursdayClose = :thursdayClose,
      fridayOpen = :fridayOpen,
      fridayClose = :fridayClose,
      saturdayOpen = :saturdayOpen,
      saturdayClose = :saturdayClose,
      sundayOpen = :sundayOpen,
      sundayClose = :sundayClose
    WHERE restaurant_id = :id
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


def delete_restaurant(id):
   
  sql = text("""
    DELETE FROM restaurant WHERE id=:id RETURNING id,name
              """)
   
  result = db.session.execute(sql,{"id":id})
  db.session.commit()

  return result;


def delete_restaurant_request(id):
  print(id,'this is the id?!')
  sql = text("""
    DELETE FROM restaurant_tobe_accepted WHERE id=:id RETURNING id,name
              """)
   
  result = db.session.execute(sql,{"id":id})
  db.session.commit()
  return result;


def delete_review(user_id, restaurant_id):
   
  sql = text("""
    DELETE FROM reviews WHERE user_id=:user_id and restaurant_id=:restaurant_id  RETURNING *
              """)
   
  result = db.session.execute(sql,{"user_id":user_id, "restaurant_id":restaurant_id})
  db.session.commit()

  return result;

def delete_favourited(user_id, restaurant_id):
   
  sql = text("""
    DELETE FROM favoriteRestaurants WHERE user_id=:user_id and restaurant_id=:restaurant_id RETURNING *
              """)
   
  result = db.session.execute(sql,{"user_id":user_id, "restaurant_id":restaurant_id})
  db.session.commit()

  return result;
from random import randint
from db import db
from sqlalchemy.sql import text


def get_restaurants():
    sql = text("""
    SELECT DISTINCT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gps_location,
      r.added
    FROM
      restaurant r
    ORDER BY
      r.added



                """)
    return db.session.execute(sql)


def get_favourite_restaurants(user_id):
    sql = text("""
    SELECT DISTINCT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gps_location,
      r.added
    FROM
      restaurant r
     JOIN
       favourite_restaurants fr
    ON
      r.id = fr.restaurant_id
    WHERE
    fr.user_id=:id
     ORDER BY
    r.added

                """)

    return db.session.execute(sql, {"id": user_id})
    #


def get_all_requests():
    sql = text("""
    SELECT DISTINCT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gps_location,
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


def check_favourite(user_id, restaurant_id):
    sql = text("""
    SELECT
      added
    FROM
       favourite_restaurants fr
    WHERE
    fr.user_id=:user_id AND fr.restaurant_id=:restaurant_id


                """)

    return db.session.execute(
        sql, {"user_id": user_id, "restaurant_id": restaurant_id})


def get_single(restaurant_id):
    sql = text("""
    SELECT
      r.id,
      r.name,
      r.address,
      r.description,
      r.gps_location,
      r.added,
      rh.monday_open,
      rh.tuesday_open,
      rh.wednesday_open,
      rh.thursday_open,
      rh.friday_open,
      rh.saturday_open,
      rh.sunday_open,
      rh.monday_close,
      rh.tuesday_close,
      rh.wednesday_close,
      rh.thursday_close,
      rh.friday_close,
      rh.saturday_close,
      rh.sunday_close
    FROM
      restaurant r
      left JOIN
      restaurant_hours rh

    ON
      r.id = rh.restaurant_id

    WHERE r.id=:id

    """)
    return db.session.execute(sql, {"id": restaurant_id})


def get_single_request(restaurant_id):

    sql = text("""
      SELECT
        r.id,
        r.name,
        r.address,
        r.description,
        r.gps_location,
        r.requested,
        rh.monday_open,
        rh.tuesday_open,
        rh.wednesday_open,
        rh.thursday_open,
        rh.friday_open,
        rh.saturday_open,
        rh.sunday_open,
        rh.monday_close,
        rh.tuesday_close,
        rh.wednesday_close,
        rh.thursday_close,
        rh.friday_close,
        rh.saturday_close,
        rh.sunday_close
      FROM
        restaurant_tobe_accepted r
        left JOIN
        restaurant_hours rh

      ON
        r.id = rh.restaurant_id

      WHERE r.id=:id

      """)

    return db.session.execute(sql, {"id": restaurant_id})
    #


def get_reviews(restaurant_id):
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

    return db.session.execute(sql, {"restaurant_id": restaurant_id})
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

    return db.session.execute(sql, {"user_id": user_id})
    #


def check_review(user_id, restaurant_id):
    sql = text("""
    SELECT
      user_id,
      restaurant_id,
      rating,
      comment

    FROM
      reviews

    WHERE
      restaurant_id=:restaurant_id AND user_id =:user_id

    """)

    return db.session.execute(
        sql, {"user_id": user_id, "restaurant_id": restaurant_id})
    #


def check_hours_exist(restaurant_id):
    sql = text("""
    SELECT
      restaurant_id
    FROM
      restaurant_hours

    WHERE
      restaurant_id=:restaurant_id 

    """)

    return db.session.execute(
        sql, {"restaurant_id": restaurant_id})
    #


def find_restaurant(search_text):
    sql = text("""
    SELECT DISTINCT
      id,
      name,
      address,
      description,
      gps_location,
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

    result = db.session.execute(sql, {"search_text": search_text})
    return result


def create_restaurant(name, description, address):
    sql = text("""
  INSERT INTO RESTAURANT
  (name, description, address, added)
  VALUES
  (:name, :description, :address, NOW())
  RETURNING id;
  """)
    result = db.session.execute(
        sql, {"name": name, "address": address, "description": description})
    db.session.commit()

    return result


def create_restaurant_request(name, description, address):
    sql = text("""
  INSERT INTO restaurant_tobe_accepted
  (name, description, address, requested)
  VALUES
  (:name, :description, :address, NOW())
  RETURNING id;
  """)
    result = db.session.execute(
        sql, {"name": name, "address": address, "description": description})
    db.session.commit()

    return result


def create_review(user_id, restaurant_id, rating, comment):
    sql = text("""
    INSERT INTO reviews
    (user_id, restaurant_id, rating, comment, added)
    VALUES
    (:user_id, :restaurant_id,:rating,:comment, NOW())
    RETURNING *;
    """)
    result = db.session.execute(sql,
                                {"user_id": user_id,
                                 "restaurant_id": restaurant_id,
                                 "rating": rating,
                                 "comment": comment})
    db.session.commit()
    return result


def create_favourite(user_id, restaurant_id):
    sql = text("""
    INSERT INTO favourite_restaurants
    (user_id, restaurant_id, added)
    VALUES
    (:user_id, :restaurant_id, NOW())
    RETURNING True;
    """)
    result = db.session.execute(
        sql, {"user_id": user_id, "restaurant_id": restaurant_id, })
    db.session.commit()
    return result


def update_restaurant(restaurant_id, name, description, address):
    sql = text("""
        UPDATE RESTAURANT
        SET name=:name, description=:description, address=:address
        WHERE id=:id
        RETURNING *;
    """)

    result = db.session.execute(
        sql, {"id": restaurant_id, "name": name, "description": description, "address": address})
    db.session.commit()
    return result


def update_review(user_id, restaurant_id, rating, comment):
    sql = text("""
        UPDATE reviews
        SET user_id=:user_id, restaurant_id=:restaurant_id, rating=:rating, comment=:comment, added=NOW()
        WHERE user_id=:user_id AND restaurant_id=:restaurant_id
        RETURNING *;
    """)

    result = db.session.execute(sql,
                                {"user_id": user_id,
                                 "restaurant_id": restaurant_id,
                                 "rating": rating,
                                 "comment": comment})
    db.session.commit()
    return result


def create_hours(restaurant_id
                 ,monday_open,monday_close,
                  tuesday_open,tuesday_close,
                  wednesday_open, wednesday_close,
                  thursday_open, thursday_close,
                  friday_open, friday_close,
                  saturday_open, saturday_close,
                  sunday_open, sunday_close):
    sql = text("""
    INSERT INTO restaurant_hours
    (restaurant_id,
    monday_open,monday_close,
    tuesday_open,tuesday_close,
    wednesday_open, wednesday_close,
    thursday_open, thursday_close,
    friday_open, friday_close,
    saturday_open, saturday_close,
    sunday_open, sunday_close)  
    VALUES 
    (:id,
    :monday_open,:monday_close,
    :tuesday_open,:tuesday_close,
    :wednesday_open, :wednesday_close,
    :thursday_open, :thursday_close,
    :friday_open, :friday_close,
    :saturday_open, :saturday_close,
    :sunday_open, :sunday_close)
    RETURNING *;
    """)
    result = db.session.execute(sql,
      {
        "id":restaurant_id,
        "monday_open": monday_open,
        "monday_close": monday_close,
        "tuesday_open": tuesday_open,
        "tuesday_close": tuesday_close,
        "wednesday_open": wednesday_open,
        "wednesday_close": wednesday_close,
        "thursday_open": thursday_open,
        "thursday_close": thursday_close,
        "friday_open": friday_open,
        "friday_close": friday_close,
        "saturday_open": saturday_open,
        "saturday_close": saturday_close,
        "sunday_open": sunday_open,
        "sunday_close": sunday_close
      }
    )
    db.session.commit()
    return result.fetchone()


def create_request_hours(restaurant_id
                 ,monday_open,monday_close,
                  tuesday_open,tuesday_close,
                  wednesday_open, wednesday_close,
                  thursday_open, thursday_close,
                  friday_open, friday_close,
                  saturday_open, saturday_close,
                  sunday_open, sunday_close):
    sql = text("""
    INSERT INTO restaurant_request_hours
(restaurant_id,
    monday_open,monday_close,
    tuesday_open,tuesday_close,
    wednesday_open, wednesday_close,
    thursday_open, thursday_close,
    friday_open, friday_close,
    saturday_open, saturday_close,
    sunday_open, sunday_close)  
    VALUES 
    (:id,
    :monday_open,:monday_close,
    :tuesday_open,:tuesday_close,
    :wednesday_open, :wednesday_close,
    :thursday_open, :thursday_close,
    :friday_open, :friday_close,
    :saturday_open, :saturday_close,
    :sunday_open, :sunday_close)
    RETURNING *;

    """)
    result = db.session.execute(sql,
      {
        "id":restaurant_id,
        "monday_open": monday_open,
        "monday_close": monday_close,
        "tuesday_open": tuesday_open,
        "tuesday_close": tuesday_close,
        "wednesday_open": wednesday_open,
        "wednesday_close": wednesday_close,
        "thursday_open": thursday_open,
        "thursday_close": thursday_close,
        "friday_open": friday_open,
        "friday_close": friday_close,
        "saturday_open": saturday_open,
        "saturday_close": saturday_close,
        "sunday_open": sunday_open,
        "sunday_close": sunday_close
      }
    )
    db.session.commit()
    return result.fetchone()


def update_hours(restaurant_id, monday_open, monday_close,
                 tuesday_open, tuesday_close,
                 wednesday_open, wednesday_close,
                 thursday_open, thursday_close,
                 friday_open, friday_close,
                 saturday_open, saturday_close,
                 sunday_open, sunday_close):

    sql = text("""
    UPDATE restaurant_hours
    SET
      monday_open = :monday_open,
      monday_close = :monday_close,
      tuesday_open = :tuesday_open,
      tuesday_close = :tuesday_close,
      wednesday_open = :wednesday_open,
      wednesday_close = :wednesday_close,
      thursday_open = :thursday_open,
      thursday_close = :thursday_close,
      friday_open = :friday_open,
      friday_close = :friday_close,
      saturday_open = :saturday_open,
      saturday_close = :saturday_close,
      sunday_open = :sunday_open,
      sunday_close = :sunday_close
    WHERE restaurant_id = :id
    RETURNING *;

    """)
    result = db.session.execute(sql,
                                {
                                    "id": restaurant_id,
                                    "monday_open": monday_open,
                                    "monday_close": monday_close,
                                    "tuesday_open": tuesday_open,
                                    "tuesday_close": tuesday_close,
                                    "wednesday_open": wednesday_open,
                                    "wednesday_close": wednesday_close,
                                    "thursday_open": thursday_open,
                                    "thursday_close": thursday_close,
                                    "friday_open": friday_open,
                                    "friday_close": friday_close,
                                    "saturday_open": saturday_open,
                                    "saturday_close": saturday_close,
                                    "sunday_open": sunday_open,
                                    "sunday_close": sunday_close
                                }
                                )
    db.session.commit()
    return result.fetchone()


def delete_restaurant(restaurant_id):

    sql = text("""
    DELETE FROM restaurant WHERE id=:id RETURNING id,name
              """)

    result = db.session.execute(sql, {"id": restaurant_id})
    db.session.commit()

    return result


def delete_restaurant_request(restaurant_id):
    print(restaurant_id, 'this is the id?!')
    sql = text("""
    DELETE FROM restaurant_tobe_accepted WHERE id=:id RETURNING id,name
              """)

    result = db.session.execute(sql, {"id": restaurant_id})
    db.session.commit()
    return result


def delete_review(user_id, restaurant_id):

    sql = text("""
    DELETE FROM reviews WHERE user_id=:user_id and restaurant_id=:restaurant_id  RETURNING *
              """)

    result = db.session.execute(
        sql, {"user_id": user_id, "restaurant_id": restaurant_id})
    db.session.commit()

    return result


def delete_favourited(user_id, restaurant_id):

    sql = text("""
    DELETE FROM favourite_restaurants WHERE user_id=:user_id and restaurant_id=:restaurant_id RETURNING *
              """)

    result = db.session.execute(
        sql, {"user_id": user_id, "restaurant_id": restaurant_id})
    db.session.commit()

    return result

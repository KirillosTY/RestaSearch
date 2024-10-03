import restaurant_db


def get_all():
    restaurants = restaurant_db.get_restaurants().fetchall()

    if not restaurants:
        print(restaurants, "something went wrong")
        return False

    return restaurants


def get_all_requests():
    restaurant_requests = restaurant_db.get_all_requests().fetchall()
    if not restaurant_requests:
        print(restaurant_requests, "something went wrong")
        return False

    return restaurant_requests


def get_favourites(restaurant_id):
    restaurants = restaurant_db.get_favourite_restaurants(restaurant_id).fetchall()
    if not restaurants:
        print(restaurants, "something went wrong")
        return False

    return restaurants


def check_favourite(user_id, restaurant_id):
    restaurants = restaurant_db.check_favourite(
        user_id, restaurant_id).fetchall()
    if not restaurants:
        print(restaurants, "something went wrong")
        return False

    return restaurants


def check_review(user_id, restaurant_id):
    review_left = restaurant_db.check_review(user_id,
                                             restaurant_id).fetchone()
    if not review_left:
        return False

    return review_left


def get_single(restaurant_id):
    single_rest = restaurant_db.get_single(restaurant_id).fetchone()
    single_rest_review = restaurant_db.get_reviews(restaurant_id).fetchall()

    if not single_rest:
        return False

    return [single_rest, single_rest_review]


def get_single_request(restaurant_id):
    singleRest = restaurant_db.get_single_request(restaurant_id).fetchone()

    if not singleRest:
        return False

    return singleRest


def get_reviews(restaurant_id):
    singleRestReview = restaurant_db.get_reviews(restaurant_id).fetchall()

    return singleRestReview


def get_user_reviews(user_id):
    singleRestReview = restaurant_db.get_user_reviews(user_id).fetchall()

    return singleRestReview


def find_restaurant(search_text):
    searched_restaurants = restaurant_db.find_restaurant(
        search_text).fetchall()
    return searched_restaurants


def create_restaurant(name, description, address,
                      monday_open, monday_close,
                      tuesday_open, tuesday_close,
                      wednesday_open, wednesday_close,
                      thursday_open, thursday_close,
                      friday_open, friday_close,
                      saturday_open, saturday_close,
                      sunday_open, sunday_close,
                      genret):

    result = restaurant_db.create_restaurant(
        name, description, address).fetchone()
    if result:

        hours = restaurant_db.create_hours(
            result[0],
            checkNone(monday_open),
            checkNone(monday_close),
            checkNone(tuesday_open),
            checkNone(tuesday_close),
            checkNone(wednesday_open),
            checkNone(wednesday_close),
            checkNone(thursday_open),
            checkNone(thursday_close),
            checkNone(friday_open),
            checkNone(friday_close),
            checkNone(saturday_open),
            checkNone(saturday_close),
            checkNone(sunday_open),
            checkNone(sunday_close))
        print(hours, 'tunnit')
    return result


def create_request(name, description, address,
                   monday_open, monday_close,
                   tuesday_open, tuesday_close,
                   wednesday_open, wednesday_close,
                   thursday_open, thursday_close,
                   friday_open, friday_close,
                   saturday_open, saturday_close,
                   sunday_open, sunday_close,
                   genret):

    result = restaurant_db.create_restaurant_request(
        name, description, address).fetchone()
    if result:

        hours = restaurant_db.create_request_hours(
            result[0],
            checkNone(monday_open),
            checkNone(monday_close),
            checkNone(tuesday_open),
            checkNone(tuesday_close),
            checkNone(wednesday_open),
            checkNone(wednesday_close),
            checkNone(thursday_open),
            checkNone(thursday_close),
            checkNone(friday_open),
            checkNone(friday_close),
            checkNone(saturday_open),
            checkNone(saturday_close),
            checkNone(sunday_open),
            checkNone(sunday_close))
        print(hours, 'tunnit')
    return result


def create_review(user_id, restaurant_id, rating, comment):
    result = restaurant_db.create_review(
        user_id, restaurant_id, rating, comment).fetchone()
    return result


def create_favourite(user_id, restaurant_id):
    favourited = restaurant_db.create_favourite(
        user_id, restaurant_id).fetchall()

    return favourited


def update_review(user_id, restaurant_id, rating, comment):
    result = restaurant_db.update_review(
        user_id, restaurant_id, rating, comment).fetchone()
    print(result)
    return result


def update_single(id, name, description, address,
                  monday_open, monday_close,
                  tuesday_open, tuesday_close,
                  wednesday_open, wednesday_close,
                  thursday_open, thursday_close,
                  friday_open, friday_close,
                  saturday_open, saturday_close,
                  sunday_open, sunday_close,
                  genret):

    restaurant_db.update_restaurant(id, name, description, address).fetchone()

    restaurant_db.update_hours(
        id,
        checkNone(monday_open),
        checkNone(monday_close),
        checkNone(tuesday_open),
        checkNone(tuesday_close),
        checkNone(wednesday_open),
        checkNone(wednesday_close),
        checkNone(thursday_open),
        checkNone(thursday_close),
        checkNone(friday_open),
        checkNone(friday_close),
        checkNone(saturday_open),
        checkNone(saturday_close),
        checkNone(sunday_open),
        checkNone(sunday_close))

    return get_single(id)


def delete_restaurant(restaurant_id):
    result = restaurant_db.delete_restaurant(restaurant_id).fetchone()
    return result


def delete_request(restaurant_id):
    result = restaurant_db.delete_restaurant_request(restaurant_id).fetchone()
    print('deleting went to shit', result)
    return result


def delete_review(user_id, restaurant_id):
    result = restaurant_db.delete_review(user_id, restaurant_id).fetchone()
    return result


def remove_favourite(user_id, restaurant_id):
    removed = restaurant_db.delete_favourited(
        user_id, restaurant_id).fetchone()

    return removed


def checkNone(time):
    if time == "":
        return None

    return time

from app import app
from flask import render_template, request, redirect, session, abort
import users
import restaurants
from inputCheck import username_check, password_check
import re


@app.route('/')
def default():
    check_access_before(False)
    user = session.get("user") 
    print(user)
    favourite_rest_list = restaurants.get_favourites(session.get("user_id"))
    reviews = restaurants.get_user_reviews(session.get("user_id"))
    if not favourite_rest_list:
        # Add error hadling for both
        favourite_rest_list = []
    if not user:
        return redirect("/login")

    return render_template(
        "start.html",
        favourite_restaurants=favourite_rest_list,
        reviews=reviews)


@app.route('/login', methods=['GET', 'POST'])
def login():

    print(request.method)
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form["username"]
    password = request.form["password"]
    if not username_check(username):
        return render_template(
            "login.html",
            message="Käyttäjätunnuksen pitää olla 8-16 merkkiä")
    if not password_check(password):
        return render_template(
            "login.html",
            message="""Salasanan pitää olla ainakin 8 merkkiä
            sisältäen yhden pienen
            ja ison kirjaimen sekä numeron.
            Onnea elämään noilla salasanoilla <3.""")

    logging = users.login(username, password)
    if logging is None:
        return render_template(
            "login.html",
            message="Käyttäjätunnusta ei löydy")
    if not logging:
        return render_template(
            "login.html",
            message="Salasana on väärin")

    return redirect("/")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    users.delete_session()
    return redirect("/login")


@app.route('/create', methods=['GET', 'POST'])
def create():

    csrf = session.get("csrf_token")

    if csrf is not None:
        if not session.get("is_admin"):
            abort(403)

    print(request.method)
    if request.method == 'GET':
        return render_template('create_user.html')

    username = request.form["username"]
    password = request.form["password"]
    password_repeat = request.form["password_repeat"]
    is_admin = request.form.get("admin", False)

    if not password_repeat == password:
        return render_template(
            "create_user.html",
            message="Salasanan pitää täsmätä")
    if not username_check(username):
        return render_template(
            "create_user.html",
            message="Käyttäjätunnuksen pitää olla 8-16 merkkiä")
    if not (password_check(password) and password_check(password_repeat)):
        print("käydään mitä vittua tapahttuu")
        return render_template(
            "create_user.html",
            message="""Salasanan pitää olla ainakin 8 merkkiä
            sisältäen yhden pienen
            ja ison kirjaimen sekä numeron.
            Onnea elämään noilla salasanoilla <3."""
        )
    created_user = users.create(username, password, is_admin)
    if not created_user:
        return render_template(
            "create_user.html",
            message="Käyttäjätunnus on jo käytössä")
    return redirect("/")


@app.route('/restaurants', methods=['GET', 'POST'])
def restaurant_lists():
    restaurants_found = restaurants.get_all()
    favourites_found = restaurants.get_favourites(session.get("user_id"))

    if not restaurants_found:
        restaurants_found = []
    if not favourites_found:
        favourites_found = []
    search_text = request.form.get('restaurant_query', False)
    if request.method == 'POST' and search_text:
        rest_found = restaurants.find_restaurant(search_text)
        print(rest_found, "käydääää")
        return render_template('restaurants.html',
                               restaurants=rest_found,
                               favourited_restaurants=favourites_found,
                               searched=True)

    elif request.method == 'GET' or search_text == '':
        return render_template('restaurants.html',
                               restaurants=restaurants_found,
                               favourited_restaurants=favourites_found,
                               searched=False)


@app.route('/restaurants/requests', methods=['GET', 'POST'])
def restaurant_requests():
    check_access_before(False)
    restaurants_found = restaurants.get_all_requests()
    if not restaurants_found:
        restaurants_found = []

    if request.method == 'GET':
        return render_template('restaurant_requested.html',
                               restaurants=restaurants_found)


@app.route('/restaurants/<int:restaurant_id>', methods=['GET', 'POST'])
def single_restaurant(restaurant_id):
    check_access_before(False)
    rest_and_reviews = restaurants.get_single(restaurant_id)
    single_rest = rest_and_reviews[0]
    single_rest_reviews = rest_and_reviews[1]
    if single_rest is None:
        single_rest = []
        rest_and_reviews = []

    user_id = session.get('user_id')
    restaurant_favourited = restaurants.check_favourite(
        user_id, single_rest[0])

    left_review = restaurants.check_review(user_id, single_rest[0])

    if request.method == 'GET':
        return render_template(
            'single_restaurant.html',
            restaurant=single_rest,
            reviews=single_rest_reviews,
            reviewed=left_review,
            favourited=restaurant_favourited)

    users.check_csrf()
    form_buttons = request.form.to_dict()
    print(form_buttons.keys())
    for key in form_buttons.keys():
        if key in ['edit', 'remove', 'favourite', 'remove_favourite']:
            return handle_admin_buttons(form_buttons, restaurant_id)

        if key in ['review', 'review_update', 'review_delete']:
            print("ei silti käydä?!")
            return handle_review_buttons(
                form_buttons, restaurant_id, single_rest)

    return render_template(
        'single_restaurant.html',
        restaurant=single_rest,
        reviews=single_rest_reviews,
        message="Jotain meni pieleen, yritä myöhemmin uudelleen")


def handle_admin_buttons(admin_buttons, restaurant_id):

    if admin_buttons.get('edit', False) == 'edit':
        return redirect("/edit/restaurants/" + str(restaurant_id))

    if admin_buttons.get('remove', False) == 'remove':
        result = restaurants.delete_restaurant(restaurant_id)

        if result:
            return render_template(
                'single_restaurant.html',
                restaurant=[],
                reviews=[],
                success_message="Ravintola " +
                result[1] +
                " on nyt poistettu")

    if admin_buttons.get('favourite', False) == 'favourite':
        user_id = session.get('user_id')
        restaurants.create_favourite(user_id, restaurant_id)
        # succesmessage
        return redirect("/restaurants/" + str(restaurant_id))

    if admin_buttons.get('remove_favourite', False) == 'remove_favourite':
        user_id = session.get('user_id')
        restaurants.remove_favourite(user_id, restaurant_id)
        # succesmessage
        return redirect("/restaurants/" + str(restaurant_id))
    return False


def handle_review_buttons(review_buttons, restaurant_id, single_rest):

    if review_buttons.get('review', False) == 'review':
        rating = request.form['rating']
        comment = request.form['comment']
        user_id = session.get('user_id')
        restaurants.create_review(user_id, restaurant_id, rating, comment)
        return redirect("/restaurants/" + str(restaurant_id))

    elif review_buttons.get('review_update', False) == 'review_update':
        rating = request.form['rating']
        comment = request.form['comment']
        user_id = session.get('user_id')
        restaurants.update_review(user_id, restaurant_id, rating, comment)
        return redirect("/restaurants/" + str(restaurant_id))

    elif review_buttons.get('review_delete', False) == 'review_delete':
        user_id = session.get('user_id')
        result = restaurants.delete_review(user_id, restaurant_id)
        single_rest_reviews = restaurants.get_reviews(restaurant_id)
        if result:
            return render_template(
                'single_restaurant.html',
                restaurant=single_rest,
                reviews=[],
                success_message="Arvostelu on nyt poistettu")

        return render_template(
            'single_restaurant.html',
            restaurant=single_rest,
            reviews=single_rest_reviews,
            message="Jotain meni pieleen, yritä myöhemmin uudelleen")
    return False


@app.route('/edit/restaurants/<int:restaurant_id>', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    check_access_before(True)

    rest_and_reviews = restaurants.get_single(restaurant_id)
    if request.method == 'GET':
        return render_template(
            'single_edit_rest.html',
            id=id,
            restaurant=rest_and_reviews[0])

    users.check_csrf()
    name = request.form["name"]
    description = request.form["description"]
    address = request.form.get("address", None)
    monday_open = request.form.get("monday_open", None)
    tuesday_open = request.form.get("tuesday_open", None)

    wednesday_open = request.form.get("wednesday_open", None)
    thursday_open = request.form.get("thursday_open", None)
    friday_open = request.form.get("friday_open", None)
    saturday_open = request.form.get("saturday_open", None)
    sunday_open = request.form.get("sunday_open", None)

    monday_close = request.form.get("monday_close", None)
    tuesday_close = request.form.get("tuesday_close", None)
    wednesday_close = request.form.get("wednesday_close", None)
    thursday_close = request.form.get("thursday_close", None)
    friday_close = request.form.get("friday_close", None)
    saturday_close = request.form.get("saturday_close", None)
    sunday_close = request.form.get("sunday_close", None)

    genre = request.form.get("genre", None)

    restaurant_updated = restaurants.update_single(
        restaurant_id,
        name,
        description,
        address,
        monday_open,
        monday_close,
        tuesday_open,
        tuesday_close,
        wednesday_open,
        wednesday_close,
        thursday_open,
        thursday_close,
        friday_open,
        friday_close,
        saturday_open,
        saturday_close,
        sunday_open,
        sunday_close,
        genre)

    return render_template('single_edit_rest.html', id=id,
                           restaurant=restaurant_updated[0],
                           success_message="Tiedot tallentuneet")


@app.route('/restaurants/<int:restaurant_id>/request', methods=['GET', 'POST'])
def accept_restaurant(restaurant_id):

    check_access_before(True)

    rest = restaurants.get_single_request(restaurant_id)
    if request.method == 'GET':
        return render_template('single_request.html', id=id, restaurant=rest)

    users.check_csrf()
    name = request.form["name"]
    description = request.form["description"]
    address = request.form.get("address", None)
    monday_open = request.form.get("monday_open", None)
    tuesday_open = request.form.get("tuesday_open", None)

    wednesday_open = request.form.get("wednesday_open", None)
    thursday_open = request.form.get("thursday_open", None)
    friday_open = request.form.get("friday_open", None)
    saturday_open = request.form.get("saturday_open", None)
    sunday_open = request.form.get("sunday_open", None)

    monday_close = request.form.get("monday_close", None)
    tuesday_close = request.form.get("tuesday_close", None)
    wednesday_close = request.form.get("wednesday_close", None)
    thursday_close = request.form.get("thursday_close", None)
    friday_close = request.form.get("friday_close", None)
    saturday_close = request.form.get("saturday_close", None)
    sunday_close = request.form.get("sunday_close", None)

    genre = request.form.get("genre", None)

    restaurant_accepted = restaurants.create_restaurant(
        name,
        description,
        address,
        monday_open,
        monday_close,
        tuesday_open,
        tuesday_close,
        wednesday_open,
        wednesday_close,
        thursday_open,
        thursday_close,
        friday_open,
        friday_close,
        saturday_open,
        saturday_close,
        sunday_open,
        sunday_close,
        genre)
    print(restaurant_accepted, 'seconds')

    if restaurant_accepted:
        restaurants.delete_request(restaurant_id)

    return redirect('/restaurants/' + str(restaurant_accepted[0]))


@app.route('/create/restaurant', methods=['GET', 'POST'])
def create_restaurant():
    check_access_before(False)
    is_admin = session.get("is_admin")
    if request.method == 'GET':
        return render_template('create_restaurant.html')
    users.check_csrf()

    name = request.form["name"]
    description = request.form["description"]
    address = request.form.get("address", None)
    monday_open = request.form.get("monday_open", None)
    tuesday_open = request.form.get("tuesday_open", None)

    wednesday_open = request.form.get("wednesday_open", None)
    thursday_open = request.form.get("thursday_open", None)
    friday_open = request.form.get("friday_open", None)
    saturday_open = request.form.get("saturday_open", None)
    sunday_open = request.form.get("sunday_open", None)

    monday_close = request.form.get("monday_close", None)
    tuesday_close = request.form.get("tuesday_close", None)
    wednesday_close = request.form.get("wednesday_close", None)
    thursday_close = request.form.get("thursday_close", None)
    friday_close = request.form.get("friday_close", None)
    saturday_close = request.form.get("saturday_close", None)
    sunday_close = request.form.get("sunday_close", None)

    genre = request.form.get("genre", None)
    if is_admin:
        restaurant = restaurants.create_restaurant(
            name,
            description,
            address,
            monday_open,
            monday_close,
            tuesday_open,
            tuesday_close,
            wednesday_open,
            wednesday_close,
            thursday_open,
            thursday_close,
            friday_open,
            friday_close,
            saturday_open,
            saturday_close,
            sunday_open,
            sunday_close,
            genre)
    else:
        restaurant = restaurants.create_request(
            name,
            description,
            address,
            monday_open,
            monday_close,
            tuesday_open,
            tuesday_close,
            wednesday_open,
            wednesday_close,
            thursday_open,
            thursday_close,
            friday_open,
            friday_close,
            saturday_open,
            saturday_close,
            sunday_open,
            sunday_close,
            genre)
        return redirect("/restaurants/requests")

    

    return redirect("/restaurants/" + str(restaurant[0]))


def check_access_before(admin_required):
    if not session.get('csrf_token'):

        abort(403)
    if admin_required:
        if not session.get("is_admin"):
            abort(403)

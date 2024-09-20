
from flask import Flask,redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)

app.secret_key = getenv("SECRET")

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQL_AlCHEMY_DBURL")
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = getenv("SECRET")  # Change this to a strong secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expiry time
jwt = JWTManager(app)

  

@app.route('/api/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        
        sql = text("SELECT id,username,password FROM users WHERE username=:username")

        result = db.session.execute(sql,{"username":username})

        user = result.fetchone()
        print(generate_password_hash(password))
        print("Käydään täällä ennen checkiä",check_password_hash(user.password,password ))
        if (user and check_password_hash(user.password,password)):
            access_token = create_access_token(identity={'username': username})

            return jsonify({"access_token": access_token, "user": {"id": user.id, "username": username}})
        else:
            return jsonify({"message": "Invalid credentials", "status": "error"}), 401
    else:
        return jsonify({"message": "Request must be JSON"}), 400



@app.route('/restaurants')
def restaurants():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, latitude, longitude, comment, rating FROM restaurants')
    restaurants = cur.fetchall()
    cur.close()
    conn.close()

    # Convert data to JSON format
    restaurant_list = []
    for rest in restaurants:
        restaurant_list.append({
            'id': rest[0],
            'name': rest[1],
            'latitude': rest[2],
            'longitude': rest[3],
            'comment': rest[4],
            'rating': rest[5]
        })

    return jsonify(restaurant_list)

if __name__ == '__main__':
    app.run(debug=True)
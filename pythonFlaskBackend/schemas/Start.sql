CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN
);
CREATE TABLE restaurant (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    address TEXT,
    description TEXT NOT NULL,
    gps_location TEXT,
    user_id INTEGER REFERENCES users(id),
    added TIMESTAMP
);

CREATE TABLE reviews (
  restaurant_id INTEGER REFERENCES Restaurant(id) ON DELETE CASCADE,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  comment TEXT,
  rating INTEGER,
  added TIMESTAMP,
  CONSTRAINT unique_review UNIQUE (restaurant_id, user_id)
);


CREATE TABLE restaurant_type (
  restaurant_id INTEGER REFERENCES Restaurant(id) ON DELETE CASCADE UNIQUE,
  first_type varchar(16) NOT NULL,
  second_type varchar(16),
  third_type varchar(16),
  fourth_type varchar(16),
  fifth_type varchar(16)
);

CREATE TABLE favourite_restaurants (
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  restaurant_id INTEGER REFERENCES restaurant(id) ON DELETE CASCADE,
  added TIMESTAMP,
  CONSTRAINT unique_favourite UNIQUE (restaurant_id, user_id)
);


CREATE TABLE favorites (
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  user_friended_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  added TIMESTAMP,
  CONSTRAINT unique_friend UNIQUE (user_friended_id, user_id)
);


CREATE TABLE restaurant_hours (
  restaurant_id INTEGER PRIMARY KEY REFERENCES restaurant(id) ON DELETE CASCADE,
  monday_open TIME,
  tuesday_open TIME,
  wednesday_open TIME,
  thursday_open TIME,
  friday_open TIME,
  saturday_open TIME,
  sunday_open TIME,
  monday_close TIME,
  tuesday_close TIME,
  wednesday_close TIME,
  thursday_close TIME,
  friday_close TIME,
  saturday_close TIME,
  sunday_close TIME
);

CREATE TABLE restaurant_request_hours (
  restaurant_id INTEGER PRIMARY KEY REFERENCES restaurant_tobe_accepted(id) ON DELETE CASCADE,
  monday_open TIME,
  tuesday_open TIME,
  wednesday_open TIME,
  thursday_open TIME,
  friday_open TIME,
  saturday_open TIME,
  sunday_open TIME,
  monday_close TIME,
  tuesday_close TIME,
  wednesday_close TIME,
  thursday_close TIME,
  friday_close TIME,
  saturday_close TIME,
  sunday_close TIME
);

CREATE TABLE restaurant_tobe_accepted (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    description TEXT NOT NULL,
    gps_location TEXT,
    user_id INTEGER REFERENCES users(id),
    requested TIMESTAMP
);


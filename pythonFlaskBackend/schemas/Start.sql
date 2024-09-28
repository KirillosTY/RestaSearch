CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    isAdmin BOOLEAN
);
CREATE TABLE restaurant (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    description TEXT NOT NULL,
    gpsLocation TEXT,
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

CREATE TABLE favoriteRestaurants (
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  restaurant_id INTEGER REFERENCES restaurant(id) ON DELETE CASCADE,
  added TIMESTAMP,
  CONSTRAINT unique_favourite UNIQUE (restaurant_id, user_id)
);


CREATE TABLE favorites (
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  userFriended_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  added TIMESTAMP,
  CONSTRAINT unique_friend UNIQUE (userFriended_id, user_id)
);


CREATE TABLE restaurant_hours (
  restaurant_id INTEGER PRIMARY KEY REFERENCES restaurant(id) ON DELETE CASCADE,
  monday TIME,
  tuesday TIME,
  wednesday TIME,
  thursday TIME,
  friday TIME,
  saturday TIME,
  sunday TIME
);

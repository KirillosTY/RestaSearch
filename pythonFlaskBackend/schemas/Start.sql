CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    isAdmin BOOLEAN
);
CREATE TABLE Restaurant (
    id SERIAL PRIMARY KEY,
    name TEXT,
    address TEXT,
    description TEXT,
    openingHours TEXT,
    gpsLocation TEXT,
    user_id INTEGER REFERENCES users,
    added TIMESTAMP
);

CREATE TABLE Reviews (
  restaurant_id INTEGER REFERENCES Restaurant(id) ON DELETE CASCADE,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  comment TEXT,
  rating INTEGER,
  added TIMESTAMP,
  CONSTRAINT unique_review UNIQUE (restaurant_id, user_id)
);





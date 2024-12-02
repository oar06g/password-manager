CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  password TEXT
);

INSERT INTO users (id, password) VALUES (1, 'haIrySECKw');

SELECT password FROM users WHERE id = 1;

CREATE TABLE IF NOT EXISTS info (
  id INTEGER PRIMARY KEY,
  user_id INTEGER,
  sitename TEXT,
  username TEXT,
  password TEXT,
  email TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
)
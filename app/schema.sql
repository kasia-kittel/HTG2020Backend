DROP TABLE IF EXISTS consumer;

CREATE TABLE consumers (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO consumers (id, username, password) VALUES (1, "Joe", "pass1");
INSERT INTO consumers (id, username, password) VALUES (2, "Kate", "pass2");
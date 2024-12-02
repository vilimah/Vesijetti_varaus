CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    sent_at TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    price INT,
    date TEXT,
    time TEXT,
    visible BOOLEAN
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    prod_id INTEGER REFERENCES products ON DELETE CASCADE,
    reserved_at TIMESTAMP
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

INSERT INTO roles (name, description) VALUES (
    'user', 'käyttäjä'
);

INSERT INTO roles (name, description) VALUES (
    'admin', 'pääkäyttäjä'
);

CREATE TABLE userRoles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles ON DELETE CASCADE
);

CREATE TABLE info (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    created TIMESTAMP
);

Test:1
INSERT INTO products (title, description, price, date, time, visible) VALUES (
    'Vesijetti', '2 tuntia vesijeteillä ajelua, tankkaaminen kuuluu hintaan', '149', '30.11.2024','18.30', 'TRUE'
);
Test:2
INSERT INTO products (title, description, price, date, time, visible) VALUES (
    'Vesijetti', '2 tuntia vesijeteillä ajelua, tankkaaminen kuuluu hintaan', '149', '31.11.2024', '14.30', 'TRUE'
);

Jos luo käyttäjän niin tällä syötteellä saa omalle käyttäjälle admin oikeudet jota voi kokeilla.
INSERT INTO userRoles (user_id, role_id) VALUES ('1', '2');

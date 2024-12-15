from db import db
from flask import session
from sqlalchemy.sql import text

# roolin tarkistus
def check_role():
    user_id = session.get("user_id")
    if not user_id:
        return False
    sql = text("SELECT COUNT(*) FROM userRoles WHERE user_id = :user_id AND role_id = 2")
    result = db.session.execute(sql, {"user_id":user_id}).scalar()
    return result > 0

# näkee kaikki käyttäjät
def see_users():
    sql = text("SELECT id, username FROM users ORDER BY username")
    result = db.session.execute(sql)
    return result.fetchall()

# käyttäjän poistaminen
def del_user(given_user):
    sql = text("DELETE FROM users WHERE id = :id")
    result = db.session.execute(sql, {"id":given_user})
    db.session.commit()
    return result.rowcount > 0

# pääkäyttäjäksi lisääminen
def add_admin(given_id):
    admin = 2
    sql = text("INSERT INTO userRoles (user_id, role_id) VALUES (:user_id, :role_id)")
    result = db.session.execute(sql, {"user_id":given_id, "role_id":admin})
    db.session.commit()
    return result.rowcount > 0

# pääkäyttäjän poisto
def del_admin(given_user):
    sql = text("DELETE FROM userRoles WHERE user_id = :given_user")
    result = db.session.execute(sql, {"given_user":given_user})
    db.session.commit()
    return result.rowcount > 0

# näkee kaikki tuottee
def see_products():
    sql = text("SELECT * FROM products WHERE visible=TRUE ORDER BY id")
    result = db.session.execute(sql)
    return result.fetchall()

# lisää uusi tuote
def add_products(title, description, price, date, time):
    boolean = "TRUE"
    sql = text("INSERT INTO products (title, description, price, date, time, visible) VALUES (:title, :description, :price, :date, :time, :visible)")
    result = db.session.execute(sql, {"title":title, "description":description, "price":price, "date":date, "time":time, "visible":boolean})
    db.session.commit()
    return result.rowcount > 0

# poista tuote
def del_products(prod_id):
    sql = text("DELETE FROM products WHERE id = :prod_id")
    result = db.session.execute(sql, {"prod_id":prod_id})
    db.session.commit()
    return result.rowcount > 0

# poista viesti
def del_message(review_id):
    sql = text("DELETE FROM messages WHERE id = :review_id")
    result = db.session.execute(sql, {"review_id":review_id})
    db.session.commit()
    return result.rowcount > 0

# näe varaukset
def see_reservations():
    sql = text("SELECT U.username, P.title, P.description, P.price, P.date, P.time, reserved_at FROM reservations R, users U, products P WHERE U.id = R.user_id AND P.id = R.prod_id  ORDER BY reserved_at")
    result = db.session.execute(sql)
    return result.fetchall()

# näe adminit
def see_admins():
    sql = text("SELECT DISTINCT U.username, R.name, U.id FROM users U, roles R, userRoles I WHERE U.id = I.user_id AND R.id = I.role_id")
    result = db.session.execute(sql)
    return result.fetchall()

# näe infot
def see_info():
    sql = text("SELECT * FROM info ORDER BY created")
    result = db.session.execute(sql)
    return result.fetchall()

# lisää infoa
def add_info(title, description):
    sql = text("INSERT INTO info (title, description, created) VALUES (:title, :description, NOW())")
    result = db.session.execute(sql, {"title":title, "description":description})
    db.session.commit()
    return result.rowcount > 0

# poista info
def delete_info(info_id):
    sql = text("DELETE FROM info WHERE id = :id")
    result = db.session.execute(sql, {"id":info_id})
    db.session.commit()
    return result.rowcount > 0

# näe palautteet
def see_inbox():
    sql = text("SELECT M.id, M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id")
    result = db.session.execute(sql)
    return result.fetchall()

from db import db
from flask import session
from sqlalchemy.sql import text

def check_role():
    user_id = session.get("user_id")
    if not user_id:
        return False
    sql = text("SELECT COUNT(*) FROM userRoles WHERE user_id = :user_id AND role_id = 2")
    result = db.session.execute(sql, {"user_id":user_id}).scalar()
    return result > 0

def see_users():
    sql = text("SELECT id, username FROM users ORDER BY username")
    result = db.session.execute(sql)
    return result.fetchall()

def del_user(given_user):
    sql = text("DELETE FROM users WHERE id = :id")
    result = db.session.execute(sql, {"id":given_user})
    db.session.commit()
    return result.rowcount > 0

def add_admin(given_id):
    admin = 2
    sql = text("INSERT INTO userRoles (user_id, role_id) VALUES (:user_id, :role_id)")
    result = db.session.execute(sql, {"user_id":given_id, "role_id":admin})
    db.session.commit()
    return result.rowcount > 0

def del_admin(given_user):
    user_role = 1
    sql = text("UPDATE userRoles SET role_id = :role_id WHERE user_id = :user_id")
    db.session.execute(sql, {"role_id": user_role, "user_id":given_user})
    db.session.commit()

def see_products():
    sql = text("SELECT * FROM products ORDER BY id")
    result = db.session.execute(sql)
    return result.fetchall()

def add_products(title, description, price, time):
    sql = text("INSERT INTO products (title, description, price, time) VALUES (:time, :description, :price, :time)")
    db.session.execute(sql, {"title":title, "description":description, "price":price, "time":time})
    db.session.commit()

def del_products(prod_id):
    sql = text("DELETE FROM products WHERE id = :prod_id")
    db.session.execute(sql, {"id":prod_id})
    db.session.commit()

def del_message(review_id):
    sql = text("DELETE FROM messages WHERE id = :review_id")
    db.session.execute(sql, {"id":review_id})
    db.session.commit()

def see_reservations():
    sql = text("SELECT * FROM reservations ORDER BY reserved_at")
    result = db.session.execute(sql)
    return result.fetchall()

def see_admins():
    sql = text("SELECT DISTINCT U.username, R.name FROM users U, roles R, userRoles I WHERE U.id = I.user_id AND R.id = I.role_id")
    result = db.session.execute(sql)
    return result.fetchall()




# tee info kenttä johon adminina voi lisätä vaikka mainos tekstiä tai ohjeita, tähän tarvitaan oma taulu
def see_info():
    pass

def add_info():
    pass

def del_info():
    pass

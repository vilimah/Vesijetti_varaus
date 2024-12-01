from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

# kirjautuminen
def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

# uloskirjautuminen
def logout():
    del session["user_id"]

# rekisteröinti
def register(username, password):
    hash_value = generate_password_hash(password, method="pbkdf2:sha256")

    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username,:password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

# hakee käyttäjä id:n
def user_id():
    return session.get("user_id", 0)


def get_profile(user_id):
    sql = text("SELECT id FROM users WHERE id = :id")
    result = db.session.execute(sql, {"id": id})
    user = result.fetchone()
    if user is None:
        return None  
    id = user.id  
    return {
        "id": id
    }

# salasanan vaihtaminen
def change_password(user_id_i, new_password):
    user_id_i = user_id()
    if user_id_i == 0:
        return False
    
    hash_value = generate_password_hash(new_password, method="pbkdf2:sha256")
    
    try:
        sql = text("UPDATE users SET password = :new_password WHERE id = :user_id")
        db.session.execute(sql, {"new_password": hash_value, "user_id": user_id_i})
        db.session.commit()
        return True
    except:
        return False

# hakee kaikki tuotteet listana
def get_products():
    sql = text("SELECT * FROM products WHERE visible = True ")
    result = db.session.execute(sql)
    return result.fetchall()

def book(prod_id):
    try:
        id_user = session.get("user_id", 0)
        sql = text("INSERT INTO reservations (user_id, prod_id, reserved_at) VALUES (:user_id, :prod_id, NOW())")
        sql_hide = text("UPDATE products SET visible = False WHERE id = :prod_id")
        db.session.execute(sql, {"user_id": id_user, "prod_id": prod_id})
        db.session.execute(sql_hide, {"prod_id": prod_id})
        db.session.commit()
        return True
    except:
        return False

def my_reservations():
    id_user = user_id()
    if user_id == 0:
        return False
    sql = text("SELECT P.title, P.description, P.price, P.date, P.time FROM products P, reservations R WHERE R.prod_id = P.id AND R.user_id = :user_id")
    result = db.session.execute(sql, {"user_id":id_user})
    return result.fetchall()



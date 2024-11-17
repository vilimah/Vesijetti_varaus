from db import db
import users
from sqlalchemy.sql import text


def get_list():
    sql = text("SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id")
    result = db.session.execute(sql)
    return result.fetchall()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True

def my_questions():
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("SELECT M.id, M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id AND U.id = :user_id  ORDER BY M.id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def delete_own(message_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("DELETE FROM messages WHERE id = :message_id AND user_id = :user_id")
    db.session.execute(sql, {"message_id":message_id, "user_id":user_id})
    db.session.commit()
    return True
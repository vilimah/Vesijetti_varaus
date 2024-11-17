from app import app
from flask import render_template, request, redirect, session
import users, messages

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/booking")
def booking():
    return render_template("booking.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if not content:
        return render_template("error.html", message="Viestin sisältö on tyhjä")
    if messages.send(content):
        return redirect("/inbox")
    else:  
        return render_template("error.html", message="Viestin lähetys epäonnistui")

@app.route("/inbox")
def inbox():
    list = messages.get_list()
    return render_template("inbox.html", count=len(list), messages=list)

@app.route("/message")
def message():
    return render_template("message.html")

@app.route("/myquestions")
def questions():
    list = messages.my_questions()
    return render_template("myquestions.html", messages=list)

@app.route("/delete", methods=["POST"])
def delete():
    message_id = request.form.get("message_id")
    if not message_id:
        return render_template("error.html", message="Viestin ID puuttuu")
    
    if messages.delete_own(message_id):
        return redirect("/myquestions")
    else:
        render_template("error.html", message="Palautteen poistaminen epäonnistui")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        
@app.route("/burger")
def burger():
    return render_template("burger.html")
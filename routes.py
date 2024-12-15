from app import app
from flask import render_template, request, redirect, session
import users, messages, admin

# etusivu
@app.route("/")
def index():
    admin_role = admin.check_role()
    list_info = users.all_info()
    return render_template("index.html", role=admin_role, info=list_info)

# varaaminen
@app.route("/booking")
def booking():
    list = users.get_products()
    return render_template("booking.html", products=list)

# palautteen lähetys
@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if not content:
        return render_template("error.html", message="Viestin sisältö on tyhjä")
    if messages.send(content):
        return redirect("/inbox")
    else:  
        return render_template("error.html", message="Viestin lähetys epäonnistui")

# palautteet
@app.route("/inbox")
def inbox():
    list = messages.get_list()
    return render_template("inbox.html", count=len(list), messages=list)

# palautteen luonti
@app.route("/message")
def message():
    return render_template("message.html")

# omat palautteet
@app.route("/myquestions")
def questions():
    list = messages.my_questions()
    return render_template("myquestions.html", messages=list)

# palautteen poisto
@app.route("/delete", methods=["POST"])
def delete():
    message_id = request.form.get("message_id")
    if not message_id:
        return render_template("error.html", message="Viestin ID puuttuu")
    
    if messages.delete_own(message_id):
        return redirect("/myquestions")
    else:
        return render_template("error.html", message="Palautteen poistaminen epäonnistui")

# kirjautuminen
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

# uloskirjautuminen      
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

# rekisteröityminen
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

# oma profiili        
@app.route("/profile/<int:user_id>")
def profile(user_id):
    if "user_id" not in session:
        return render_template("error.html", message="Kirjaudu nähdäksesi profiili!")
    admin_role = admin.check_role()
    
    current_user_id = session["user_id"]
    my_res = users.my_reservations()
    if current_user_id == user_id:
        return render_template("profile.html", reservations=my_res, role=admin_role)
    
    return render_template("error.html", message="Ei oikeuksia nähdä sivua!")

# salasanan vaihtaminen
@app.route("/password/<int:user_id>", methods=["GET", "POST"])
def password(user_id):
    if "user_id" not in session:
        return render_template("error.html", message="Kirjaudu vaihtaaksesi salasana!")
    
    current_user_id = session["user_id"]

    if current_user_id != user_id:
        return render_template("error.html", message="Ei oikeuksia nähdä sivua!")
    
    if request.method == "GET":
        return render_template("password.html")
    
    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        if new_password != confirm_password:
            return render_template("error.html", message="Salasanat eroavat")
        if users.change_password(user_id, new_password):
            return redirect(f"/profile/{user_id}")
        else:
            return render_template("error.html", message="Salasanan vaihtaminen ei onnistunut")

# admin päävalikko
@app.route("/admins")
def admin_page():
    if "user_id" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään!")
    
    if not admin.check_role():
        return render_template("error.html", message="Ei oikeuksia nähdä sivua!")
    
    list_users = admin.see_users()
    list_products = admin.see_products()
    list_admins = admin.see_admins()
    list_reservations = admin.see_reservations()
    list_info = admin.see_info()
    list_messages = admin.see_inbox()

    return render_template("admins.html", users=list_users,
                                          products=list_products,
                                          admins=list_admins, 
                                          reservations=list_reservations, 
                                          info=list_info,
                                          messages=list_messages)
                                          
# admin: käyttäjän poistaminen
@app.route("/del/user", methods=["POST"])
def delete_user():
    user_id = request.form.get("user_id")
    if not user_id:
        return render_template("error.html", message="Käyttäjä ID puuttuu")
    
    if admin.del_user(user_id):
        return redirect("/admins")
    else:
        return render_template("error.html", message="Käyttäjän poistaminen epäonnistui")

# admin oikeuksien lisääminen
@app.route("/add/admin", methods=["POST"])
def add_admin():
    user_id = request.form.get("user_id")
    if not user_id:
        return render_template("error.html", message="Käyttäjä ID puuttuu")
    
    if admin.add_admin(user_id):
        return redirect("/admins")
    else:
        return render_template("error.html", message="Adminin lisääminen epäonnistui")

# tuotteen varaaminen
@app.route("/book", methods=["POST"])
def reserve():
    user_id = users.user_id()
    prod_id = request.form.get("prod_id")
    if not prod_id:
        return render_template("error.html", message="Tuote ID puuttuu")
    if users.book(prod_id):
        return redirect(f"/profile/{user_id}")
    else:
        return render_template("error.html", message="Tuotteen varaaminen epäonnistui")
    
# tuotteen lisääminen (admin) 
@app.route("/new/product")
def new_prod():
    if "user_id" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään!")
    
    if not admin.check_role():
        return render_template("error.html", message="Ei oikeuksia nähdä sivua!")
    
    return render_template("product.html")

# lisää tuotteen (admin)
@app.route("/add/product", methods=["POST"])
def add_prod():
    if "user_id" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään!")
    
    if not admin.check_role():
        return render_template("error.html", message="Ei oikeuksia lisätä tuotetta!")
    
    title = request.form["title"]
    description = request.form["description"]
    price = request.form["price"]
    date = request.form["date"]
    time = request.form["time"]
    
    if admin.add_products(title, description, price, date, time):
            return redirect("/admins")
    else:
        return render_template("error.html", message="Tuotteen lisääminen epäonnistui")

# varauksen peruutus  
@app.route("/cancel", methods=["POST"])
def cancel_prod():
    user_id = users.user_id()
    prod_id = request.form.get("prod_id")
    if not prod_id:
        return render_template("error.html", message="Tuoteen ID puuttuuu")
    if users.cancel(prod_id):
        return redirect(f"/profile/{user_id}")
    else:
        render_template("error.html", message="Varauksen poistaminen epäonnistui")

# uuden infon lisäys (admin)
@app.route("/new/info")
def new_info():
    if "user_id" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään!")
    
    if not admin.check_role():
        return render_template("error.html", message="Ei oikeuksia nähdä sivua!")
    
    return render_template("info.html")

# lisää info kenttään infoa (admin)
@ app.route("/add/info", methods=["POST"])
def add_info():
    if "user_id" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään!")
    
    if not admin.check_role():
        return render_template("error.html", message="Ei oikeuksia lisätä infoa!")
    
    title = request.form["title"]
    description = request.form["description"]

    if admin.add_info(title, description):
        return redirect("/admins")
    else:
        return render_template("error.html", message="Infon lisääminen epäonnistui")

# infon poisto (admin)
@app.route("/del/info", methods=["POST"])
def del_info():
    info_id = request.form.get("info_id")
    if not info_id:
        return render_template("error.html", message="Infon ID puuttuu")
    if admin.delete_info(info_id):
        return redirect("/admins")
    else:
        return render_template("error.html", message="Infon poistaminen epäonnistui")

# tuotteen poisto (admin)
@app.route("/del/product", methods=["POST"])
def del_prod():
    prod_id = request.form.get("prod_id")
    if not prod_id:
        return render_template("error.html", message="Tuotteen ID puuttuu")
    if admin.del_products(prod_id):
        return redirect("/admins")
    else:
        return render_template("error.html", message="Tuotteen poistaminen epäonnistui")

# adminin poisto (admin)
@app.route("/del/admin", methods=["POST"])
def del_admin():
    given_user = request.form.get("given_user")
    if not given_user:
        return render_template("error.html", message="Käyttäjä ID puuttuu")
    if admin.del_admin(given_user):
        return redirect("/admins")
    else:
        return render_template("error.html", message="Admin oikeuksien poistaminen epäonnistui")

# palautteen poisto (admin)   
@app.route("/del/review", methods=["POST"])
def del_review():
    review_id = request.form.get("review_id")
    if not review_id:
        return render_template("error.html", message="Palautteen ID puuttuu")
    if admin.del_message(review_id):
        return redirect("/admins")
    else:
        return render_template("error.html", message="Palautteen poistaminen epäonnistui")
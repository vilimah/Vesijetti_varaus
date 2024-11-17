from flask import Flask
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes

# ohjelma ei suostu rekisteröimään uutta käyttäjää! kysy tähän apua -- KOODI TOIMII NYT KUN USERS.PY TIEDOSTOON VAIHDETTU
# hash_value = generate_password_hash(password, method="pbkdf2:sha256")
# hash_value = generate_password_hash(password) sijaan

# vilimahonen, vili123 tunnukset
# maija, maikki1
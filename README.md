# Vesijetti varausjärjestelmä
Tsoha projektityö

Tässä projektissa on toteutettu vesijetti varausjärjestelmä -websovellus. Websovelluksessa voi luoda omat tunnukset ja niillä voi kirjautua sisään. Käyttäjällä on oikeutena vaihtaa salasana, varata tuotteita ja nähdä omat varaukset omasta profiilista sekä peruuttaa varaus, luoda palaute ja poistaa oma palaute tarvittaessa. Kirjautumattomille käyttäjille on myös nähtävillä tuotteet sekä palautteet, mutta jos haluaa varata tai luoda palautteen niin käyttäjän tulee olla kirjautunut. Jos haluaa admin-oikeudet toimimaan niin tulee sijoittaa tietokantaan userRoles käyttäjä id ja rooli id ja siitä eteenpäin admin-oikeudet omaava voi lisätä kenelle tahansa käyttäjälle admin-oikeudet. Admin näkee käyttäjän tekemät varaukset. Admin voi lisätä ja poistaa tuotteita. Admin voi poistaa käyttäjän ja tehdä käyttäjästä admin-käyttäjän. Admin voi poistaa kenen tahansa palautteen. Admin voi lisätä ja poistaa infoa, joka näkyy kaikille vierailijoille etusivulla.


Tätä sovellusta ei toistaiseksi pysty testaamaan fly.io:ssa, mutta tässä on seuraavaksi ohjeet jolla sovellus pitäisi olla testattavissa.

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL= tietokannan-paikallinen-osoite
SECRET_KEY= salainen-avain

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
Määritä vielä tietokannan skeema komennolla

$ psql < schema.sql
Nyt voit käynnistää sovelluksen komennolla

$ flask run

# Vesijetti varausjärjestelmä
Tsoha projektityö

Tässä projektissa olisi tarkoitus luoda web-sovellus, jolla pystyy varaamaan vesijetin + muita siihen liittyviä palveluita käyttöönsä.
Käyttäjä voi kirjautua sisään ja ulos ja luoda tunnukset sivulle.
Käyttäjä voi nähdä vapaana olevat vesijetit, niiden hinnat ja varata sellaisen.
Käyttäjä voi luoda arvostelun, jonka hän voi myös itse poistaa ja hän voi lukea muiden arvosteluja.
Burger-valikko josta löytyy yhteystiedot, kalenteri ja arvostelut.
Ylläpitäjä pystyy muokkaamaan ja rajoittamaan tuotteiden saatavuuksia.
Ylläpitäjä pystyy tarvittaessa poistamaan arvosteluja.
Ylläpitäjä näkee käyttäjän tekemät varaukset.

Välipalautus 2:
Sovelluksen tämän hetkinen tilanne:
- Sovellukseen pystyy luomaan tunnukset ja niillä pystyy kirjautumaan sisään ja ulos
- Kirjautunut käyttäjä voi lisätä ja poistaa arvostelun

Tehtävää:
- Valikon tekeminen
- Tuotteiden lisääminen
- Admin oikeuksien luonti
- Varausjärjestelmä

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

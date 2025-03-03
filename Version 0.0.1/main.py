import mysql.connector
import re

#yhdistetään mysql serveriimme
project_mars = mysql.connector.connect(
  host="localhost",
  user="user",
  password="test",
  database="project_mars"
)

#tehdään hakuväline databaseen
dbSearch = project_mars.cursor()

#tehdään databasesta tuloksen saaminen funktioksi:
def result():
    ugly = dbSearch.fetchall()
    #poistetaan kaikki muut paitsi a-z krijaimet, A-Z kirjaimet ja 0-9 numerot
    beatiful = re.sub(r"[^a-zA-Z0-9 ]", "",str(ugly))
    return beatiful

#pelin aikamäärä on 5 vuotta, vuodesta 2077 vuoteen 2082 joka on 1826 päivää (1 karkausvuosi mukaanlukien) ja tunteina 43824
time = 43824.0
#kerätään valitun pelaajan lompakon rahamäärä
def wallet(id):
    dbSearch.execute(f"select game.wallet from game where game.id = {id}")
    var = result()
    return var

#tähän pelaajaan sidonnainen id, laitan aluksi 1 (Yrjö) jotta en saisi erroria
print(wallet(1))

#onko pelaaja hävinnyt, looppia suoritetaan niin kauan, kun pelaaja ei ole hävinnyt
game_is_playable = True

#tapahtuu kun pelin avaa ensimmäistä kertaa
print("Tervetuloa peliimme nimeltä PELIN NIMI !")
#Looppi jossa pelin toiminnallisuus tapahtuu
while True:
    if not game_is_playable:
        #Pelin häviäminen
        print("Hävisit pelin")
        break

    #TILAPÄINEN PELIN TOIMINTALOGIIKKA, VAIN JOTTA TESTATTIIN ETTÄ PYÖRISI
    player_prompt = int(input("Paina 1 jatkaaksesi peliä ja paina 2 hävitäksesi pelin! "))
    if player_prompt == 1:
        print("Olet pelissä")
    elif player_prompt == 2:
        game_is_playable = False
    else:
        print("Yritä uudestaan, skill issue")



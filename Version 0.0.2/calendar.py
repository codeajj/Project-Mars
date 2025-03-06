import mysql.connector
import re

#Luodaan pelin kalenteri, mikä pystyy kertomaan pvm ja kauan aikaa saapua maaliin.
project_mars = mysql.connector.connect(
  host="localhost",
  user="user",
  password="test",
  database="project_mars"
)
dbSearch = project_mars.cursor()
def result():
    ugly = dbSearch.fetchall()
    #Poistaa kaiken paitsi 1 välilyönnin a-ö krijaimet, A-Z kirjaimet ,ison Ö:n, ison Ä:N, ruotsalainen å kirjain ,norjalainen ö kirjain, viivan
    beatiful = re.sub(r"[^\s+a-öA-ZÖ0-9ÄåÅøØ-]", "",str(ugly))
    return beatiful

player = "Hasan"

def timeCall():
    dbSearch.execute(f"select time from game where player = '{player}';")
    time = result()
    return int(time) #Pelaaja voi kutsua ajan ja tarkistaa kauan jäljellä!

def timecounter():
    dbSearch.execute(f"update game set time = time - 1 where player = '{player}';")
    return #Tämä miinustaa tietokannasta yhden päivän.

game_is_playable = True

while True:
    clock = timeCall() #Pelin kello jolla lasketaan päiviä kunnes loppuu
    if clock == -1:
        game_is_playable = False

    #Game start
    player_prompt = str(input('For move options, type: '"'time'"'. To exit game, type: '"'exit'"'.\n'))
    print(clock)
    print(type(clock))
    if not game_is_playable or player_prompt == "exit":
        #Pelin häviäminen
        print("Game over")
        break

    if player_prompt == "time" or player_prompt == "Time":
        print(f"You have {timeCall()} days left!")
    if player_prompt == "move" or player_prompt == "Move":
        movement = True
        print("Where do you want to go?")
        print("1 Uranus or 2 Mars?")
        go = input()
        if go == "1":
            print("You arrived to Uranus")
            timecounter()
            print(f"You have {timeCall()} days left!")
        if go == "2":
            print("You arrived to Mars")
            timecounter()
            print(f"You have {timeCall()} days left!")

import mysql.connector
import re
import time

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
    #Poistaa kaiken paitsi 1 välilyönnin a-ö krijaimet, A-Z kirjaimet ,ison Ö:n, ison Ä:N, ruotsalainen å kirjain ,norjalainen ö kirjain, viivan
    beatiful = re.sub(r"[^\s+a-öA-ZÖ0-9ÄåÅøØ-]", "",str(ugly))
    return beatiful

#pelin aikamäärä on 5 vuotta, vuodesta 2077 vuoteen 2082 joka on 1826 päivää (1 karkausvuosi mukaanlukien) ja tunteina 43824
time = 43824.0
#kerätään valitun pelaajan lompakon rahamäärä
def wallet(id):
    dbSearch.execute(f"select game.wallet from game where game.id = {id}")
    var = result()
    return var
#ottaa co2 määrän
def co2_consumed(id):
    dbSearch.execute(f"select game.co2_consumed from game where game.id = {id}")
    var = result()
    return var
#selvittää pelaajan nykyisen lokaation ICAO koodin
def location(id):
    dbSearch.execute(f"select game.location from game where game.id = {id}")
    var = result()
    return var
#päivittää lompakon
def walletUpdate(id,amount):
    dbSearch.execute(f"""
    update game
    set game.wallet = game.wallet + {amount}
    where id ='{id}'
""")
    print("Toimii w")
#päivittää co2_päästöt
def co2_consumedUpdate(id,amount):
    dbSearch.execute(f"""
    update game
    set game.co2_consumed = game.co2_consumed + {amount}
    where id = '{id}'
    """)
    print("Toimii C")

#HAHMO FUNKTIOT!
def Yrjö():
    dbSearch.execute("SELECT player FROM game WHERE player = 'Yrjö';")
    print(f"Character:",result())
    dbSearch.execute("SELECT wallet FROM game WHERE player = 'Yrjö';")
    print(f"Wallet:",result())
    return
def Hasan():
    dbSearch.execute("SELECT player FROM game WHERE player = 'Hasan';")
    print(f"Character:",result())
    dbSearch.execute("SELECT wallet FROM game WHERE player = 'Hasan';")
    print(f"Wallet:",result())
    return
def kim():
    dbSearch.execute("SELECT player FROM game WHERE player = 'Kim';")
    print(f"Character:",result())
    dbSearch.execute("SELECT wallet FROM game WHERE player = 'Kim';")
    print(f"Wallet:",result())
    return
#country() funktio ei tee muuta kun kutsu "player" muuttujan nimisen hahmon lokaation.
def country():
    ugly = dbSearch.fetchall()
    selection = re.sub(r"[^\s+a-öA-ZÖ0-9ÄåÅøØ-]", "",str(ugly))
    return selection

#tähän pelaajaan sidonnainen id, laitan aluksi 1 (Yrjö) jotta en saisi erroria
walletUpdate(1,2000)
co2_consumedUpdate(1,1500)
print(wallet(1))
print(co2_consumed(1))
print(location(1))

#onko pelaaja hävinnyt, looppia suoritetaan niin kauan, kun pelaaja ei ole hävinnyt
game_is_playable = True

#tapahtuu kun pelin avaa ensimmäistä kertaa

#character_select.py alkaa!
#INTRO, game start. Kirjoita "exit" ja peli sammuu, pätee koko character selection osuuteen.
game = input("Start the game? [Y/N] ")
if game == "Y" or game == "y":
    print("Welcome to Project Mars Demo!")
    print("You have three difficulties, each with a different character!")

    print("""
          1. Normal

          2. Hard

          3. Extreme!
    """)

    diff = input("Choose your difficulty: ")
#Vaikeustason valinta, printtaa hahmo fuktiot ja asettaa "player" muuttujan hahmoksi. LOOP!
    while diff != "1" or diff != "2" or diff != "3":

        if diff == "1":
            Yrjö()
            confirm = input("Do you want to continue? [Y/N] ")
            if confirm == "Y" or confirm == "y":
                player = "Yrjö"
                break
            elif confirm == "N" or confirm == "n":
                diff = input("Choose your difficulty: ")
        elif diff == "2":
            Hasan()
            confirm = input("Do you want to continue? [Y/N] ")
            if confirm == "Y" or confirm == "y":
                player = "Hasan"
                break
            elif confirm == "N" or confirm == "n":
                diff = input("Choose your difficulty: ")

        elif diff == "3":
            kim()
            confirm = input("Do you want to continue? [Y/N] ")
            if confirm == "Y" or confirm == "y":
                player = "Kim"
                break
            elif confirm == "N" or confirm == "n":
                diff = input("Choose your difficulty: ")
        elif diff == "Exit" or diff == "exit":
            exit()

        else:
            print("Try writing 1, 2 or 3")
            diff = input("Choose your difficulty: ")
elif game == "N" or game == "n":
    print("Bye bye!")
    exit()
#Hahmo valittu koodi, pelin ALKU
dbSearch.execute(f"SELECT airport.name as 'Airport' FROM airport, game WHERE location = ident and player = '{player}';")
print(f"Welcome {player} to {country()}")
#character_select.py LOPPUU! exit ei enään toimi!

#Looppi jossa pelin toiminnallisuus tapahtuu
while True:
    player_prompt = str(input('For move options, type: '"'move'"'. To exit game, type: '"'exit'"'. '))

    if not game_is_playable or player_prompt == "exit":
        #Pelin häviäminen
        print("Game over")
        break

    if player_prompt == "move":
        print("You can move to ")

    else:
        print("Wrong option, try again")

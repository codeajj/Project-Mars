
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
player = ""
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
#päivittää co2_päästöt
def co2_consumedUpdate(id,amount):
    dbSearch.execute(f"""
    update game
    set game.co2_consumed = game.co2_consumed + {amount}
    where id = '{id}'
    """)
    #funktio vaatii kentokentän numeron jossa pelaaja on
def airports():
    #Tiivistettynä tässä koodissa katsotaan minne eri paikkoihin pelaaja voi siitryä kyseisestä letokentästä ja printtaa vaihtoehdot
    locations = {}
    #selvitetään missä maassa ollaan
    dbSearch.execute(f"select country.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")
    currentCountry = result()
    #asetetaan jokiaselle lentokentälle 2 pientä, 2 keskikokoista ja seuraavan maahan iso lentokentän ICAO koodi
    if currentCountry == "Argentina":
        ICAO = ["SAAC", "SAAP", "SACC", "SAOI", "YSSY"]
    elif currentCountry =="Australia":
        ICAO = ["YBIE","YBWN","YBLA","YBOA","ZBAD"]
    elif currentCountry == "China":
        ICAO = ["", "", "", "", ""]# Vasta 2 lentokenttää täytetty, muut myöhemmin kun on ajankontaista
    elif currentCountry == "Germany":
        ICAO = ["", "", "", "", ""]
    elif currentCountry == "Luxembourg":
        ICAO = ["", "", "", "", ""]
    elif currentCountry =="Mongolia":
         ICAO = ["", "", "", "", ""]
    elif currentCountry == "Norway":
        ICAO = ["", "", "", "", ""]
    elif currentCountry == "Poland":
        ICAO = ["", "", "", "", ""]
    elif currentCountry == "South Korea":
        ICAO = ["", "", "", "", ""]
    elif currentCountry == "United States":
        ICAO = ["", "", "", "", ""]
    else:
        print("Error 404")
    for i in ICAO:
        dbSearch.execute(f"select airport.name from airport where gps_code = '{i}'")
        var1 = result()
        dbSearch.execute(f"select airport.type from airport where gps_code = '{i}'")
        var2 = result()
        locations.update({var1 : var2})
        airportTypes = {}
        for k, v in locations.items():
            airportTypes.setdefault(v, []).append(k)
        # yllä etsittiin lentokenttien nimet ja tyypit ja säilöttiin ne tekiöihin mediumairport, smallairport ja largeairport
    #selvitetään mikä on seuraava maa
    dbSearch.execute(f"select country.name from airport,country where airport.iso_country = country.iso_country and gps_code = '{ICAO[-1]}'")
    nextCountry = result()
    print(f"In {currentCountry} can go to 2 different small airports: \n{airportTypes["smallairport"]} \nOr 2 different medium airports: \n{airportTypes["mediumairport"]} \nOr you can go to next level in {nextCountry}: \n{airportTypes["largeairport"]}")
    return airportTypes
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
    player_prompt = str(input('For move options, type: '"'move'"'. To exit game, type: '"'exit'"'.\n'))

    if not game_is_playable or player_prompt == "exit":
        #Pelin häviäminen
        print("Game over")
        break

    if player_prompt == "move":
        airports()
    else:
        print("Wrong option, try again")

import mysql.connector
import re
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

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

def textCleaner(text): # toimii kuin resultin funktio, mutta tallentaa pilkut myös
    beatiful = re.sub(r"[^\s+a-öA-ZÖ,0-9ÄåÅøØ-]", "",str(text))
    return beatiful

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
    global nextCountry
    nextCountry = result()
    print(f"In {currentCountry} can go to 2 different small airports: \n{textCleaner(airportTypes["smallairport"])} \nOr 2 different medium airports: \n{textCleaner(airportTypes["mediumairport"])} \nOr you can go to next level in {nextCountry}: \n{textCleaner(airportTypes["largeairport"])}")
    return airportTypes
#liikkumis / move funktio, päivitetään databasen pelaajan olinpaikka pelaajan valitsemista vaihtoehdoista
def move():
    global nextCountry
    player_move_prompt = int(input(f"Type: '1' , to move to next country {nextCountry} or type: '2' to move inside the country "))
    new_location = dbSearch.execute(f"select gps_code from airport, country where airport.iso_country = country.iso_country and type ='large_airport' and country.name = '{nextCountry}'")
    new_location = result()
    islooping = True
    while islooping:
        if player_move_prompt == 1:
            dbSearch.execute(f"update game set location = '{new_location}'")
            islooping = False
        elif player_move_prompt == 2:
            events()
            islooping = False
        else:
            print("Wrong option, try again")
            player_move_prompt = int(input(f"Type: '1' , to move to next country {nextCountry} "))
            break
    return
#maan sisällä liikkuminen eventeissä
def events():
    #PLACEHOLDER
    print("You have chosen to move inside the country")
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
def co2_emission():
    #tarkoituksena laskea kuinka pitkä matka lentokenttien välillä


    #mistä mennään
    dbSearch.execute(f"select airport.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")
    kentta1 = "Ministro Pistarini International Airport"
    print(kentta1)

    # minne mennään, hard codataan testin vuoksi austraalia
    """
    dbSearch.execute(f"select country.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")
    kentta2 = tulos()
    """
    kentta2 = "Sydney Kingsford Smith International Air"
    geolocator = Nominatim(user_agent="test")
    location1 = geolocator.geocode(str(kentta1),timeout=7)
    location2 = geolocator.geocode(str(kentta2),timeout=7)

    kentta1 = location1.latitude, location1.longitude
    kentta2 = location2.latitude, location2.longitude
    lopputulos = geodesic(kentta1, kentta2)
    print(lopputulos)
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
print(f"Welcome {player} to {result()}")
#character_select.py LOPPUU! exit ei enään toimi!

#pelin lokaatio resettaa
dbSearch.execute(f"update game set location = 'SAEZ'")

#Looppi jossa pelin toiminnallisuus tapahtuu
while True:
    player_prompt = str(input('For move options, type: '"'move'"'. To exit game, type: '"'exit'"'.\n'))

    if not game_is_playable or player_prompt == "exit":
        #Pelin häviäminen
        print("Game over")
        break

    if player_prompt == "move":
        airports()
        #Tällä hetkellä liikutaan vain maiden välillä isoilla lentokentillä
        #Mikäli pelaaja ei liiku, voi se suorittaa tapahtumia WIP
        move()
    else:
        print("Wrong option, try again")

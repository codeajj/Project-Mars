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
    # käytetään lentokenttien nimiä myöhemmin koodissa
    global airport_names
    airport_names = []
    locations = {}
    #selvitetään missä maassa ollaan
    dbSearch.execute(f"select country.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")
    currentCountry = result()
    #asetetaan jokiaselle lentokentälle 2 pientä, 2 keskikokoista ja seuraavan maahan iso lentokentän ICAO koodi
    if currentCountry == "Argentina":
        ICAO = ["SAAC", "SAOI", "SACC", "SAAP", "YSSY"]
    elif currentCountry =="Australia":
        ICAO = ["YBOA","YBWN","YBLA","YBIE","ZMCK"]
    elif currentCountry == "Mongolia":
        ICAO = ["ZMUG", "ZMTG", "ZMMN", "ZMUB", "ZBAD"]
    elif currentCountry == "China":
        ICAO = ["ZBCZ", "ZGLD", "ZLGL", "ZYDD", "EDDF"]
    elif currentCountry =="Germany":
         ICAO = ["", "", "", "", "EPWA"]#Broken uwu
    elif currentCountry == "Poland":
        ICAO = ["EPEL", "EPBA", "EPCE", "EPKT", "ELLX"]
    elif currentCountry == "Luxembourg":
        ICAO = ["ELNT", "ELUS", "ENGM"] #TODO tee funktio joka huomioi luxembpurgin lentokenttien puuttuvan määrän
    elif currentCountry == "Norway":
        ICAO = ["", "", "", "", "RKSI"]#boken
    elif currentCountry == "South Korea":
        ICAO = ["RKTA", "RKTL", "RKNY", "RKTU", "KJFK"]
    elif currentCountry == "United States":
        ICAO = ["", "", "", ""]#BROKEN HUOM TÄÄLLÄ VAIN 4 KENTTÄÄ
    else:
        print("Error 404")
    for i in ICAO:
        dbSearch.execute(f"select airport.name from airport where gps_code = '{i}'")
        var1 = result()
        dbSearch.execute(f"select airport.type from airport where gps_code = '{i}'")
        var2 = result()
        list.append(airport_names,var1)
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
    player_move_prompt = int(input(f"Type: '1' , to move to next country {nextCountry} or \ntype: '2' to move inside the country \n"))
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
            player_move_prompt = int(input(f"Type: '1' , to move to next country {nextCountry} \n"))
            break
    return
#maan sisällä liikkuminen eventeissä
def events():
#Sama rakenne kuin movessa
#Näyttää pelaajalle nimet kahdesta pienestä ja kahdesta keskikokoisesta
# lentokentästä johon liikkua
# MAAN SISÄLLÄ
    player_move_prompt_inside_country = int(input(f"""Type: '1' , to move to {airport_names[0]} or 
Type: '2' , to move  to {airport_names[1]} or 
Type: '3' , to move  to {airport_names[2]} or 
Type: '4' , to move  to {airport_names[3]}\n """))

#Ei ole vielä itse eventtejä joita tapahtuu kyseisissä lentokentissä
    islooping = True
    while islooping:
        if player_move_prompt_inside_country == 1:

            islooping = False
        elif player_move_prompt_inside_country == 2:

            islooping = False
        elif player_move_prompt_inside_country == 3:

            islooping = False
        elif player_move_prompt_inside_country == 4:

            islooping = False
        else:
            print("Wrong option, try again")
            player_move_prompt_inside_country = int(input(f"""Type: '1' , to move to {airport_names[0]} or 
            Type: '2' , to move  to {airport_names[1]} or 
            Type: '3' , to move  to {airport_names[2]} or 
            Type: '4' , to move  to {airport_names[3]}\n """))
            break
    return
#Funktio kertomaan pelaajalle missä maassa ollaan
def tell_location():
    dbSearch.execute(f"select country.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")
    currentCountry = result()
    return print(f"Your current location is: {currentCountry} ")
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
    #etsii nykyisen pelaajan siainnin
    dbSearch.execute(f"select airport.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")
    kentta1 = result()
    print(kentta1)

    # selvittää mikä on seuraava lentokenttä minne mennään
    # TODO saa tähän pelaajan valitsema maa
    #dbSearch.execute(f"select country.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")

    #käytetään geopy selvittääksemme maiden latitude ja longtitude koordinaatit
    kentta2 = tulos()
    print(kentta2)
    geolocator = Nominatim(user_agent="test")
    location1 = geolocator.geocode(kentta1, timeout=7)
    location2 = geolocator.geocode(kentta2, timeout=7)
    print(location2)
    print(location1)
    latlong1 = location1.latitude, location1.longitude
    latlong2 = location2.latitude, location2.longitude
    #selvitetään maiden etäisyys latitudella ja longtitudella
    distance = geodesic(latlong1, latlong2)
    # muutetaan geopy:n muodosta float luvuksi
    strdistance = str(distance)
    # poistetaan km lopusta
    totaldist = float(re.sub(r"[^0-9.]", "", strdistance))
    # km to mile
    totaldist = totaldist / 1.6
    # 1 henkilön arvoiodut co2 päästöt per 1 maili
    co2Randomizer = random.randint(150, 300)
    # kerrotaan matka liikutuilla maileilla
    co2 = totaldist * co2Randomizer
    # mile to km
    co2 = co2 * 1.6
    # g to kg
    co2 = co2 / 1000
    # end result: co2 kg/km ja siirertään se databaseen
    dbSearch.execute(f"update game set co2_consumed = co2_consumed + {co2} where player = {player}")

#onko pelaaja hävinnyt, looppia suoritetaan niin kauan, kun pelaaja ei ole hävinnyt
game_is_playable = True

#tapahtuu kun pelin avaa ensimmäistä kertaa

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
#resettaa co2 mittarin
dbSearch.execute(f"update game set co2_consumed = '0'")



#Looppi jossa pelin toiminnallisuus tapahtuu
while True:
    player_prompt = str(input('For move options, type: '"'move'"'. \nFor current country location, type: '"'gps'"'. \nTo exit game, type: '"'exit'"'.\n'))

    if not game_is_playable or player_prompt == "exit":
        #Pelin häviäminen
        print("Game over")
        break

    if player_prompt == "move":
        airports()
        #Tällä hetkellä liikutaan vain maiden välillä isoilla lentokentillä
        #Mikäli pelaaja ei liiku, voi se suorittaa tapahtumia WIP
        move()

    #Pelaaja voi katsoa nykyisen lokaation
    elif player_prompt == "gps":
        tell_location()

    else:
        print("Wrong option, try again")

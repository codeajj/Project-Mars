import mysql.connector
import re
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import random

# yhdistetään mysql serveriimme
project_mars = mysql.connector.connect(
    host="localhost",
    user="user",
    password="test",
    database="project_mars"
)
player = ""
player_has_gone_to_events = False
# tehdään hakuväline databaseen
dbSearch = project_mars.cursor()


# tehdään databasesta tuloksen saaminen funktioksi:
def result():
    ugly = dbSearch.fetchall()
    # Poistaa kaiken paitsi 1 välilyönnin a-ö krijaimet, A-Z kirjaimet ,ison Ö:n, ison Ä:N, ruotsalainen å kirjain ,norjalainen ö kirjain, viivan
    beatiful = re.sub(r"[^\s+a-öA-ZÖ0-9ÄåÅøØ-]", "", str(ugly))
    return beatiful


def textCleaner(text):  # toimii kuin resultin funktio, mutta tallentaa pilkut myös
    beatiful = re.sub(r"[^\s+a-öA-ZÖ,0-9ÄåÅøØ-]", "", str(text))
    return beatiful


# selvittää liikuttavat lentokentät
def airports():
    # Tiivistettynä tässä koodissa katsotaan minne eri paikkoihin pelaaja voi siitryä kyseisestä letokentästä ja printtaa vaihtoehdot
    # käytetään lentokenttien nimiä myöhemmin koodissa
    global airport_names
    airport_names = []
    locations = {}
    # selvitetään missä maassa ollaan
    dbSearch.execute(
        f"select country.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")
    currentCountry = result()
    # asetetaan jokiaselle lentokentälle 2 pientä, 2 keskikokoista ja seuraavan maahan iso lentokentän ICAO koodi
    if currentCountry == "Argentina":
        ICAO = ["SAAC", "SAOI", "SACC", "SAAP", "YSSY"]
    elif currentCountry == "Australia":
        ICAO = ["YBOA", "YBWN", "YBLA", "YBIE", "ZMCK"]
    elif currentCountry == "Mongolia":
        ICAO = ["ZMUG", "ZMTG", "ZMMN", "ZMUB", "ZBAD"]
    elif currentCountry == "China":
        ICAO = ["ZBCZ", "ZGLD", "ZLGL", "ZYDD", "EDDF"]
    elif currentCountry == "Germany":
        ICAO = ["EDCS", "EDBP", "EDAC", "EDBM", "EPWA"]
    elif currentCountry == "Poland":
        ICAO = ["EPEL", "EPBA", "EPCE", "EPKT", "ELLX"]
    elif currentCountry == "Luxembourg":
        ICAO = ["ELNT", "ELUS", "ENGM"]  # TODO tee funktio joka huomioi luxembpurgin lentokenttien puuttuvan määrän
    elif currentCountry == "Norway":
        ICAO = ["ESD", "ENSG", "ENAL", "ENSS", "RKSI"]
    elif currentCountry == "South Korea":
        ICAO = ["RKTA", "RKTL", "RKNY", "RKTU", "KJFK"]
    elif currentCountry == "United States":
        ICAO = ["PALB", "PAUO", "KEGE", "KBSE", "MARS"]  # BROKEN HUOM TÄÄLLÄ VAIN 4 KENTTÄÄ
    else:
        print("Error 404")
    for i in ICAO:
        dbSearch.execute(f"select airport.name from airport where gps_code = '{i}'")
        var1 = result()
        dbSearch.execute(f"select airport.type from airport where gps_code = '{i}'")
        var2 = result()
        list.append(airport_names, var1)
        locations.update({var1: var2})
        airportTypes = {}
        for k, v in locations.items():
            airportTypes.setdefault(v, []).append(k)
        # yllä etsittiin lentokenttien nimet ja tyypit ja säilöttiin ne tekiöihin mediumairport, smallairport ja largeairport
    # selvitetään mikä on seuraava maa
    dbSearch.execute(
        f"select country.name from airport,country where airport.iso_country = country.iso_country and gps_code = '{ICAO[-1]}'")
    global nextCountry
    nextCountry = result()
    if currentCountry == "Luxembourg":
        print(
            f"In {currentCountry} you can go to 2 different small airports: \n{textCleaner(airportTypes["smallairport"])} \nor to the next level in {nextCountry}: \n{textCleaner(airportTypes["largeairport"])}")
    elif currentCountry == "United States":
        print(
            f"In {currentCountry} you can go to 2 different small airports: \n{textCleaner(airportTypes["smallairport"])} \nOr to an different medium airport: \n{textCleaner(airportTypes["mediumairport"])} \nOr you can win the game by going to Mars")
    else:
        print(
            f"In {currentCountry} you can go to 2 different small airports: \n{textCleaner(airportTypes["smallairport"])} \nOr 2 different medium airports: \n{textCleaner(airportTypes["mediumairport"])} \nOr you can go to the next level in {nextCountry}: \n{textCleaner(airportTypes["largeairport"])}")
    return airportTypes


# liikkumis / move funktio, päivitetään databasen pelaajan olinpaikka pelaajan valitsemista vaihtoehdoista
def move():
    global nextCountry
    player_move_prompt = int(
        input(f"\nType: '1' to move to next country {nextCountry} or \ntype: '2' to move inside the country \n"))
    new_location = dbSearch.execute(
        f"select gps_code from airport, country where airport.iso_country = country.iso_country and type ='large_airport' and country.name = '{nextCountry}'")
    new_location = result()
    islooping = True
    while islooping:
        if player_move_prompt == 1:
            dbSearch.execute(f"update game set location = '{new_location}'")
            timeupdate()

            airports()
            main_airport_event()
            islooping = False
        elif player_move_prompt == 2:
            events()
            islooping = False
        else:
            print("Wrong option, try again")
            player_move_prompt = int(input(f"Type: '1' to move to next country {nextCountry} \n"))
            break
    return


def timeCall():
    dbSearch.execute(f"select time from game where player = '{player}';")
    time = result()
    return int(time)  # Pelaaja voi kutsua ajan ja tarkistaa kauan jäljellä!


def timeupdate():
    dbSearch.execute(f"update game set time = time - 1 where player = '{player}';")
    return  # Tämä miinustaa tietokannasta yhden päivän.


# maan sisällä liikkuminen eventeissä
def events():
    global player_has_gone_to_events, place1_state, place2_state, place3_state, place4_state, place1_option, place2_option, place3_option, place4_option
    start_ICAO = "SAEZ"
    argentina_ICAO = ["SAAC", "SAOI", "SACC", "SAAP", "YSSY"]
    australia_ICAO = ["YBOA", "YBWN", "YBLA", "YBIE", "ZMCK"]
    mongolia_ICAO = ["ZMUG", "ZMTG", "ZMMN", "ZMUB", "ZBAD"]
    china_ICAO = ["ZBCZ", "ZGLD", "ZLGL", "ZYDD", "EDDF"]
    germany_ICAO = ["EDCS", "EDBP", "EDAC", "EDBM", "EPWA"]
    poland_ICAO = ["EPEL", "EPBA", "EPCE", "EPKT", "ELLX"]
    luxembourg_ICAO = ["ELNT", "ELUS", "ENGM"]
    norway_ICAO = ["ESD", "ENSG", "ENAL", "ENSS", "RKSI"]
    south_korea_ICAO = ["RKTA", "RKTL", "RKNY", "RKTU", "KJFK"]
    united_states_ICAO= ["PALB", "PAUO", "KEGE", "KBSE", "MARS"]

    dbSearch.execute(f"select gps_code from airport, game where game.location = airport.ident and player = '{player}'")
    current_ICAO = result()
    if current_ICAO == start_ICAO:
        if not player_has_gone_to_events:
            places_to_go = argentina_ICAO[0:4]
            local_airport_names = []
            for i in places_to_go:
                dbSearch.execute(f"select name from airport where gps_code = '{i}'")
                place_to_go = result()
                local_airport_names.append(place_to_go)
            i = 0
            go_to_output = "\nYou can go to: "
            while i < len(local_airport_names):
                go_to_output += f"{local_airport_names[i]}, "
                i += 1
            go_to_output = go_to_output[:-2]
            print(go_to_output)
            place1_state = local_airport_names[0]
            place2_state = local_airport_names[1]
            place3_state = local_airport_names[2]
            place4_state = local_airport_names[3]
            place1_option = 1
            place2_option = 2
            place3_option = 3
            place4_option = 4
        while True:
            player_chosen_place = int(input(f"""\nType: '1' to go to {place1_state} or\n
Type: '2' to go to {place2_state} or\n
Type: '3' to go to {place3_state} or\n
Type: '4' to go to {place4_state} or\n
Type: '5' to leave!\n"""))
            if player_chosen_place == place1_option:
                #EKAN MAAN ('SAAC') EVENTTI TULEE TÄHÄN
                print(f"You have arrived in {place1_state}. Also, we will now print 4 lines of information to you that you don't need :)")
                co2_emission(place1_state)
                dbSearch.execute(f"select co2_consumed from game where player = '{player}'")
                show_emissions = result()
                print(f"Your total emissions increased to {show_emissions} ")
                place1_state = "OPTION USED"
                place1_option = 0
            elif player_chosen_place == place2_option:
                # EKAN MAAN ('SAOI') EVENTTI TULEE TÄHÄN
                print(f"You have arrived in {place2_state}. Also, we will now print 4 lines of information to you that you don't need :)")
                co2_emission(place2_state)
                dbSearch.execute(f"select co2_consumed from game where player = '{player}'")
                show_emissions = result()
                print(f"Your total emissions increased to {show_emissions} ")
                place2_state = "OPTION USED"
                place2_option = 0
            elif player_chosen_place == place3_option:
                # EKAN MAAN ('SACC') EVENTTI TULEE TÄHÄN
                print(f"You have arrived in {place3_state}. Also, we will now print 4 lines of information to you that you don't need :)")
                co2_emission(place3_state)
                dbSearch.execute(f"select co2_consumed from game where player = '{player}'")
                show_emissions = result()
                print(f"Your total emissions increased to {show_emissions} ")
                place3_state = "OPTION USED"
                place3_option = 0
            elif player_chosen_place == place4_option:
                # EKAN MAAN ('SAAP') EVENTTI TULEE TÄHÄN
                print(f"You have arrived in {place4_state}. Also, we will now print 4 lines of information to you that you don't need :)")
                co2_emission(place4_state)
                dbSearch.execute(f"select co2_consumed from game where player = '{player}'")
                show_emissions = result()
                print(f"Your total emissions increased to {show_emissions} ")
                place4_state = "OPTION USED"
                place4_option = 0
            elif player_chosen_place == 5:
                print("You have left from inside country events\n")
                player_has_gone_to_events = True
                break
            else:
                print("Incorrect prompt, action not found please try again")
    return
# Kutsutaan pelin alussa (triggeröidäkseen ekan eventin) ja move():ssa, kun pelaaja
# valitsee liikkuvansa päälentokentälle ja pakotetaan päälentokentän eventti pelaajalle
def main_airport_event():
    # Tänne eventtien otsikot
    large_airport_events = [
        "FIRST EVENT",
        "SECOND EVENT",
        "THIRD EVENT",
        "FOURTH EVENT",
        "FIFTH EVENT",
        "SIXTH EVENT",
        "SEVENTH EVENT",
        "EIGHT EVENT",
        "NINTH EVENT",
        "TENTH EVENT",
    ]
    dbSearch.execute(f"select id from game where player = '{player}'")
    current_player_id = result()

    dbSearch.execute(f"select location from game where id ='{current_player_id}'")
    current_location = result()

    dbSearch.execute(
        f"select location from game, airport where game.location = airport.ident and airport.type = 'large_airport' and game.id = '{current_player_id}'")
    check_current_large_airport = result()
    if current_location == check_current_large_airport:
        if check_current_large_airport == 'SAEZ':
            # Ensimmäisen eventin toiminnallisuus
            print(large_airport_events[0])
            return
        elif check_current_large_airport == 'YSSY':
            # Toisen eventin toiminnallisuus
            print(large_airport_events[1])
            return
        elif check_current_large_airport == 'ZMCK':
            # Kolmannen eventin toiminnallisuus
            print(large_airport_events[2])
            return
        elif check_current_large_airport == 'ZBAD':
            # Neljännen eventin toiminnallisuus
            print(large_airport_events[3])
            return
        elif check_current_large_airport == 'EDDF':
            # Viidennen eventin toiminnallisuus
            print(large_airport_events[4])
            return
        elif check_current_large_airport == 'EPWA':
            # Kuudennen eventin toiminnallisuus
            print(large_airport_events[5])
            return
        elif check_current_large_airport == 'ELLX':
            # Seitsemännen eventin toiminnallisuus
            print(large_airport_events[6])
            return
        elif check_current_large_airport == 'ENGM':
            # Kahdeksannen eventin toiminnallisuus
            print(large_airport_events[7])
            return
        elif check_current_large_airport == 'RKSI':
            # Yhdeksännen eventin toiminnallisuus
            print(large_airport_events[8])
            return
        elif check_current_large_airport == 'KJFK':
            # Kymmenennen eventin toiminnallisuus
            print(large_airport_events[9])
            return


# Funktio kertomaan pelaajalle missä maassa ollaan
def tell_location():
    dbSearch.execute(
        f"select country.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")
    currentCountry = result()
    return print(f"Your current location is: {currentCountry}\n")


# HAHMO FUNKTIOT!
def Yrjö():
    dbSearch.execute("SELECT player FROM game WHERE player = 'Yrjö';")
    print(f"Character:", result())
    dbSearch.execute("SELECT wallet FROM game WHERE player = 'Yrjö';")
    print(f"Wallet:", result())
    return


def Hasan():
    dbSearch.execute("SELECT player FROM game WHERE player = 'Hasan';")
    print(f"Character:", result())
    dbSearch.execute("SELECT wallet FROM game WHERE player = 'Hasan';")
    print(f"Wallet:", result())
    return


def kim():
    dbSearch.execute("SELECT player FROM game WHERE player = 'Kim';")
    print(f"Character:", result())
    dbSearch.execute("SELECT wallet FROM game WHERE player = 'Kim';")
    print(f"Wallet:", result())
    return


# co2 kalkulaattori

# vaatii 2 tietoa ennen kuin toimii: 1.toisen lentokentän nimen 2.pelaajan nimen
def co2_emission(secound_airport):
    # etsii nykyisen pelaajan siainnin
    dbSearch.execute(
        f"select airport.name from airport,country, game where airport.iso_country = country.iso_country and game.location = airport.ident and player = '{player}'")
    kentta1 = result()
    print(kentta1)
    kentta2 = secound_airport
    print(kentta2)
    geolocator = Nominatim(user_agent="test")
    location1 = geolocator.geocode(kentta1, timeout=7)
    location2 = geolocator.geocode(kentta2, timeout=7)
    print(location2)
    print(location1)
    latlong1 = location1.latitude, location1.longitude
    latlong2 = location2.latitude, location2.longitude
    # selvitetään maiden etäisyys latitudella ja longtitudella
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
    dbSearch.execute(f"update game set co2_consumed = co2_consumed + {co2} where player = '{player}'")


# onko pelaaja hävinnyt, looppia suoritetaan niin kauan, kun pelaaja ei ole hävinnyt
game_is_playable = True
# tapahtuu kun pelin avaa ensimmäistä kertaa
# INTRO, game start. Kirjoita "exit" ja peli sammuu, pätee koko character selection osuuteen.
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
    # Vaikeustason valinta, printtaa hahmo fuktiot ja asettaa "player" muuttujan hahmoksi. LOOP!
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
co2_emission("Dandong Langtou Airport")
# Hahmo valittu koodi, pelin ALKU
dbSearch.execute(f"SELECT airport.name as 'Airport' FROM airport, game WHERE location = ident and player = '{player}';")
print(f"Welcome {player} to {result()}")
# character_select.py LOPPUU! exit ei enään toimi!

# pelin lokaatio resettaa
dbSearch.execute(f"update game set location = 'SAEZ'")
# resettaa co2 mittarin
dbSearch.execute(f"update game set co2_consumed = '0'")

exitList = {"Exit", "exit", "Exit game", "exit game", "Quit", "quit", "Quit game", "quit game"}
gpsList = {"GPS", "GPs", "Gps", "gps"}
helpList = {"?", "Help", "help"}
main_airport_event()

# Looppi jossa pelin toiminnallisuus tapahtuu
while True:
    clock = timeCall()  # Pelin kello jolla lasketaan päiviä kunnes loppuu
    if clock == -1:
        game_is_playable = False
    player_prompt = str(input('For actions type '"'Help or ?'"'\n'))

    if not game_is_playable:
        # Pelin häviäminen
        print("Game over")
        break
    if player_prompt in exitList:
        # Pelaaja itse lopettaa
        print("Bye bye!")
        break

    if player_prompt == "Move" or player_prompt == "move":
        # näyttää lentokenttien nimet minne pelaaja voi siirtyä
        airports()
        # Tällä hetkellä liikutaan vain maiden välillä isoilla lentokentillä
        # Mikäli pelaaja ei liiku, voi se suorittaa tapahtumia WIP
        move()
    if player_prompt == "Time" or player_prompt == "time":
        print(f"You have {timeCall()} days left!\n")

    # Pelaaja voi katsoa nykyisen lokaation
    elif player_prompt in gpsList:
        tell_location()

    elif player_prompt in helpList:
        print("""        Move
        Time
        GPS

        Quit game
        """)

    else:
        print("Incorrect prompt, action not found please try again")
import mysql.connector
import time
import re

mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="test",
  database="project_mars"
)

#KAUNEUS FILTTERI ON!
dbHaku = mydb.cursor()
def tulos():
    ugly = dbHaku.fetchall()
    selection = re.sub(r"[^a-öA-Ö0-9 ]", "", str(ugly))
    return selection

#HAHMOT:
def Yrjö():
    dbHaku.execute("SELECT player FROM game WHERE player = 'Yrjö';")
    print(f"Character: ",tulos())
    dbHaku.execute("SELECT wallet FROM game WHERE player = 'Yrjö';")
    print(f"Wallet: ",tulos())
    dbHaku.execute("SELECT airport.name as 'Airport' FROM airport, game WHERE location = ident and player = 'Yrjö';")
    print(f"Location: ",tulos())
    return
def Hasan():
    dbHaku.execute("SELECT player FROM game WHERE player = 'Hasan';")
    print(f"Character: ",tulos())
    dbHaku.execute("SELECT wallet FROM game WHERE player = 'Hasan';")
    print(f"Wallet: ",tulos())
    dbHaku.execute("SELECT airport.name as 'Airport' FROM airport, game WHERE location = ident and player = 'Hasan';")
    print(f"Location: ",tulos())
    return
def SumTinWong():
    dbHaku.execute("SELECT player FROM game WHERE player = 'Sum Tin Wong';")
    print(f"Character: ",tulos())
    dbHaku.execute("SELECT wallet FROM game WHERE player = 'Sum Tin Wong';")
    print(f"Wallet: ",tulos())
    dbHaku.execute("SELECT airport.name as 'Airport' FROM airport, game WHERE location = ident and player = 'Sum Tin Wong';")
    print(f"Location: ",tulos())
    return

#INTRO?!?!? Tosi bad veri baad
game = input("Start the game? [Y/N] ")
if game == "Y" or game == "y":
    print("Welcome to Project Mars Demo!")
    time.sleep(1)
    print("You have three difficulties, each with a different character!")
    time.sleep(2)

    print("""
          1. Normal

          2. Hard

          3. Extreme!
    """)

    diff = input("Choose your difficulty: ")

    while diff != "1" or diff != "2" or diff != "3":

        if diff == "1":
            Yrjö()
            confirm = input("Do you want to continue? [Y/N] ")
            if confirm == "Y" or confirm == "y":
                break
            elif confirm == "N" or confirm == "n":
                diff = input("Choose your difficulty: ")
        elif diff == "2":
            Hasan()
            confirm = input("Do you want to continue? [Y/N] ")
            if confirm == "Y" or confirm == "y":
                break
            elif confirm == "N" or confirm == "n":
                diff = input("Choose your difficulty: ")

        elif diff == "3":
            SumTinWong()
            confirm = input("Do you want to continue? [Y/N] ")
            if confirm == "Y" or confirm == "y":
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
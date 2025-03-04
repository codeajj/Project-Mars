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
    selection = re.sub(r"[^a-zA-Z0-9 ]", "", str(ugly))
    return selection

#HAHMOT:
def Yrjö():
    dbHaku.execute("SELECT player FROM game WHERE player = 'Yrjö';")
    print(f"Character: ", tulos())
    dbHaku.execute("SELECT wallet FROM game WHERE player = 'Yrjö';")
    print(f"Wallet: ", tulos())
    dbHaku.execute("SELECT airport.name as 'Airport' FROM airport, game WHERE location = ident and player = 'Yrjö';")
    print(f"Location: ", tulos())
    return
def Hasan():
    dbHaku.execute("SELECT player FROM game WHERE player = 'Hasan';")
    print(f"Character: ", tulos())
    dbHaku.execute("SELECT wallet FROM game WHERE player = 'Hasan';")
    print(f"Wallet: ", tulos())
    dbHaku.execute("SELECT airport.name as 'Airport' FROM airport, game WHERE location = ident and player = 'Hasan';")
    print(f"Location: ", tulos())
    return
def SumTinWong():
    dbHaku.execute("SELECT player FROM game WHERE player = 'Sum Tin Wong';")
    print(f"Character: ", tulos())
    dbHaku.execute("SELECT wallet FROM game WHERE player = 'Sum Tin Wong';")
    print(f"Wallet: ", tulos())
    dbHaku.execute("SELECT airport.name as 'Airport' FROM airport, game WHERE location = ident and player = 'Sum Tin Wong';")
    print(f"Location: ", tulos())
    return

#INTRO?!?!? Tosi bad veri baad
print("Welcome to Mars Rush!")
time.sleep(1)
print("You have three characters to select with varying difficulties!")
time.sleep(3)

print("""
      1. Normal
      
      2. Hard
      
      3. Extreme!
""")

diff = input("Choose your difficulty: ")

if diff == "1" or "Normal" or "normal":
    Yrjö()

elif diff == "2" or "Hard" or "hard":
    Hasan()

elif diff == "3" or "Extreme" or "extreme":
    SumTinWong()
else:
    print("Error!")
    diff = input("Choose your difficulty: ")
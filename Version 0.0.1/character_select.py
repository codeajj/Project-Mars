import mysql.connector
import time

mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="test",
  database="project_mars"
)

dbHaku = mydb.cursor()
def tulos():
    selection = dbHaku.fetchall()
    return selection

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
    dbHaku.execute("SELECT player FROM game WHERE player = 'Yrjö';")
    print(tulos())
elif diff == "2" or "Hard" or "hard":
    dbHaku.execute("SELECT player FROM game WHERE player = 'Hasan';")
    print(tulos())
else:
    dbHaku.execute("SELECT player FROM game WHERE player = 'Sum Tin Wong';")
    print(tulos())
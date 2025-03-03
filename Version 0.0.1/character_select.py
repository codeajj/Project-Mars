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

#Printaa kolme hahmoa tietokannan sisältä näyttääkseen
dbHaku.execute("SELECT player FROM game;")
#name = input("Choose your character 1-3: ")
#dbHaku.execute(f"select {name}")

print("Welcome to Mars Rush!")
time.sleep(1)
print("You have three characters to select with varying difficulties!")
time.sleep(3)
print(tulos())
print("Choose your character out of these three difficulties!")

#ALKEELLINEN TESTI
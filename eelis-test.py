import mysql.connector
import re

mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="test",
  database="project_mars"
)

#tehdään hakuväline databaseen selvemmäksi
dbHaku = mydb.cursor()

#tehdään databasesta lukeminen selvemmäksi:
def tulos():
    ruma = dbHaku.fetchall()
    #poistetaan kaikki muut paitsi a-z krijaimet, A-Z kirjaimet ja 0-9 numerot
    kaunis = re.sub(r"[^a-zA-Z0-9 ]", "",str(ruma))
    return ruma

print("kerro haluamasi lentokentän ICAO koodi: ")
icao = input()

dbHaku.execute(f"select name,municipality from airport where gps_code like '{icao}'")
print(tulos())
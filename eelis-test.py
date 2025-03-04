import mysql.connector
import re

mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="test",
  database="project_mars"
)

#tehdään hakuväline databaseen selvemmäksi
dbSearch = mydb.cursor()

#tehdään databasesta lukeminen selvemmäksi:
def result():
    ugly = dbSearch.fetchall()
    #Poistaa kaiken paitsi 1 välilyönnin a-ö krijaimet, A_Z kirjaimet ,ison Ö:n, ison Ä:N, ruotsalainen å kirjain ,norjalainen ö kirjain, viivan
    beatiful = re.sub(r"[^\s+a-öA-ZÖÄåÅøØ-]", "",str(ugly))
    return beatiful

print("kerro haluamasi lentokentän ICAO koodi: ")
icao = "ENSS"
dbSearch.execute(f"select name,municipality from airport where gps_code like '{icao}'")
print(result())
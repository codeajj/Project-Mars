from functions import *

player = ""
player_has_gone_to_events = False
mars_condition = False


from flask import Flask

app = Flask(__name__)
@app.route('/')
def game():
    game_is_playable = True

    input("Start game?")
    if game == "Y" or game == "y":
        clear()
        print("Welcome to Project Mars Demo!")
        print("You have three difficulties, each with a different character!")

        print("""
              1. Normal
    
              2. Hard
    
              3. Extreme!
        """)

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)

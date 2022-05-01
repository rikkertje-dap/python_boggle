from flask import render_template
from flask import session
from config import app
from config import db

from model.dice import Dice
from model.game import Game
from model.player import Player
from model.word import Word

from controller.gamecontroller import gamecontroller
from controller.playercontroller import playercontroller

app.register_blueprint(gamecontroller)
app.register_blueprint(playercontroller)

@app.route('/')
def app_index():
    return render_template('home.html')

@app.route('/session')
def get_session():
    return str(session["player_id"]) + " | " + session["player_name"]

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', debug=True)

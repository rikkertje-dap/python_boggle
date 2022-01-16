from flask import render_template
from flask import Blueprint
from flask import session
from flask import redirect
from flask import url_for
from config import app
from config import db
from model.game import Game
from model.player import Player

gamecontroller = Blueprint('gamecontroller', __name__)

@app.route('/highscores', methods=['GET'])
def show_highscores():
    games = Game.query.all()
    return render_template('gamelist.html', games=Game.query.filter(Game.player_id == session["player_id"]))

@app.route('/games', methods=['GET'])
def show_games():
    return render_template('gamelist.html', games=Game.query.filter(Game.player_id == session["player_id"]))


@app.route('/game/<game_id>', methods=['GET'])
def show_game(game_id):
    game = Game.query.filter(Game.id == game_id).first()
    game.generate_board()
    return render_template('game.html', game=game)


@app.route('/game', methods=['GET'])
def new_game():
    game = Game(player_id=session["player_id"])
    db.session.add(game)
    db.session.commit()
    return redirect(url_for('show_games'))


def is_input_valid(game, player_input):
    is_valid = False
    if game.is_there_still_time():
        if game.is_input_connected(player_input):
            return True
    return is_valid

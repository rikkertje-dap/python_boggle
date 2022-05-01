from flask import render_template
from flask import Blueprint
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from config import app
from config import db
from model.game import Game
from model.word import Word
from datetime import datetime

gamecontroller = Blueprint('gamecontroller', __name__)

@app.route('/highscores', methods=['GET'])
def show_highscores():
    games = Game.query.all()
    return render_template('highscores.html', games=games, now=datetime.now())

@app.route('/games', methods=['GET'])
def show_games():
    return render_template('gamelist.html', games=Game.query.filter(Game.player_id == session["player_id"]), now=datetime.now())


@app.route('/game/<game_id>', methods=['GET'])
def show_game(game_id):
    session["current_x"] = ""
    session["current_y"] = ""
    session["current_input"] = ""
    session["current_letters"] = ""
    game = Game.query.filter(Game.id == game_id).first()
    game.generate_board()
    game.generate_word_list()
    if session.get("player_id") != None and game.player_id == session["player_id"]:
        return render_template('game.html', game=game, now=datetime.now())
    else:
        return render_template("error.html", message="You don't have the rights to play this game")


@app.route('/game/<game_id>/letter', methods=['GET'])
def submit_letter_for_game(game_id):

    prev_x = None
    prev_y = None

    if session["current_x"] != "" and session["current_y"] != "":
        prev_x = int(session["current_x"])
        prev_y = int(session["current_y"])

    session["current_x"] = request.args.get("x")
    session["current_y"] = request.args.get("y")

    current_input = ""
    current_letters = []

    game = Game.query.filter(Game.id == game_id).first()
    game.generate_board()
    game.generate_word_list()

    if session.get("player_id") != None and game.player_id == session["player_id"]:
        if session["current_input"]:
            current_input = str(session["current_input"])
        if session["current_letters"]:
            current_letters = session["current_letters"]

        session["current_input"] = game.submit_letter(current_input, current_letters,
                                                      int(session["current_x"]),
                                                      int(session["current_y"]),
                                                      prev_x, prev_y)
        if not session["current_letters"]:
            session["current_letters"] = [str(session["current_x"]) + str(session["current_y"])]
        else:
            session["current_letters"] += [(str(session["current_x"]) + str(session["current_y"]))]
        return render_template('game.html', game=game, now=datetime.now())
    else:
        return render_template("error.html", message="You don't have the rights to play this game")


@app.route('/game/<game_id>/clear', methods=['GET'])
def clear_current_input(game_id):
    session["current_x"] = ""
    session["current_y"] = ""
    session["current_input"] = ""
    session["current_letters"] = ""
    return show_game(game_id)


@app.route('/game/<game_id>/submit', methods=['GET'])
def submit_word(game_id):
    game = Game.query.filter(Game.id == game_id).first()
    game.generate_board()

    if session.get("player_id") != None and game.player_id == session["player_id"]:
        if game.is_there_still_time():
            if Word.is_valid_word(session["current_input"]):
                if not game.has_word_been_played(session["current_input"]):
                    word = Word(session["current_input"])
                    game.increase_score(word.score)
                    game.submit_word(word.word)
                    db.session.commit()

                    game.set_message("Nice one! You played \"" + session["current_input"] + "\" for " + str(word.score) + " points")
                else:
                    game.set_message(("Sorry, but you have already played the word \"" + session["current_input"]))
            else:
                game.set_message("Sorry, but \"" + session["current_input"] + "\" is not a valid word...\"")
        else:
            game.set_message("Sorry, but you are out of time. The Game is over...")

        return clear_current_input(game_id)
    else:
        return render_template("error.html", message="You don't have the rights to play this game")


@app.route('/game', methods=['GET'])
def new_game():
    game = Game(player_id=session["player_id"])
    db.session.add(game)
    db.session.commit()
    return redirect(url_for('show_games'))

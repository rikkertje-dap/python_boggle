from flask import render_template
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from config import app
from config import db
from model.player import Player


playercontroller = Blueprint('playercontroller', __name__)


@app.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    player = Player.query.filter(Player.name == request.form['name']).first()
    if player:
        if player.password == request.form['password']:
            session["player_id"] = player.id
            session["player_name"] = player.name
            return redirect(url_for('app_index'))
        else:
            return render_template('login.html', message="Incorrect password")
    else:
        return render_template('login.html', message="No user found")

@app.route('/logout', methods=['GET'])
def do_logout():
    session.pop("player_id")
    session.pop("player_name")
    return redirect(url_for('app_index'))


@app.route('/register', methods=['GET'])
def show_register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def do_register():
    db.session.add(Player(name=request.form['name'], password=request.form['password']))
    db.session.commit()
    return redirect(url_for('show_login'))

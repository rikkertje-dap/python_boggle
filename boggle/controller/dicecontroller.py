from flask import render_template
from flask import Blueprint
from config import app
from model.dice import Dice

dicecontroller = Blueprint('dicecontroller', __name__)


@app.route('/dice')
def dice_index():
    return render_template('dicelist.html', dices=Dice.query.all())
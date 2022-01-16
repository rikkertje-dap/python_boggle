from config import db as db


class Dice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    letters = db.Column(db.String(6), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Dice, self).__init__(**kwargs)

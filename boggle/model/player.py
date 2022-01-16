from config import db as db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
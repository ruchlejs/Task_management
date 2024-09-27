from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(32), nullable = False, unique = True)
    password = db.Column(db.String(128), nullable = False)

    def __repr__(self):
        return f'username : {self.username}'
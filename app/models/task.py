from .. import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(128), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name = "fk_task_user"), nullable = False)

    def __repr__(self):
        return f'task : {self.name}'
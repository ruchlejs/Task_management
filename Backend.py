from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt= Bcrypt()

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(128), nullable = False)

    def __repr__(self):
        return f'task : {self.name}'
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(32), nullable = False, unique = True)
    password = db.Column(db.String(128), nullable = False)

    def __repr__(self):
        return f'username : {self.username}'

SECRET_KEY = 'AAAA'

with app.app_context():
    db.create_all()

@app.route('/task', methods=['GET'])
def get_task():
    count = Task.query.count()
    if not count:
        return jsonify({"message":"liste vide"})
    else:
        tasks = Task.query.all()
        res = [ {"id":task.id, "task":task.name} for task in tasks]
        return jsonify(res)


@app.route('/task',methods=['POST'])
def post_task():
    task = request.form.get('task')

    if task:
        new_task = Task(name=task)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": f"Tâche '{task}' ajoutée avec succès"}), 201
    else:
        return jsonify({"error": "Aucune tâche spécifiée"}), 400

@app.route('/task/<int:task_id>',methods=['GET'])
def get_task_by_id(task_id):
    task = Task.query.get(task_id)

    if task:
        return jsonify(f"{task}"),200
        
    return jsonify({"error": "Tâche non trouvée"}), 404


@app.route('/task/<int:task_id>', methods=['PUT'])
def change_task_by_id(task_id):
    task = Task.query.get(task_id)
    new_name = request.form.get('task')
    if task and new_name:
        task.name = new_name
        db.session.commit()
        return jsonify({"message":f"task {task.id} change for {task.name}"}), 200

    return jsonify('error, unfined task'), 404

@app.route('/task/<int:task_id>', methods=['DELETE'])
def remove_task_by_id(task_id):
    task = Task.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify(f'tache {task_id} remove with success'), 200
    return jsonify({"error": f"can't find task with the id : {task_id}"})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ressource non trouvée"}), 404

@app.route('/task/search',methods=['GET'])
def search_task():
    name = request.args.get('q','')
    results = Task.query.filter(Task.name.ilike(f'%{name}%')).all()
    results_dict = [{
        "id": res.id,
        "name": res.name} for res in results]
    if results:
            return jsonify(results_dict), 200
    return jsonify('tache non trouvé'), 404




@app.route('/register', methods = ['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    if username and password:
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username,password=hash_password)
        db.session.add(user)
        db.session.commit()
        return jsonify ({"message" : f"successful register for {username}"}),201
    return jsonify({"error":"couldn't register"}),400


@app.route('/login', methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username:
        user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password,password):
            return jsonify({"message":f"successfully login as {username}"}), 201



if __name__ == '__main__':
    app.run(debug=True)


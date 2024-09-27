from flask import Blueprint, request, jsonify
from ..models import Task
from ..models import User
from .. import db

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/<int:user_id>/task', methods=['GET'])
def get_task(user_id):
    user=User.query.get(user_id)

    if not user:
        return jsonify({"error":"Not a valid user"})

    count = Task.query.filter_by(user_id=user.id).count()
    if not count:
        return jsonify({"message":"liste vide"})
    else:
        tasks = Task.query.all()
        res = [ {"id":task.id, "task":task.name} for task in tasks]
        return jsonify(res)


@task_bp.route('/<int:user_id>/task',methods=['POST'])
def post_task(user_id):
    task = request.form.get('task')
    user = User.query.get(user_id)

    if task and user:
        new_task = Task(name=task, user_id = user.id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": f"Tâche '{task}' ajoutée avec succès pour l'utilisateur {user.username}"}), 201
    else:
        return jsonify({"error": "Aucune tâche spécifiée"}), 400

@task_bp.route('/<int:user_id>/task/<int:task_id>',methods=['GET'])
def get_task_by_id(user_id, task_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error":"not a valid user"}), 400

    task = Task.query.get(task_id)

    if task:
        return jsonify(f"{task}"),200
        
    return jsonify({"error": "Tâche non trouvée"}), 404


@task_bp.route('/<int:user_id>/task/<int:task_id>', methods=['PUT'])
def change_task_by_id(user_id, task_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error":"not a valid user"}), 400

    task = Task.query.get(task_id)
    new_name = request.form.get('task')
    if task and new_name:
        task.name = new_name
        db.session.commit()
        return jsonify({"message":f"task {task.id} change for {task.name}"}), 200

    return jsonify('error, unfined task'), 404

@task_bp.route('/<int:user_id>/task/<int:task_id>', methods=['DELETE'])
def remove_task_by_id(user_id, task_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error":"not a valid user"}), 400    

    task = Task.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify(f'tache {task_id} remove with success'), 200
    return jsonify({"error": f"can't find task with the id : {task_id}"})


@task_bp.route('/<int:user_id>/task/search',methods=['GET'])
def search_task(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error":"not a valid user"}), 400
    
    name = request.args.get('q','')
    results = Task.query.filter(Task.user_id == user.id, Task.name.ilike(f'%{name}%')).all()
    results_dict = [{
        "id": res.id,
        "name": res.name} for res in results]
    if results:
            return jsonify(results_dict), 200
    return jsonify('tache non trouvé'), 404
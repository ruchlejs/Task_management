from flask import Blueprint,jsonify

error_bp = Blueprint('error_bp',__name__)

@error_bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ressource non trouvée"}), 404
from flask import jsonify

def init_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Ressource non trouvée"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Erreur interne du serveur"}), 500
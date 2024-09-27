from .task import task_bp
from .user import user_bp
from .error import error_bp

def init_routes(app):
    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(error_bp)
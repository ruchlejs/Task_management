from .task import task_bp
from .user import user_bp
from .error import init_error_handlers

def init_routes(app):
    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    init_error_handlers(app)
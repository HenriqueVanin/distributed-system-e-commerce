from flask import Flask
from "./principal.py" import principal_bp
from "./sseServer.py" import sse_bp
from "./storage.py" import storage_bp

def create_app():
    """
    Cria e configura o aplicativo Flask.
    """
    app = Flask(__name__)

    # Registro de Blueprints
    app.register_blueprint(sse_bp, url_prefix="/sse")
    app.register_blueprint(principal_bp, url_prefix="/principal")
    app.register_blueprint(storage_bp, url_prefix="/storage")

    return app
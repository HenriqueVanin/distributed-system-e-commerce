from flask import Flask
from principal import principal_bp
from storage import storage_bp
from flask_cors import CORS
def create_app():
    """
    Cria e configura o aplicativo Flask.
    """
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para o app Flask

    cors = CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173"]  # Adicione aqui os outros hosts ou portas
        }
    })
    # Registro de Blueprints
    app.register_blueprint(principal_bp, url_prefix="/principal")
    app.register_blueprint(storage_bp, url_prefix="/storage")

    return app
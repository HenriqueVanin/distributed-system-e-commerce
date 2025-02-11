from flask import Flask
from flask_cors import CORS 
from flask_sse import sse
from flask import request, jsonify
import requests
import pika
import threading
import json
from payment import payment, start_payment_thread
from principal import principal, start_principal_thread
from storage import storage, start_storage_thread
from deliver import deliver, start_deliver_thread
from webhook import webhook, start_webhook_thread

app = Flask(__name__)

CORS(app)  # Habilita CORS para o app Flask

cors = CORS(app, origins="http://localhost:5173")


# Registrar os Blueprints
app.register_blueprint(payment, url_prefix='/payment')
app.register_blueprint(principal, url_prefix='/principal')
app.register_blueprint(storage, url_prefix='/storage')
app.register_blueprint(deliver, url_prefix='/deliver')

app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix='/stream')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    message = data.get('message', 'Sem mensagem')
    sse.publish({"message": f"{message}"}, type='new_message')

    return jsonify({"status": "Mensagem recebida!", "message": message}), 200

# Callback para processar mensagens da fila Pedidos_Criados


def start_all_threads():
    #start_consumer_thread()
    start_principal_thread()
    start_payment_thread()
    start_deliver_thread()
    start_storage_thread()
    start_webhook_thread()
   
if __name__ == '__main__':
    start_all_threads()
    app.run(debug=True, threaded=True)

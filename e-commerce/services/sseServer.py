from flask import Flask, request, jsonify
from flask_sse import sse
from flask_cors import CORS  # Importa o CORS
from redis import Redis

app = Flask(__name__)
CORS(app)  # Habilita CORS para o app Flask

cors = CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"]  # Adicione aqui os outros hosts ou portas
    }
})

app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix='/stream')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    message = data.get('message', 'Sem mensagem')
    sse.publish({"message": message}, type='new_message')

    return jsonify({"status": "Mensagem recebida!", "message": message}), 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

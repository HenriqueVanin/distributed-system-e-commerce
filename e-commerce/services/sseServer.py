from flask import Flask, request, jsonify
from flask_sse import sse
from flask_cors import CORS  # Importa o CORS
from redis import Redis
import threading

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

# Callback para processar mensagens da fila requests_Criados
def on_request_pagamento_alterado(ch, method, properties, body):
    request = json.loads(body)
    print(f"request recebido: {request}")

    url = 'http://127.0.0.1:5000/stream'
    payload = {'status': request.status, 'message': request.message}  # Dados a serem enviados
    resposta = requests.post(url, json=payload)  # Faz a requisição HTTP com JSON
    return jsonify({'mensagem': request.message})
   
# Consumidor para a fila requests_Criados
def consume_pagamentos_requests():
    channel = get_channel()

    # Declara a fila requests_Criados
    channel.queue_declare(queue='requests_Enviados')
    channel.queue_declare(queue='Pagamentos_Aprovados')
    channel.queue_declare(queue='Pagamentos_Recusados')

    # Configura o consumidor
    channel.basic_consume(queue='requests_Enviados', on_message_callback=on_request_pagamento_alterado)
    channel.basic_consume(queue='Pagamentos_Aprovados', on_message_callback=on_request_pagamento_alterado)
    channel.basic_consume(queue='Pagamentos_Recusados', on_message_callback=on_request_pagamento_alterado)

    print('Esperando por requests criados...')
    channel.start_consuming()

if __name__ == '__main__':
    # Iniciar o consumidor em um thread separado
    threading.Thread(target=consume_pagamentos_requests, daemon=True).start()

    # Iniciar o Flask
    app.run(debug=True, threaded=True)
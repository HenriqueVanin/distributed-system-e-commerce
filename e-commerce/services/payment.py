from pydantic import BaseModel
from flask import Flask, request
import asyncio
import pika
import json

# Simulação de mensagens publicadas em um sistema de mensageria
# mensageria = {"Pagamentos_Aprovados": [], "Pagamentos_Recusados": []}

class PagamentoWebhook(BaseModel):
    request_id: str
    status: str  # "aprovado" ou "recusado"

app = Flask(__name__)

# Configuração do RabbitMQ
def get_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    return connection.channel()

# Função para publicar eventos
def publish_event(topic, message):
    channel = get_channel()
    channel.queue_declare(queue=topic)  # Declara a fila, se ainda não existir
    channel.basic_publish(
        exchange='',
        routing_key=topic,
        body=json.dumps(message)
    )
    print(f"Evento publicado em {topic}: {message}")

# Callback para processar mensagens da fila requests_Criados
def on_created_request(ch, method, properties, body):
    request = json.loads(body)
    print(f"request recebido: {request}")

    if request.status == 'aprovado':
        publish_event('Pagamentos_Aprovados', request)
    else:
        publish_event('Pagamentos_Recusados', request)

    # Confirma o processamento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consumidor para a fila requests_Criados
def consume_created_requests():
    channel = get_channel()

    # Declara a fila requests_Criados
    channel.queue_declare(queue='requests_Criados')

    # Configura o consumidor
    channel.basic_consume(queue='requests_Criados', on_message_callback=on_created_request)

    print('Esperando por requests criados...')
    channel.start_consuming()

# Endpoint para o webhook de pagamento
@app.route('/webhook_payment', methods=['POST'])
async def webhook_payment():
    payment = request.json
    if payment['status'] == 'aprovado':
        publish_event('Pagamentos_Aprovados', payment)
        return 'Pagamento processado', 200
    elif payment['status'] == 'recusado':
        publish_event('Pagamentos_Recusados', payment)
        return 'Pagamento processado', 200
    else:
        return 'Pagamento não processado', 400

if __name__ == '__main__':
    # Iniciar o consumidor em um thread separado
    import threading
    threading.Thread(target=consume_created_requests, daemon=True).start()

    # Iniciar o Flask
    app.run(debug=True)
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from flask import Flask, request
import asyncio
import pika
import json

# Simulação de mensagens publicadas em um sistema de mensageria
# mensageria = {"Pagamentos_Aprovados": [], "Pagamentos_Recusados": []}

class PagamentoWebhook(BaseModel):
    pedido_id: str
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

# Callback para processar mensagens da fila Pedidos_Criados
def on_pedido_criado(ch, method, properties, body):
    pedido = json.loads(body)
    print(f"Pedido recebido: {pedido}")

    if pedido.status == 'aprovado':
        publish_event('Pagamentos_Aprovados', pedido)
    else:
        publish_event('Pagamentos_Recusados', pedido)

    # Confirma o processamento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consumidor para a fila Pedidos_Criados
def consume_pedidos_criados():
    channel = get_channel()

    # Declara a fila Pedidos_Criados
    channel.queue_declare(queue='Pedidos_Criados')

    # Configura o consumidor
    channel.basic_consume(queue='Pedidos_Criados', on_message_callback=on_pedido_criado)

    print('Esperando por pedidos criados...')
    channel.start_consuming()

# Endpoint para o webhook de pagamento
@app.route('/webhook_pagamento', methods=['POST'])
async def webhook_pagamento():
    pagamento = request.json
    if pagamento['status'] == 'aprovado':
        publish_event('Pagamentos_Aprovados', pagamento)
        return 'Pagamento processado', 200
    elif pagamento['status'] == 'recusado':
        publish_event('Pagamentos_Recusados', pagamento)
        return 'Pagamento processado', 200
    else:
        return 'Pagamento não processado', 400

if __name__ == '__main__':
    # Iniciar o consumidor em um thread separado
    import threading
    threading.Thread(target=consume_pedidos_criados, daemon=True).start()

    # Iniciar o Flask
    app.run(debug=True)
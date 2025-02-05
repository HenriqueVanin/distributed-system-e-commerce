from pydantic import BaseModel
from flask import Flask, request, Blueprint
import asyncio
import pika
import json
import threading
import random
import time

payment = Blueprint('payment', __name__)

# Simulação de mensagens publicadas em um sistema de mensageria
# mensageria = {"Pagamentos_Aprovados": [], "Pagamentos_Recusados": []}

class PagamentoWebhook(BaseModel):
    request_id: str
    status: str  # "aprovado" ou "recusado"

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
def on_created_request(ch, method, properties, body):
    print(f"request recebido: {body}")
    if not body:
        print("Erro: Corpo vazio!")
        return
    
    try:
        request = json.loads(body)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return
    
    print("Request recebido:", request)
    request["status"] = "enviado"
    publish_event('Pedidos_Enviados', request)
    time.sleep(10)
    if random.choice([True, False]):
        request["status"] = "aprovado"
        publish_event('Pagamentos_Aprovados', request)
    else:
        request["status"] = "recusado"
        publish_event('Pagamentos_Recusados', request)

# Consumidor para a fila Pedidos_Criados
def consume_created_requests():
    channel = get_channel()

    # Declara a fila Pedidos_Criados
    channel.queue_declare(queue='Pedidos_Criados')

    # Configura o consumidor
    channel.basic_consume(queue='Pedidos_Criados', on_message_callback=on_created_request, auto_ack=True)

    print('Esperando por requests criados...')
    channel.start_consuming()



def start_payment_thread():
    threading.Thread(target=consume_created_requests, daemon=True).start()
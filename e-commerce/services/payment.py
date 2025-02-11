from pydantic import BaseModel
from flask import Flask, request, Blueprint
import asyncio
import pika
import json
import threading
import random
import time
from pika.exchange_type import ExchangeType

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
    channel.exchange_declare(exchange=topic, exchange_type=ExchangeType.fanout)
    try:
        channel.basic_publish(
            exchange=topic,
            routing_key='',
            body=json.dumps(message)
        )
        
    except pika.exceptions.UnroutableError:
        print("Erro: Mensagem não foi roteada para a fila!")
    except Exception as e:
        print("Erro inesperado:", e)

# Callback para processar mensagens da fila Pedidos_Criados
def on_created_request(ch, method, properties, body):
    if not body:
        print("Erro: Corpo vazio!")
        return
    try:
        request = json.loads(body)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return
    
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
    print("iniciado o consumidor de pagamentos")
    channel = get_channel()

    channel.exchange_declare(exchange='Pagamentos_Aprovados', exchange_type=ExchangeType.fanout) 
    channel.exchange_declare(exchange='Pagamentos_Recusados', exchange_type=ExchangeType.fanout) 
    queue = channel.queue_declare(queue='', exclusive=True)
    channel.queue_bind(exchange='Pagamentos_Aprovados', queue=queue.method.queue)
    channel.queue_bind(exchange='Pagamentos_Recusados', queue=queue.method.queue)

    channel.basic_consume(queue=queue.method.queue, on_message_callback=on_created_request, auto_ack=True)

    #print('Esperando por requests criados...')
    channel.start_consuming()



def start_payment_thread():
    threading.Thread(target=consume_created_requests, daemon=True).start()
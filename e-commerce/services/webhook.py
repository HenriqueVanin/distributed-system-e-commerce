from flask import Flask, Blueprint
from flask_cors import CORS 
from flask_sse import sse
from flask import request, jsonify
import requests
import pika
import threading
import json
from pika.exchange_type import ExchangeType


webhook = Blueprint('webhook', __name__)

def on_request_payment_changed(ch, method, properties, body):
    
    if not body:
        print("Erro: mensagem vazia recebida!")
        return 
    try:
        request = json.loads(body)
        url = 'http://localhost:5000/webhook'
        payload = {
            'message': json.dumps(request)
        }  # Dados a serem enviados
        resposta = requests.post(url, json=payload)  # Faz a requisição HTTP com JSON
        message = payload.get('message', 'Mensagem não encontrada')
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return  # Caso haja erro de JSON, não tente processar        
    
   
# Consumidor para a fila Pedidos_Criados
def consume_pagamentos_requests():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='Pedidos_Enviados', exchange_type=ExchangeType.fanout)
    channel.exchange_declare(exchange='Pagamentos_Aprovados', exchange_type=ExchangeType.fanout) 
    channel.exchange_declare(exchange='Pagamentos_Recusados', exchange_type=ExchangeType.fanout)
    channel.exchange_declare(exchange='Pedidos_Criados', exchange_type=ExchangeType.fanout) 
    channel.exchange_declare(exchange='Pedidos_Excluidos', exchange_type=ExchangeType.fanout)  
    queue = channel.queue_declare(queue='', exclusive=True)
    channel.queue_bind(exchange='Pedidos_Enviados', queue=queue.method.queue)
    channel.queue_bind(exchange='Pagamentos_Recusados', queue=queue.method.queue)
    channel.queue_bind(exchange='Pagamentos_Aprovados', queue=queue.method.queue)
    channel.queue_bind(exchange='Pedidos_Criados', queue=queue.method.queue)
    channel.queue_bind(exchange='Pedidos_Excluidos', queue=queue.method.queue)

    channel.basic_consume(queue=queue.method.queue, on_message_callback=on_request_payment_changed, auto_ack=True)
    channel.start_consuming()

def start_webhook_thread():
    threading.Thread(target=consume_pagamentos_requests, daemon=True).start()

from flask import Flask, Blueprint
from flask_cors import CORS 
from flask_sse import sse
from flask import request, jsonify
import requests
import pika
import threading
import json


webhook = Blueprint('webhook', __name__)

def on_request_pagamento_alterado(ch, method, properties, body):
    print("ENTROU NO WEBHOOK")
    if not body:
        print("Erro: mensagem vazia recebida!")
        return  # Não processa se o corpo da mensagem estiver vazio
    try:
        request = json.loads(body)
        print(f"request recebido sse: {request}")

        url = 'http://localhost:5000/webhook'
        payload = {'message': request['status']}  # Dados a serem enviados
        resposta = requests.post(url, json=payload)  # Faz a requisição HTTP com JSON
        print(payload)
        message = payload.get('message', 'Mensagem não encontrada')
        print(f"Mensagem: {message}")
        # Garantir que o contexto do Flask esteja disponível
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return  # Caso haja erro de JSON, não tente processar        
    
   
# Consumidor para a fila Pedidos_Criados
def consume_pagamentos_requests():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # Declarar filas
    channel.queue_declare(queue='Pagamentos_Aprovados')
    channel.queue_declare(queue='Pagamentos_Recusados')
    channel.queue_declare(queue='Pedidos_Enviados')
    channel.queue_declare(queue='Pedidos_Criados')

    # Configurar consumidores
    channel.basic_consume(queue='Pedidos_Criados', on_message_callback=on_request_pagamento_alterado, auto_ack=True)
    channel.basic_consume(queue='Pagamentos_Aprovados', on_message_callback=on_request_pagamento_alterado, auto_ack=True)
    channel.basic_consume(queue='Pagamentos_Recusados', on_message_callback=on_request_pagamento_alterado, auto_ack=True)
    channel.basic_consume(queue='Pedidos_Enviados', on_message_callback=on_request_pagamento_alterado, auto_ack=True)

    print('Esperando por requests/pagamentos criados...')
    channel.start_consuming()

def start_webhook_thread():
    threading.Thread(target=consume_pagamentos_requests, daemon=True).start()

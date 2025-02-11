from pydantic import BaseModel
from flask import Flask, request, Blueprint, jsonify
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
        print("Erro inesperado no pagamento:", e)
    

@payment.route('/webhook', methods=['POST'])
def webhook():
    # Verifica se o conteúdo da requisição é JSON
    if request.is_json:
        data = request.get_json()  
        status = data.get("status")
        if status == "aprovado":
            data["status"] = "aprovado"
            publish_event('Pagamentos_Aprovados', data)
        else:
            data["status"] = "recusado"
            publish_event('Pagamentos_Recusados', data)
        return jsonify(data), 200  
    else:
        return jsonify({"error": "Formato inválido, JSON esperado"}), 400
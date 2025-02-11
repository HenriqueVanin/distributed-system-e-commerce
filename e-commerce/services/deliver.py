from pydantic import BaseModel
import asyncio
import pika
import json
from flask import Blueprint
import threading
from pika.exchange_type import ExchangeType
import time

deliver = Blueprint('deliver', __name__)
class requestEntrega(BaseModel):
    request_id: str

def on_aproved_payment(ch, method, properties, body):
    pagamento = json.loads(body)
    time.sleep(2)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='Pedidos_Enviados', exchange_type=ExchangeType.fanout)
    try:
        pagamento['status'] = "enviado"
        channel.basic_publish(
            exchange='Pedidos_Enviados',
            routing_key='',
            body=json.dumps(pagamento)
        )
        
    except pika.exceptions.UnroutableError:
        print("Erro: Mensagem não foi roteada para a fila!")
    except Exception as e:
        print("Erro inesperado na entrega:", e)

def consume_aproved_payment():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='Pagamentos_Aprovados', exchange_type=ExchangeType.fanout) 
    queue = channel.queue_declare(queue='', exclusive=True)
    channel.queue_bind(exchange='Pagamentos_Aprovados', queue=queue.method.queue)

    channel.basic_consume(queue=queue.method.queue, on_message_callback=on_aproved_payment, auto_ack=True)

    #print('Esperando por pagamentos aprovados...')
    channel.start_consuming()

def start_deliver_thread():
    threading.Thread(target=consume_aproved_payment, daemon=True).start()
from pydantic import BaseModel
import asyncio
import pika
import json


# Simulação de mensagens publicadas em um sistema de mensageria
# mensageria = {"requests_Enviados": []}
# fila_pagamentos_aprovados = []

class requestEntrega(BaseModel):
    request_id: str

def on_aproved_payment(ch, method, properties, body):
    pagamento = json.loads(body)
    print(f"Pagamento aprovado: {pagamento}")
    
    # Simula a emissão de nota e envio do request
    sent_request = {
        "request_id": pagamento['request_id'],
        "status": "enviado",
        "nota_fiscal": f"NF-{pagamento['request_id']}"
    }

    # Publica no tópico requests_Enviados
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='requests_Enviados', exchange_type='fanout')

    # Publica o evento
    channel.basic_publish(
        exchange='requests_Enviados',
        routing_key='',
        body=json.dumps(sent_request)
    )

    print(f"request enviado: {sent_request}")

    # Confirma o processamento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_aproved_payment():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declara a fila para Pagamentos_Aprovados
    channel.queue_declare(queue='Pagamentos_Aprovados')

    # Configura o consumidor
    channel.basic_consume(queue='Pagamentos_Aprovados', on_message_callback=on_aproved_payment)

    print('Esperando por pagamentos aprovados...')
    channel.start_consuming()

consume_aproved_payment()



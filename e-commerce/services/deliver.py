from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import pika
import json

app = FastAPI()

# Simulação de mensagens publicadas em um sistema de mensageria
# mensageria = {"Pedidos_Enviados": []}
# fila_pagamentos_aprovados = []

class PedidoEntrega(BaseModel):
    pedido_id: str

def on_pagamento_aprovado(ch, method, properties, body):
    pagamento = json.loads(body)
    print(f"Pagamento aprovado: {pagamento}")
    
    # Simula a emissão de nota e envio do pedido
    pedido_enviado = {
        "pedido_id": pagamento['pedido_id'],
        "status": "enviado",
        "nota_fiscal": f"NF-{pagamento['pedido_id']}"
    }

    # Publica no tópico Pedidos_Enviados
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='Pedidos_Enviados', exchange_type='fanout')

    # Publica o evento
    channel.basic_publish(
        exchange='Pedidos_Enviados',
        routing_key='',
        body=json.dumps(pedido_enviado)
    )

    print(f"Pedido enviado: {pedido_enviado}")

    # Confirma o processamento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_pagamento_aprovado():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declara a fila para Pagamentos_Aprovados
    channel.queue_declare(queue='Pagamentos_Aprovados')

    # Configura o consumidor
    channel.basic_consume(queue='Pagamentos_Aprovados', on_message_callback=on_pagamento_aprovado)

    print('Esperando por pagamentos aprovados...')
    channel.start_consuming()

consume_pagamento_aprovado()



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import pika
import json

app = FastAPI()

# # Simulação de tópicos de mensageria
# mensageria = {"requests_Criados": [], "requests_Excluídos": []}

# Banco de dados simulado de estoque
storage_db = {
    "produto_1": 100,
    "produto_2": 50,
    "produto_3": 75
}

# Modelos de dados
class request(BaseModel):
    request_id: str
    itens: list  # [{"product_id": "produto_1", "quantity": 2}, ...]

def on_created_request(ch, method, properties, body):
    request = json.loads(body)
    for item in request.itens:
        product_id = item["product_id"]
        quantity = item["quantity"]
        if product_id not in storage_db or storage_db[product_id] < quantity:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        storage_db[product_id] -= quantity

    print(f"request excluído: {request}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_removed_request(ch, method, properties, body):
    request = json.loads(body)
    for item in request.itens:
        product_id = item["product_id"]
        quantity = item["quantity"]
        if product_id not in storage_db:
            raise HTTPException(status_code=404, detail="Produto não encontrado no estoque")
        storage_db[product_id] += quantity
    print(f"request excluído: {request}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_requests():
    try:
        # Conexão com o RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declaração das filas
        channel.queue_declare(queue='requests_Criados', durable=True)
        channel.queue_declare(queue='requests_Excluidos', durable=True)

        # Configuração de consumo
        channel.basic_consume(queue='requests_Criados', on_message_callback=on_created_request)
        channel.basic_consume(queue='requests_Excluidos', on_message_callback=on_removed_request)

        print('Esperando por requests...')
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Encerrando consumidor...")
        if 'connection' in locals():
            connection.close()

consume_requests()

# @app.get("/estoque")
# async def consultar_estoque():
#     return storage_db

# @app.get("/mensageria")
# async def consultar_mensageria():
#     return mensageria
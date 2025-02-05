from pydantic import BaseModel
import asyncio
import pika
import json
from flask import Blueprint
import threading


storage = Blueprint("storage", __name__)


storage_db = [{'id': "fennec", "name": "Fennec", "price": '800', "imgSrc": "public/fennec.jpg", "quantity": '5'},
              {'id': "octane", "name": "Octane", "price": '10', "imgSrc": "public/octane.jpg", "quantity": '15'},
              {'id': "merc", "name": "Merc", "price": '300', "imgSrc": "public/merc.jpg", "quantity": '100'},
              {'id': "shokunin", "name": "Shokunin", "price": '1000', "imgSrc": "public/shokunin.jpg", "quantity": '55'}]

# # Simulação de tópicos de mensageria
# mensageria = {"Pedidos_Criados": [], "Pedidos_Excluídos": []}

# Banco de dados simulado de estoque

# Modelos de dados
class request(BaseModel):
    request_id: str
    products: list  # [{"product_id": "produto_1", "quantity": 2}, ...]
    created_at: str
    status: str

def on_created_request(ch, method, properties, body):
    if not body:
        print("Erro: Corpo vazio!")
        return
    
    try:
        request = json.loads(body)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return
    
    print("Request recebido:", request)
    for item in request['products']:
        product_id = item["product_id"]
        quantity = item["quantity"]
        if product_id not in storage_db or storage_db[product_id] < quantity:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        storage_db[product_id] -= quantity

    print(f"request excluído: {request}")
    #ch.basic_ack(delivery_tag=method.delivery_tag)

def on_removed_request(ch, method, properties, body):
    request = json.loads(body)
    for item in request['products']:
        product_id = item["product_id"]
        quantity = item["quantity"]
        if product_id not in storage_db:
            raise HTTPException(status_code=404, detail="Produto não encontrado no estoque")
        storage_db[product_id] += quantity
    print(f"request excluído: {request}")
    #ch.basic_ack(delivery_tag=method.delivery_tag)

@storage.get("/check_storage")
async def check_storage():
    """
    Rota para consultar o estoque.
    """
    return storage_db

def consume_requests():
    try:
        # Conexão com o RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declaração das filas
        channel.queue_declare(queue='Pedidos_Criados', durable=False)
        channel.queue_declare(queue='requests_Excluidos', durable=False)

        # Configuração de consumo
        channel.basic_consume(queue='Pedidos_Criados', on_message_callback=on_created_request, auto_ack=True)
        channel.basic_consume(queue='requests_Excluidos', on_message_callback=on_removed_request, auto_ack=True)

        print('Esperando por requests...')
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Encerrando consumidor...")
        if 'connection' in locals():
            connection.close()

def start_storage_thread():
    threading.Thread(target=consume_requests, daemon=True).start()

from pydantic import BaseModel
import asyncio
import pika
import json
from flask import Blueprint
import threading
from pika.exchange_type import ExchangeType


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
        products = request['products']
        for item in products:
            product_id = item["id"]
            quantity = item["quantity"]
            # Encontrar o índice do produto no array de estoque
            index = -1
            for i, p in enumerate(storage_db):
                if p["id"] == product_id:
                    index = i
                    break
            if(request['status']=='criado'):
                if index == -1 or (int(storage_db[index]["quantity"]) < int(quantity)):
                    print("Estoque insuficiente")
                
                newQuantity = int(storage_db[index]["quantity"]) - int(quantity)
            elif(request['status']=='excluido'): 
                if index == -1:
                    print("Produto não encontrado")
                
                newQuantity = int(storage_db[index]["quantity"]) + int(quantity)
            storage_db[index]["quantity"] = str(newQuantity)
       
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return
    
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
        channel.exchange_declare(exchange='Pedidos_Criados', exchange_type=ExchangeType.fanout) 
        channel.exchange_declare(exchange='Pedidos_Excluidos', exchange_type=ExchangeType.fanout) 
        queue = channel.queue_declare(queue='', exclusive=True)
        channel.queue_bind(exchange='Pedidos_Criados', queue=queue.method.queue)
        channel.queue_bind(exchange='Pedidos_Excluidos', queue=queue.method.queue)
        channel.basic_consume(queue=queue.method.queue, on_message_callback=on_created_request, auto_ack=True)
      
        channel.start_consuming()
    except KeyboardInterrupt:
       #print("Encerrando consumidor...")
        if 'connection' in locals():
            connection.close()

def start_storage_thread():
    threading.Thread(target=consume_requests, daemon=True).start()

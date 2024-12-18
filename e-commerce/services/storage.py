from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import pika
import json

app = FastAPI()

# # Simulação de tópicos de mensageria
# mensageria = {"Pedidos_Criados": [], "Pedidos_Excluídos": []}

# Banco de dados simulado de estoque
estoque_db = {
    "produto_1": 100,
    "produto_2": 50,
    "produto_3": 75
}

# Modelos de dados
class Pedido(BaseModel):
    pedido_id: str
    itens: list  # [{"produto_id": "produto_1", "quantidade": 2}, ...]

def on_pedido_criado(ch, method, properties, body):
    pedido = json.loads(body)
    for item in pedido.itens:
        produto_id = item["produto_id"]
        quantidade = item["quantidade"]
        if produto_id not in estoque_db or estoque_db[produto_id] < quantidade:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        estoque_db[produto_id] -= quantidade

    print(f"Pedido excluído: {pedido}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_pedido_excluido(ch, method, properties, body):
    pedido = json.loads(body)
    for item in pedido.itens:
        produto_id = item["produto_id"]
        quantidade = item["quantidade"]
        if produto_id not in estoque_db:
            raise HTTPException(status_code=404, detail="Produto não encontrado no estoque")
        estoque_db[produto_id] += quantidade
    print(f"Pedido excluído: {pedido}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consome_pedidos():
    try:
        # Conexão com o RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declaração das filas
        channel.queue_declare(queue='Pedidos_Criados', durable=True)
        channel.queue_declare(queue='Pedidos_Excluidos', durable=True)

        # Configuração de consumo
        channel.basic_consume(queue='Pedidos_Criados', on_message_callback=on_pedido_criado)
        channel.basic_consume(queue='Pedidos_Excluidos', on_message_callback=on_pedido_excluido)

        print('Esperando por pedidos...')
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Encerrando consumidor...")
        if 'connection' in locals():
            connection.close()

consome_pedidos()

# @app.get("/estoque")
# async def consultar_estoque():
#     return estoque_db

# @app.get("/mensageria")
# async def consultar_mensageria():
#     return mensageria
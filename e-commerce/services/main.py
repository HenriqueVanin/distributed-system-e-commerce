from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from flask import Flask, request, jsonify
import asyncio
import pika
import json
import threading

# app = FastAPI()

# Simulação de tópicos de mensageria
# mensageria = {
#     "Pedidos_Criados": [],
#     "Pedidos_Excluídos": [],
#     "Pagamentos_Aprovados": [],
#     "Pagamentos_Recusados": [],
#     "Pedidos_Enviados": []
# }

# # Modelos de dados
# class Pedido(BaseModel):
#     pedido_id: str
#     itens: list
#     valor_total: float

# class AtualizarPedido(BaseModel):
#     pedido_id: str
#     status: str  # Ex.: "enviado", "cancelado", "pago"

# # Banco de dados simulado de pedidos
# pedidos_db = {}

# @app.post("/pedidos")
# async def criar_pedido(pedido: Pedido):
#     if pedido.pedido_id in pedidos_db:
#         raise HTTPException(status_code=400, detail="Pedido já existe")
#     pedidos_db[pedido.pedido_id] = {"status": "criado", **pedido.dict()}
    
#     return {"message": "Pedido criado com sucesso"}

# @app.delete("/pedidos/{pedido_id}")
# async def excluir_pedido(pedido_id: str):
#     if pedido_id not in pedidos_db:
#         raise HTTPException(status_code=404, detail="Pedido não encontrado")
#     del pedidos_db[pedido_id]
    
#     return {"message": "Pedido excluído com sucesso"}

# @app.post("/eventos")
# async def receber_evento(evento: AtualizarPedido):
#     if evento.status == "pago":
#         pedidos_db[evento.pedido_id]["status"] = "pago"
#     elif evento.status == "cancelado":
#         pedidos_db[evento.pedido_id]["status"] = "cancelado"
#     elif evento.status == "enviado":
#         pedidos_db[evento.pedido_id]["status"] = "enviado"
#     else:
#         raise HTTPException(status_code=400, detail="Status inválido")
#     return {"message": f"Status do pedido {evento.pedido_id} atualizado"}

# @app.get("/pedidos/{pedido_id}")
# async def consultar_pedido(pedido_id: str):
#     if pedido_id not in pedidos_db:
#         raise HTTPException(status_code=404, detail="Pedido não encontrado")
#     return pedidos_db[pedido_id]

# @app.get("/mensageria")
# async def consultar_mensageria():
#     return mensageria

app = Flask(__name__)

# Banco de dados simulado
produtos = {"1": {"nome": "Produto 1", "preco": 100}, "2": {"nome": "Produto 2", "preco": 200}}
pedidos = {}

# Configuração do RabbitMQ
def get_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    return connection.channel()

# Publicar evento
def publish_event(topic, message):
    channel = get_channel()
    channel.queue_declare(queue=topic)
    channel.basic_publish(
        exchange='',
        routing_key=topic,
        body=json.dumps(message)
    )
    print(f"Evento publicado em {topic}: {message}")

# Callback para consumo de eventos
def on_pagamento_aprovado(ch, method, properties, body):
    evento = json.loads(body)
    pedido_id = evento.get("pedido_id")
    if pedido_id in pedidos:
        pedidos[pedido_id]["status"] = "pagamento aprovado"
        print(f"Pedido {pedido_id} atualizado para 'pagamento aprovado'")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_pagamento_recusado(ch, method, properties, body):
    evento = json.loads(body)
    pedido_id = evento.get("pedido_id")
    if pedido_id in pedidos:
        pedidos[pedido_id]["status"] = "pagamento recusado"
        publish_event('Pedidos_Excluídos', {"pedido_id": pedido_id})
        print(f"Pedido {pedido_id} atualizado para 'pagamento recusado' e publicado no tópico Pedidos_Excluídos")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_pedido_enviado(ch, method, properties, body):
    evento = json.loads(body)
    pedido_id = evento.get("pedido_id")
    if pedido_id in pedidos:
        pedidos[pedido_id]["status"] = "enviado"
        print(f"Pedido {pedido_id} atualizado para 'enviado'")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consumir eventos
def consume_events():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declarar filas
    channel.queue_declare(queue='Pagamentos_Aprovados')
    channel.queue_declare(queue='Pagamentos_Recusados')
    channel.queue_declare(queue='Pedidos_Enviados')

    # Configurar consumidores
    channel.basic_consume(queue='Pagamentos_Aprovados', on_message_callback=on_pagamento_aprovado)
    channel.basic_consume(queue='Pagamentos_Recusados', on_message_callback=on_pagamento_recusado)
    channel.basic_consume(queue='Pedidos_Enviados', on_message_callback=on_pedido_enviado)

    print("Consumindo eventos...")
    channel.start_consuming()

# Rotas da API REST
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(produtos)

@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    data = request.json
    pedido_id = str(len(pedidos) + 1)
    novo_pedido = {
        "pedido_id": pedido_id,
        "produtos": data.get("produtos", []),
        "status": "criado",
        "cliente": data.get("cliente"),
        "valor": sum(produtos[str(p)]["preco"] for p in data.get("produtos", []))
    }
    pedidos[pedido_id] = novo_pedido

    # Publicar evento no tópico Pedidos_Criados
    publish_event('Pedidos_Criados', novo_pedido)
    return jsonify(novo_pedido), 201

@app.route('/pedidos/<pedido_id>', methods=['DELETE'])
def excluir_pedido(pedido_id):
    if pedido_id in pedidos:
        pedido = pedidos.pop(pedido_id)
        pedido["status"] = "excluído"
        publish_event('Pedidos_Excluídos', pedido)
        return jsonify({"message": f"Pedido {pedido_id} excluído"}), 200
    else:
        return jsonify({"error": "Pedido não encontrado"}), 404

@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    return jsonify(pedidos)

if __name__ == '__main__':
    # Iniciar o consumidor em um thread separado
    threading.Thread(target=consume_events, daemon=True).start()

    # Iniciar o Flask
    app.run(debug=True)
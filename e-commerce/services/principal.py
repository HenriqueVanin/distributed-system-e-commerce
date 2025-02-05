from pydantic import BaseModel
from flask import Flask, request, jsonify, Blueprint, url_for, redirect
import asyncio
import pika
import json
import threading
from datetime import datetime
from flask_cors import CORS  # Importa o CORS

principal = Blueprint('principal', __name__)

def get_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    return connection.channel()

# Banco de dados simulado
cart = []
requests = []

# Publicar evento
def publish_event(topic, message):
    channel = get_channel()
    channel.queue_declare(queue=topic)
    channel.basic_publish(
        exchange='',
        routing_key=topic,
        body=json.dumps(message)
    )
    print(f"--------- Evento publicado em {topic}: {message}")

# Callback para consumo de eventos
def on_pagamento_aprovado(ch, method, properties, body):
    print(f"Mensagem recebida: {body}")
    if not body:
        print("Corpo vazio!")
        return

    try:
        evento = json.loads(body)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return
    request_id = evento.get("request_id")
    if request_id in requests:
        requests[request_id]["status"] = "pagamento aprovado"
        print(f"request {request_id} atualizado para 'pagamento aprovado'")

def on_pagamento_recusado(ch, method, properties, body):
    evento = json.loads(body)
    request_id = evento.get("request_id")
    if request_id in requests:
        requests[request_id]["status"] = "pagamento recusado"
        publish_event('Pedidos_Excluídos', {"request_id": request_id})
        print(f"request {request_id} atualizado para 'pagamento recusado' e publicado no tópico Pedidos_Excluídos")

def on_request_enviado(ch, method, properties, body):
    evento = json.loads(body)
    request_id = evento.get("request_id")
    if request_id in requests:
        requests[request_id]["status"] = "enviado"
        print(f"request {request_id} atualizado para 'enviado'")
    #ch.basic_ack(delivery_tag=method.delivery_tag)

# Consumir eventos
def consume_events():
    channel = get_channel()

    # Declarar filas
    channel.queue_declare(queue='Pagamentos_Aprovados', durable=False)
    channel.queue_declare(queue='Pagamentos_Recusados', durable=False)
    channel.queue_declare(queue='Pedidos_Enviados', durable=False)
    channel.queue_declare(queue='Pedidos_Criados', durable=False)


    # Configurar consumidores
    channel.basic_consume(queue='Pedidos_Criados', on_message_callback=on_pagamento_aprovado, auto_ack=True)
    channel.basic_consume(queue='Pagamentos_Aprovados', on_message_callback=on_pagamento_aprovado, auto_ack=True)
    channel.basic_consume(queue='Pagamentos_Recusados', on_message_callback=on_pagamento_recusado, auto_ack=True)
    channel.basic_consume(queue='Pedidos_Enviados', on_message_callback=on_request_enviado, auto_ack=True)

    print("Consumindo eventos...")
    channel.start_consuming()

# Rotas da API REST
@principal.route('/products', methods=['GET'])
def list_products():
    """
    Rota para listar products.
    """
    return jsonify(cart)

@principal.route('/products', methods=['POST'])
def create_product():
    """
    Rota para criar um novo produto.
    """
    data = request.json
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Dados inválidos. 'name' e 'price' são obrigatórios"}), 400

    novo_produto = {
        "id": data["id"],
        "name": data["name"],
        "price": data["price"],
        "quantity": data["quantity"],
    }
    cart.append(novo_produto)

    return jsonify({"message": "Produto criado com sucesso", "produto": {"nome": data["name"], "id": data["id"]}}), 201


@principal.route('/clear_products', methods=['POST'])
def clear_products():
    """
    Rota para limpar o carrinho de compras.
    """
    cart.clear()
    return jsonify({"message": "Carrinho de compras limpo com sucesso"}), 200

@principal.route('/products/<product_id>', methods=['DELETE'])
def remove_product(product_id):
    """
    Rota para remover um produto pelo seu ID.
    """
    # Procura o produto no cart
    for produto in cart:
        if produto["id"] == product_id:
            cart.remove(produto)  # Remove o produto do array
            return jsonify({
                "message": f"Produto {product_id} removido com sucesso.",
                "produto": produto
            }), 200

    # Caso o produto não seja encontrado
    return jsonify({"error": "Produto não encontrado."}), 404


@principal.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Rota para atualizar um produto pelo seu ID.
    """
    product_founded = next((produto for produto in cart if produto["id"] == product_id), None)

    if not product_founded:
        return jsonify({"error": "Produto não encontrado."}), 404

    data = request.json

    # Atualizar apenas os campos fornecidos
    if "quantity" in data:
        product_founded["quantity"] = data["quantity"]

    return jsonify({"message": f"Produto {product_id} atualizado com sucesso", "produto": product_founded}), 200


@principal.route('/requests', methods=['POST'])
def create_request():
    data = request.json
    request_id = str(len(requests) + 1)
    products = data.get("products", [])

    # Calculando o total corretamente
    total = 0
    new_request = {
        "request_id": request_id,
        "products": products,
        "status": "criado",
        "client_id": data.get("client_id"),
        "total": data.get("total"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    products = []

    requests.append(new_request)
    channel = get_channel()
    channel.queue_declare(queue='Pedidos_Criados')
    # Publicar evento no tópico Pedidos_Criados
    publish_event('Pedidos_Criados', new_request)
    return jsonify(new_request), 201

@principal.route('/requests/<request_id>', methods=['DELETE'])
def remove_request(request_id):
    if request_id in requests:
        request = requests.pop(request_id)
        request["status"] = "excluido"
        publish_event('Pedidos_Excluídos', request)
        return jsonify({"message": f"request {request_id} excluído"}), 200
    else:
        return jsonify({"error": "request não encontrado"}), 404

@principal.route('/requests', methods=['GET'])
def list_requests():
    return jsonify(requests)

@principal.get("/check_storage")
async def check_storage():
    """
    Rota para consultar o estoque.
    """
    check_storage_url = url_for("storage.check_storage")
    return redirect(check_storage_url)
def start_principal_thread():
    threading.Thread(target=consume_events, daemon=True).start()
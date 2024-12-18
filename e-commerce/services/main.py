from pydantic import BaseModel
from flask import Flask, request, jsonify
import asyncio
import pika
import json
import threading

app = Flask(__name__)

# Banco de dados simulado
cart = []
requests = []

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
    request_id = evento.get("request_id")
    if request_id in requests:
        requests[request_id]["status"] = "pagamento aprovado"
        print(f"request {request_id} atualizado para 'pagamento aprovado'")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_pagamento_recusado(ch, method, properties, body):
    evento = json.loads(body)
    request_id = evento.get("request_id")
    if request_id in requests:
        requests[request_id]["status"] = "pagamento recusado"
        publish_event('requests_Excluídos', {"request_id": request_id})
        print(f"request {request_id} atualizado para 'pagamento recusado' e publicado no tópico requests_Excluídos")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_request_enviado(ch, method, properties, body):
    evento = json.loads(body)
    request_id = evento.get("request_id")
    if request_id in requests:
        requests[request_id]["status"] = "enviado"
        print(f"request {request_id} atualizado para 'enviado'")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consumir eventos
def consume_events():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declarar filas
    channel.queue_declare(queue='Pagamentos_Aprovados')
    channel.queue_declare(queue='Pagamentos_Recusados')
    channel.queue_declare(queue='requests_Enviados')

    # Configurar consumidores
    channel.basic_consume(queue='Pagamentos_Aprovados', on_message_callback=on_pagamento_aprovado)
    channel.basic_consume(queue='Pagamentos_Recusados', on_message_callback=on_pagamento_recusado)
    channel.basic_consume(queue='requests_Enviados', on_message_callback=on_request_enviado)

    print("Consumindo eventos...")
    channel.start_consuming()

# Rotas da API REST
@app.route('/products', methods=['GET'])
def list_products():
    """
    Rota para listar products.
    """
    return jsonify(cart)

@app.route('/products', methods=['POST'])
def create_product():
    """
    Rota para criar um novo produto.
    """
    data = request.json
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Dados inválidos. 'name' e 'price' são obrigatórios"}), 400

    product_id = str(len(cart) + 1)  # Gera um novo ID para o produto
    novo_produto = {
        "id": data["id"],
        "name": data["name"],
        "price": data["price"]
    }
    cart.push(novo_produto)

    return jsonify({"message": "Produto criado com sucesso", "produto": {product_id: novo_produto}}), 201


@app.route('/products/<product_id>', methods=['DELETE'])
def remove_product(product_id):
    """
    Rota para remover um produto pelo seu ID.
    """
    if product_id in products:
        removed_product = products.pop(product_id)
        return jsonify({"message": f"Produto {product_id} removido com sucesso", "produto": removed_product}), 200
    else:
        return jsonify({"error": "Produto não encontrado"}), 404


@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Rota para atualizar um produto pelo seu ID.
    """
    if product_id not in cart:
        return jsonify({"error": "Produto não encontrado"}), 404

    data = request.json
    updated_product = cart[product_id]

    # Atualizar apenas os campos fornecidos
    if "name" in data:
        updated_product["name"] = data["name"]
    if "price" in data:
        updated_product["price"] = data["price"]

    return jsonify({"message": f"Produto {product_id} atualizado com sucesso", "produto": updated_product}), 200


@app.route('/requests', methods=['POST'])
def create_request():
    data = request.json
    request_id = str(len(requests) + 1)
    new_request = {
        "request_id": request_id,
        "products": data.get("products", []),
        "status": "criado",
        "client_id": data.get("client_id"),
        "total": sum(cart[str(p)]["price"] for p in data.get("products", []))
    }
    requests[request_id] = new_request

    # Publicar evento no tópico requests_Criados
    publish_event('requests_Criados', new_request)
    return jsonify(new_request), 201

@app.route('/requests/<request_id>', methods=['DELETE'])
def remove_request(request_id):
    if request_id in requests:
        request = requests.pop(request_id)
        request["status"] = "excluído"
        publish_event('requests_Excluídos', request)
        return jsonify({"message": f"request {request_id} excluído"}), 200
    else:
        return jsonify({"error": "request não encontrado"}), 404

@app.route('/requests', methods=['GET'])
def list_requests():
    return jsonify(requests)

if __name__ == '__main__':
    # Iniciar o consumidor em um thread separado
    threading.Thread(target=consume_events, daemon=True).start()

    # Iniciar o Flask
    app.run(debug=True)
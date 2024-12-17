from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Simulação de tópicos de mensageria
mensageria = {
    "Pedidos_Criados": [],
    "Pedidos_Excluídos": [],
    "Pagamentos_Aprovados": [],
    "Pagamentos_Recusados": [],
    "Pedidos_Enviados": []
}

# Modelos de dados
class Pedido(BaseModel):
    pedido_id: str
    itens: list
    valor_total: float

class AtualizarPedido(BaseModel):
    pedido_id: str
    status: str  # Ex.: "enviado", "cancelado", "pago"

# Banco de dados simulado de pedidos
pedidos_db = {}

@app.post("/pedidos")
async def criar_pedido(pedido: Pedido):
    if pedido.pedido_id in pedidos_db:
        raise HTTPException(status_code=400, detail="Pedido já existe")
    pedidos_db[pedido.pedido_id] = {"status": "criado", **pedido.dict()}
    mensageria["Pedidos_Criados"].append(pedido.dict())
    return {"message": "Pedido criado com sucesso"}

@app.delete("/pedidos/{pedido_id}")
async def excluir_pedido(pedido_id: str):
    if pedido_id not in pedidos_db:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    del pedidos_db[pedido_id]
    mensageria["Pedidos_Excluídos"].append({"pedido_id": pedido_id})
    return {"message": "Pedido excluído com sucesso"}

@app.post("/eventos")
async def receber_evento(evento: AtualizarPedido):
    if evento.status == "pago":
        pedidos_db[evento.pedido_id]["status"] = "pago"
    elif evento.status == "cancelado":
        pedidos_db[evento.pedido_id]["status"] = "cancelado"
    elif evento.status == "enviado":
        pedidos_db[evento.pedido_id]["status"] = "enviado"
    else:
        raise HTTPException(status_code=400, detail="Status inválido")
    return {"message": f"Status do pedido {evento.pedido_id} atualizado"}

@app.get("/pedidos/{pedido_id}")
async def consultar_pedido(pedido_id: str):
    if pedido_id not in pedidos_db:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedidos_db[pedido_id]

@app.get("/mensageria")
async def consultar_mensageria():
    return mensageria

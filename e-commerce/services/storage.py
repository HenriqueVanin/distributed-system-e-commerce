from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Simulação de tópicos de mensageria
mensageria = {"Pedidos_Criados": [], "Pedidos_Excluídos": []}

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

@app.post("/eventos/pedido-criado")
async def atualizar_estoque_criado(pedido: Pedido):
    for item in pedido.itens:
        produto_id = item["produto_id"]
        quantidade = item["quantidade"]
        if produto_id not in estoque_db or estoque_db[produto_id] < quantidade:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        estoque_db[produto_id] -= quantidade
    mensageria["Pedidos_Criados"].append(pedido.dict())
    return {"message": "Estoque atualizado para pedido criado"}

@app.post("/eventos/pedido-excluido")
async def atualizar_estoque_excluido(pedido: Pedido):
    for item in pedido.itens:
        produto_id = item["produto_id"]
        quantidade = item["quantidade"]
        if produto_id not in estoque_db:
            raise HTTPException(status_code=404, detail="Produto não encontrado no estoque")
        estoque_db[produto_id] += quantidade
    mensageria["Pedidos_Excluídos"].append(pedido.dict())
    return {"message": "Estoque restaurado para pedido excluído"}

@app.get("/estoque")
async def consultar_estoque():
    return estoque_db

@app.get("/mensageria")
async def consultar_mensageria():
    return mensageria

from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Simulação de mensagens publicadas em um sistema de mensageria
mensageria = {"Pedidos_Enviados": []}
fila_pagamentos_aprovados = []

class PedidoEntrega(BaseModel):
    pedido_id: str

@app.post("/pagamento-aprovado")
async def pagamento_aprovado(pedido: PedidoEntrega):
    fila_pagamentos_aprovados.append(pedido.dict())
    return {"message": "Pagamento aprovado recebido"}

async def processar_entregas():
    while True:
        if fila_pagamentos_aprovados:
            pedido = fila_pagamentos_aprovados.pop(0)
            mensageria["Pedidos_Enviados"].append(pedido)
            print(f"Pedido {pedido['pedido_id']} enviado!")
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(processar_entregas())

@app.get("/mensageria")
async def consultar_mensageria():
    return mensageria

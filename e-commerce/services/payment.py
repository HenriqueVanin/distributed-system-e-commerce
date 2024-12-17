from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Simulação de mensagens publicadas em um sistema de mensageria
mensageria = {"Pagamentos_Aprovados": [], "Pagamentos_Recusados": []}

class PagamentoWebhook(BaseModel):
    pedido_id: str
    status: str  # "aprovado" ou "recusado"

@app.post("/webhook/pagamento")
async def receber_webhook(pagamento: PagamentoWebhook):
    if pagamento.status == "aprovado":
        mensageria["Pagamentos_Aprovados"].append({"pedido_id": pagamento.pedido_id})
    elif pagamento.status == "recusado":
        mensageria["Pagamentos_Recusados"].append({"pedido_id": pagamento.pedido_id})
    else:
        raise HTTPException(status_code=400, detail="Status inválido")
    return {"message": "Pagamento processado com sucesso"}

@app.get("/mensageria")
async def consultar_mensageria():
    return mensageria

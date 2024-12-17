from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

fila_notificacoes = []

@app.post("/notificacao")
async def receber_evento(evento: dict):
    fila_notificacoes.append(evento)
    return {"message": "Evento recebido"}

async def stream_notificacoes():
    while True:
        if fila_notificacoes:
            evento = fila_notificacoes.pop(0)
            yield f"event: status_update\ndata: {json.dumps(evento)}\n\n"
        await asyncio.sleep(1)

@app.get("/stream")
async def stream_eventos():
    return StreamingResponse(stream_notificacoes(), media_type="text/event-stream")

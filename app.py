from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent.me import Me
import uvicorn

app = FastAPI()
me = Me()

class ChatRequest(BaseModel):
    message: str
    history: list

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    response = me.chat(req.message, req.history)
    return {"reply": response}

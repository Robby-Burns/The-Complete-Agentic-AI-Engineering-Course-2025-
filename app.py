import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

# --- WHY: Load configuration from environment ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

# Optional: support custom base URL if you ever proxy your LLM
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip() or None

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL) if OPENAI_BASE_URL \
         else OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/healthz")
def healthz():
    # --- WHY: For Kubernetes readiness/liveness probes ---
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    # --- WHY: Keep the endpoint focused; this is your agent's 'brain' entrypoint ---
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": req.message}]
    )
    return {"reply": resp.choices[0].message.content}

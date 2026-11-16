from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent import get_ai_response
from app.memory import memory

app = FastAPI(
    title="Advanced Voice AI Assistant",
    version="1.1.0"
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ClearMemoryRequest(BaseModel):
    session_id: str = "default"


@app.get("/")
def home():
    return {
        "message": "Voice AI Assistant is running",
        "status": "online"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        if not request.message.strip():
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        answer = get_ai_response(
            request.message,
            session_id=request.session_id
        )

        return {
            "response": answer,
            "session_id": request.session_id
        }

    except HTTPException:
        raise

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/clear-memory")
def clear_memory(request: ClearMemoryRequest):
    memory.clear_history(request.session_id)

    return {
        "message": "Conversation memory cleared successfully.",
        "session_id": request.session_id
    }

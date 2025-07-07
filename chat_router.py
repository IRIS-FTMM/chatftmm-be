# chat_router.py
from fastapi import APIRouter, HTTPException
from schemas import ChatRequest, ChatResponse
from chatbot import get_chatbot_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    try:
        response_text = get_chatbot_response(request.query)
        return ChatResponse(response=response_text)
    except Exception as e:
        print(f"API Error: {e}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan internal pada server.")
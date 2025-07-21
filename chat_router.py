# file: chat_router.py
from fastapi import APIRouter, HTTPException
from schemas import ChatRequest, ChatResponse
from chatbot import get_chatbot_response # <- PERUBAHAN: Impor dari chatbot.py

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    try:
        # Panggil alur kerja lengkap dari chatbot.py
        response_text = get_chatbot_response(request.query)
        return ChatResponse(response=response_text)
    except Exception as e:
        # Menambahkan log error yang lebih detail di backend
        print(f"API Error in chat_router: {type(e).__name__} - {e}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan internal pada server.")

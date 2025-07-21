# file: chat_router.py (PERBAIKAN FINAL DENGAN ROUTING FLEKSIBEL)

from fastapi import APIRouter, HTTPException
from schemas import ChatRequest, ChatResponse
from chatbot import get_chatbot_response

router = APIRouter()

# --- PERUBAHAN ADA DI SINI ---
# Kita mendaftarkan endpoint DUA KALI: satu tanpa slash, satu dengan slash.
# Keduanya akan menunjuk ke fungsi yang sama.
@router.post("/chat", response_model=ChatResponse, include_in_schema=False)
@router.post("/chat/", response_model=ChatResponse)
# -----------------------------
def handle_chat(request: ChatRequest):
    """
    Menangani permintaan chat dari pengguna dan mengembalikan respons dari chatbot.
    """
    try:
        response_text = get_chatbot_response(request.query)
        return ChatResponse(response=response_text)
    except Exception as e:
        print(f"API Error in chat_router: {type(e).__name__} - {e}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan internal pada server.")
from fastapi import APIRouter, HTTPException, Depends
import sys
import os

# 添加父目录到Python路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models import ChatMessage, ChatResponse, ClearResponse
from services.ai_service import AIService
from typing import Annotated

router = APIRouter(prefix="/chat", tags=["聊天"])

# 依赖注入：获取AI服务实例
def get_ai_service() -> AIService:
    return AIService()

@router.get("/")
async def health_check():
    """健康检查端点"""
    return {"message": "聊天服务运行正常"}

@router.post("/", response_model=ChatResponse)
async def chat(
    chat_message: ChatMessage,
    ai_service: Annotated[AIService, Depends(get_ai_service)]
):
    """
    处理用户聊天消息
    
    Args:
        chat_message: 用户消息
        ai_service: AI服务实例
    
    Returns:
        ChatResponse: 包含AI响应和对话历史
    """
    try:
        result = await ai_service.chat(chat_message.message)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear", response_model=ClearResponse)
async def clear_conversation(
    ai_service: Annotated[AIService, Depends(get_ai_service)]
):
    """
    清空对话历史
    
    Args:
        ai_service: AI服务实例
    
    Returns:
        ClearResponse: 清空确认消息
    """
    try:
        ai_service.clear_memory()
        return ClearResponse(message="对话历史已清空")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_conversation_history(
    ai_service: Annotated[AIService, Depends(get_ai_service)]
):
    """
    获取当前对话历史
    
    Args:
        ai_service: AI服务实例
    
    Returns:
        List[Dict]: 对话历史列表
    """
    try:
        history = ai_service.get_conversation_history()
        return {"conversation_history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    """聊天消息模型"""
    message: str

class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str
    conversation_history: List[dict]

class ClearResponse(BaseModel):
    """清空对话响应模型"""
    message: str 
"""
FastAPI 应用主文件
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

# 导入配置和Agent
from config import settings
from agent import AIAgent
from tools.base import ToolResult

# 数据模型
class ChatMessage(BaseModel):
    message: str
    use_tools: Optional[bool] = True

class ChatResponse(BaseModel):
    response: str
    conversation_history: List[dict]
    tools_used: Optional[List[dict]] = None

class ClearResponse(BaseModel):
    message: str

class ToolCall(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]

# 创建应用
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 设置JSON编码
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json

# 自定义JSON响应类
class UTF8JSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            separators=(",", ":"),
            default=str
        ).encode("utf-8")

# 设置默认响应类
app.default_response_class = UTF8JSONResponse

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局AI Agent实例
ai_agent = AIAgent()

@app.get("/")
async def root():
    return {
        "message": "智能对话Agent API 运行中",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chat-agent-api"}

@app.post("/chat/", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    try:
        # 添加日志查看接收到的消息
        print(f"收到用户消息: {chat_message.message}")
        print(f"消息类型: {type(chat_message.message)}")
        
        use_tools = chat_message.use_tools if chat_message.use_tools is not None else True
        result = await ai_agent.chat(chat_message.message, use_tools)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(chat_message: ChatMessage):
    """流式聊天端点"""
    try:
        # 添加日志查看接收到的消息
        print(f"[流式] 收到用户消息: {chat_message.message}")
        print(f"[流式] 消息类型: {type(chat_message.message)}")
        
        use_tools = chat_message.use_tools if chat_message.use_tools is not None else True
        return StreamingResponse(
            ai_agent.chat_stream(chat_message.message, use_tools),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/clear", response_model=ClearResponse)
async def clear_conversation():
    try:
        ai_agent.clear_memory()
        return ClearResponse(message="对话历史已清空")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history")
async def get_conversation_history():
    try:
        history = ai_agent.get_conversation_history()
        return {"conversation_history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools")
async def get_available_tools():
    """获取可用工具列表"""
    try:
        tools = ai_agent.tool_manager.get_available_tools()
        return {"tools": tools}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/execute")
async def execute_tool(tool_call: ToolCall):
    """执行工具"""
    try:
        result = await ai_agent.tool_manager.execute_tool(tool_call.tool_name, tool_call.parameters)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
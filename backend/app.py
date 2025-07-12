"""
简化的应用文件，避免相对导入问题
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory

# 加载环境变量
try:
    load_dotenv()
except UnicodeDecodeError as e:
    print(f"Error loading .env file: {e}")
    print("Please run fix_env.py to fix the encoding issue")
    raise
except Exception as e:
    print(f"Error loading .env file: {e}")
    print("Please check if .env file exists and has correct format")
    raise

# 数据模型
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    conversation_history: List[dict]

class ClearResponse(BaseModel):
    message: str

# 配置
class Settings:
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_TEMPERATURE: float = 0.7
    DEEPSEEK_MAX_TOKENS: int = 1000
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    @classmethod
    def validate_config(cls):
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DeepSeek API密钥未配置，请在.env文件中设置DEEPSEEK_API_KEY")

settings = Settings()

# AI服务类
class AIService:
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self._chat_model = None
    
    @property
    def chat_model(self):
        if self._chat_model is None:
            self._chat_model = ChatDeepSeek(
                model=settings.DEEPSEEK_MODEL,
                temperature=settings.DEEPSEEK_TEMPERATURE,
                max_tokens=settings.DEEPSEEK_MAX_TOKENS,
                api_key=settings.DEEPSEEK_API_KEY
            )
        return self._chat_model
    
    def _convert_messages_to_dict(self, messages: List) -> List[Dict[str, str]]:
        result = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})
        return result
    
    def _convert_memory_to_history(self) -> List[Dict[str, str]]:
        history = self.memory.chat_memory.messages
        return self._convert_messages_to_dict(history)
    
    async def chat(self, user_message: str) -> Dict[str, Any]:
        try:
            # 获取对话历史
            history = self.memory.chat_memory.messages
            
            # 构建完整的对话上下文
            context = ""
            for msg in history:
                if isinstance(msg, HumanMessage):
                    context += f"用户: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    context += f"助手: {msg.content}\n"
            
            # 添加当前用户消息
            context += f"用户: {user_message}\n助手:"
            
            # 调用ChatDeepSeek
            messages = [
                ("human", user_message)
            ]
            response = await self.chat_model.ainvoke(messages)
            ai_response = response.content
            
            # 保存到记忆
            self.memory.chat_memory.add_user_message(user_message)
            self.memory.chat_memory.add_ai_message(ai_response)
            
            # 获取更新后的对话历史
            conversation_history = self._convert_memory_to_history()
            
            return {
                "response": ai_response,
                "conversation_history": conversation_history
            }
        except Exception as e:
            raise Exception(f"AI服务处理错误: {str(e)}")
    
    def clear_memory(self):
        self.memory.clear()
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self._convert_memory_to_history()

# 创建应用
app = FastAPI(
    title="智能对话Agent API",
    description="基于DeepSeek API的智能对话助手",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局AI服务实例
ai_service = AIService()

# 验证配置
try:
    settings.validate_config()
except ValueError as e:
    print(f"配置错误: {e}")
    print("请在backend/.env文件中设置DEEPSEEK_API_KEY")

@app.get("/")
async def root():
    return {
        "message": "智能对话Agent API 运行中",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chat-agent-api"}

@app.post("/chat/", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    try:
        result = await ai_service.chat(chat_message.message)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/clear", response_model=ClearResponse)
async def clear_conversation():
    try:
        ai_service.clear_memory()
        return ClearResponse(message="对话历史已清空")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history")
async def get_conversation_history():
    try:
        history = ai_service.get_conversation_history()
        return {"conversation_history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
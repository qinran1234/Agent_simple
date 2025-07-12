from langchain_community.chat_models import ChatDeepSeek
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any
import sys
import os

# 添加父目录到Python路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config import settings

class AIService:
    """AI服务类，处理与DeepSeek API的交互"""
    
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self._chat_model = None
    
    @property
    def chat_model(self):
        """获取聊天模型实例（懒加载）"""
        if self._chat_model is None:
            self._chat_model = ChatDeepSeek(
                api_key=settings.DEEPSEEK_API_KEY,
                model=settings.DEEPSEEK_MODEL,
                temperature=settings.DEEPSEEK_TEMPERATURE,
                max_tokens=settings.DEEPSEEK_MAX_TOKENS
            )
        return self._chat_model
    
    def _convert_messages_to_dict(self, messages: List) -> List[Dict[str, str]]:
        """将LangChain消息转换为字典格式"""
        result = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})
        return result
    
    def _convert_memory_to_history(self) -> List[Dict[str, str]]:
        """将记忆转换为对话历史"""
        history = self.memory.chat_memory.messages
        return self._convert_messages_to_dict(history)
    
    async def chat(self, user_message: str) -> Dict[str, Any]:
        """处理用户消息并返回AI响应"""
        try:
            # 获取当前对话历史
            history = self._convert_memory_to_history()
            
            # 添加当前用户消息
            history.append({"role": "user", "content": user_message})
            
            # 调用AI API
            response = await self.chat_model.agenerate([history])
            
            # 获取AI响应
            ai_response = response.generations[0][0].text
            
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
        """清空对话记忆"""
        self.memory.clear()
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取当前对话历史"""
        return self._convert_memory_to_history() 
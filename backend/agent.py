"""
AI Agent 类
"""
import json
import asyncio
from typing import List, Dict, Any
from langchain_deepseek import ChatDeepSeek
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from tools.manager import ToolManager
from tools.base import ToolResult
from config import settings


class AIAgent:
    """AI智能助手"""
    
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self._chat_model = None
        self.tool_manager = ToolManager()
    
    @property
    def chat_model(self):
        """获取聊天模型"""
        if self._chat_model is None:
            self._chat_model = ChatDeepSeek(
                model=settings.DEEPSEEK_MODEL,
                temperature=settings.DEEPSEEK_TEMPERATURE,
                max_tokens=settings.DEEPSEEK_MAX_TOKENS,
                api_key=settings.DEEPSEEK_API_KEY
            )
        return self._chat_model
    
    def _convert_messages_to_dict(self, messages: List) -> List[Dict[str, str]]:
        """转换消息为字典格式"""
        result = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})
        return result
    
    def _convert_memory_to_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        history = self.memory.chat_memory.messages
        return self._convert_messages_to_dict(history)
    
    async def chat(self, user_message: str, use_tools: bool = True) -> Dict[str, Any]:
        """聊天方法"""
        try:
            # 获取对话历史
            history = self.memory.chat_memory.messages
            
            # 如果启用工具，先检测并执行工具调用
            tools_used = []
            if use_tools:
                tools_used = await self._detect_and_execute_tools(user_message, "")
            
            # 构建完整的对话上下文
            context = ""
            for msg in history:
                if isinstance(msg, HumanMessage):
                    context += f"用户: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    context += f"助手: {msg.content}\n"
            
            # 添加工具信息到上下文
            if use_tools:
                tools_info = "可用工具:\n"
                for tool in self.tool_manager.get_available_tools():
                    tools_info += f"- {tool['name']}: {tool['description']}\n"
                context += f"\n{tools_info}\n"
            
            # 如果有工具结果，添加到上下文中
            if tools_used:
                context += "\n工具执行结果:\n"
                for tool in tools_used:
                    context += f"- {tool['tool']}: {tool['result']}\n"
                context += "\n"
            
            # 添加当前用户消息
            context += f"用户: {user_message}\n助手:"
            
            # 构建包含工具结果的提示词
            system_prompt = """你是一个智能助手，可以使用各种工具来帮助用户。当用户询问需要工具支持的问题时，请基于工具执行结果来回答。

如果检测到用户需要工具支持（如计算、查询时间、天气、翻译等），请使用工具结果来提供准确的回答。

请用友好、自然的语气回答，并在适当时候使用工具结果。"""
            
            # 调用ChatDeepSeek
            messages = [
                ("system", system_prompt),
                ("human", context)
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
                "conversation_history": conversation_history,
                "tools_used": tools_used
            }
        except Exception as e:
            raise Exception(f"AI服务处理错误: {str(e)}")
    
    async def chat_stream(self, user_message: str, use_tools: bool = True):
        """流式聊天方法"""
        try:
            # 获取对话历史
            history = self.memory.chat_memory.messages
            
            # 如果启用工具，先检测并执行工具调用
            tools_used = []
            if use_tools:
                tools_used = await self._detect_and_execute_tools(user_message, "")
            
            # 构建完整的对话上下文
            context = ""
            for msg in history:
                if isinstance(msg, HumanMessage):
                    context += f"用户: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    context += f"助手: {msg.content}\n"
            
            # 添加工具信息到上下文
            if use_tools:
                tools_info = "可用工具:\n"
                for tool in self.tool_manager.get_available_tools():
                    tools_info += f"- {tool['name']}: {tool['description']}\n"
                context += f"\n{tools_info}\n"
            
            # 如果有工具结果，添加到上下文中
            if tools_used:
                context += "\n工具执行结果:\n"
                for tool in tools_used:
                    context += f"- {tool['tool']}: {tool['result']}\n"
                context += "\n"
            
            # 添加当前用户消息
            context += f"用户: {user_message}\n助手:"
            
            # 构建包含工具结果的提示词
            system_prompt = """你是一个智能助手，可以使用各种工具来帮助用户。当用户询问需要工具支持的问题时，请基于工具执行结果来回答。

如果检测到用户需要工具支持（如计算、查询时间、天气、翻译等），请使用工具结果来提供准确的回答。

请用友好、自然的语气回答，并在适当时候使用工具结果。"""
            
            # 保存用户消息到记忆
            self.memory.chat_memory.add_user_message(user_message)
            
            # 调用ChatDeepSeek进行流式输出
            messages = [
                ("system", system_prompt),
                ("human", context)
            ]
            
            # 使用astream方法进行流式输出
            full_response = ""
            async for chunk in self.chat_model.astream(messages):
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    full_response += content
                    # 发送每个字符
                    for char in content:
                        yield f"data: {json.dumps({'content': char, 'type': 'content'})}\n\n"
                        await asyncio.sleep(0.01)  # 控制输出速度
            
            # 保存AI回复到记忆
            self.memory.chat_memory.add_ai_message(full_response)
            
            # 如果有工具使用，发送工具使用信息
            if tools_used:
                yield f"data: {json.dumps({'tools_used': tools_used, 'type': 'tools'})}\n\n"
            
            # 发送完成信号
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
        except Exception as e:
            error_msg = f"AI服务处理错误: {str(e)}"
            yield f"data: {json.dumps({'content': error_msg, 'type': 'error'})}\n\n"
    
    async def _detect_and_execute_tools(self, user_message: str, ai_response: str) -> List[Dict[str, Any]]:
        """检测并执行工具调用"""
        tools_used = []
        
        # 检测计算器调用
        if any(keyword in user_message.lower() for keyword in ['计算', '算', '等于', '+', '-', '*', '/']):
            try:
                import re
                # 改进的数学表达式匹配模式
                math_pattern = r'(\d+[\+\-\*\/\s\(\)\d\.]+)'
                matches = re.findall(math_pattern, user_message)
                if matches:
                    expression = matches[0].strip()
                    result = await self.tool_manager.execute_tool("calculator", {"expression": expression})
                    if result.success:
                        tools_used.append({
                            "tool": "calculator",
                            "parameters": {"expression": expression},
                            "result": result.result
                        })
            except Exception as e:
                print(f"计算器工具执行错误: {e}")
        
        # 检测天气查询
        if any(keyword in user_message.lower() for keyword in ['天气', '气温', '温度']):
            try:
                import re
                city_pattern = r'([北京|上海|广州|深圳|杭州|南京|成都|武汉|西安|重庆|天津|青岛|大连|厦门|苏州|无锡|宁波|长沙|郑州|济南|哈尔滨|沈阳|长春|石家庄|太原|呼和浩特|合肥|福州|南昌|南宁|海口|贵阳|昆明|拉萨|兰州|西宁|银川|乌鲁木齐]+)'
                matches = re.findall(city_pattern, user_message)
                if matches:
                    city = matches[0]
                    result = await self.tool_manager.execute_tool("weather", {"city": city})
                    if result.success:
                        tools_used.append({
                            "tool": "weather",
                            "parameters": {"city": city},
                            "result": result.result
                        })
            except Exception as e:
                print(f"天气工具执行错误: {e}")
        
        # 检测时间查询
        if any(keyword in user_message.lower() for keyword in ['时间', '几点', '日期', '今天', '现在']):
            try:
                result = await self.tool_manager.execute_tool("time", {})
                if result.success:
                    tools_used.append({
                        "tool": "time",
                        "parameters": {},
                        "result": result.result
                    })
            except Exception as e:
                print(f"时间工具执行错误: {e}")
        
        # 检测翻译需求
        if any(keyword in user_message.lower() for keyword in ['翻译', 'translate', '英文', '中文', '日文', '韩文', '法文', '德文', '西班牙文', '俄文']):
            try:
                import re
                
                # 检测目标语言
                target_lang = "en"  # 默认翻译为英文
                if any(lang in user_message.lower() for lang in ['中文', '汉语', 'chinese']):
                    target_lang = "zh"
                elif any(lang in user_message.lower() for lang in ['日文', '日语', 'japanese']):
                    target_lang = "ja"
                elif any(lang in user_message.lower() for lang in ['韩文', '韩语', 'korean']):
                    target_lang = "ko"
                elif any(lang in user_message.lower() for lang in ['法文', '法语', 'french']):
                    target_lang = "fr"
                elif any(lang in user_message.lower() for lang in ['德文', '德语', 'german']):
                    target_lang = "de"
                elif any(lang in user_message.lower() for lang in ['西班牙文', '西班牙语', 'spanish']):
                    target_lang = "es"
                elif any(lang in user_message.lower() for lang in ['俄文', '俄语', 'russian']):
                    target_lang = "ru"
                
                # 提取要翻译的文本（在引号中的内容）
                text_pattern = r'["""]([^"""]+)["""]'
                matches = re.findall(text_pattern, user_message)
                
                if matches:
                    text_to_translate = matches[0]
                    result = await self.tool_manager.execute_tool("translate", {
                        "text": text_to_translate,
                        "target_lang": target_lang
                    })
                    if result.success:
                        tools_used.append({
                            "tool": "translate",
                            "parameters": {
                                "text": text_to_translate,
                                "target_lang": target_lang
                            },
                            "result": result.result
                        })
            except Exception as e:
                print(f"翻译工具执行错误: {e}")
        
        # 检测网络搜索需求
        if any(keyword in user_message.lower() for keyword in ['搜索', '查找', '查询', 'search', '查找', '了解', '联网', '上网']):
            try:
                import re
                
                # 提取搜索关键词
                # 移除常见的搜索指示词
                search_query = user_message
                search_indicators = ['搜索', '查找', '查询', 'search', '查找', '了解', '什么是', '什么是', '如何', '怎么']
                
                for indicator in search_indicators:
                    search_query = search_query.replace(indicator, '').strip()
                
                # 如果搜索查询不为空，执行搜索
                if search_query and len(search_query) > 2:
                    result = await self.tool_manager.execute_tool("web_search", {"query": search_query})
                    if result.success:
                        tools_used.append({
                            "tool": "web_search",
                            "parameters": {"query": search_query},
                            "result": result.result
                        })
            except Exception as e:
                print(f"网络搜索工具执行错误: {e}")
        
        return tools_used
    
    def clear_memory(self):
        """清空记忆"""
        self.memory.clear()
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self._convert_memory_to_history() 
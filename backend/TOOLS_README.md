# 工具系统使用说明

## 概述

本系统集成了多种实用工具，可以自动检测用户意图并调用相应的工具来提供更智能的服务。

## 可用工具

### 1. 计算器工具 (calculator)
- **功能**: 数学计算器，支持基本运算
- **触发关键词**: 计算、算、等于、+、-、*、/
- **示例**: 
  - "帮我计算 25 + 37"
  - "2 * 8 等于多少？"
  - "计算 (15 + 23) * 2"

### 2. 天气查询工具 (weather)
- **功能**: 获取指定城市的天气信息
- **触发关键词**: 天气、气温、温度
- **支持城市**: 北京、上海、广州、深圳、杭州、南京、成都、武汉、西安、重庆、天津、青岛、大连、厦门、苏州、无锡、宁波、长沙、郑州、济南、哈尔滨、沈阳、长春、石家庄、太原、呼和浩特、合肥、福州、南昌、南宁、海口、贵阳、昆明、拉萨、兰州、西宁、银川、乌鲁木齐
- **示例**:
  - "北京今天天气怎么样？"
  - "查询上海的天气"
  - "深圳的气温是多少？"

### 3. 时间查询工具 (time)
- **功能**: 获取当前时间信息
- **触发关键词**: 时间、几点、日期、今天
- **示例**:
  - "现在几点了？"
  - "今天是几号？"
  - "查询当前时间"

### 4. 网络搜索工具 (web_search)
- **功能**: 网络搜索相关信息
- **触发关键词**: 搜索、查找、查询、search、了解、联网、上网
- **示例**:
  - "搜索Python编程教程"
  - "查找最新的AI技术发展"
  - "了解人工智能技术"

### 5. 文本翻译工具 (translate)
- **功能**: 文本翻译（使用MyMemory免费API）
- **触发关键词**: 翻译、translate、英文、中文、日文、韩文、法文、德文、西班牙文、俄文
- **示例**:
  - "翻译'你好世界'为英文"
  - "将'Hello World'翻译成中文"
  - "把'こんにちは'翻译成中文"
  - "翻译'Bonjour'为英文"
  - "将'Guten Tag'翻译成中文"

## API端点

### 获取可用工具列表
```
GET /tools
```

### 执行工具
```
POST /tools/execute
Content-Type: application/json

{
    "tool_name": "calculator",
    "parameters": {
        "expression": "25 + 37"
    }
}
```

### 聊天时使用工具
```
POST /chat/
Content-Type: application/json

{
    "message": "帮我计算 25 + 37",
    "use_tools": true
}
```

### 流式聊天时使用工具
```
POST /chat/stream
Content-Type: application/json

{
    "message": "北京今天天气怎么样？",
    "use_tools": true
}
```

## 配置说明

### 天气API配置
如需使用天气查询功能，请在 `.env` 文件中添加：
```
OPENWEATHER_API_KEY=your_openweather_api_key
```

### 翻译API配置
翻译功能使用 **MyMemory 免费API**，无需注册或API密钥！

**特点：**
- 完全免费，无需注册
- 支持100多种语言
- 每日限制：1000次请求（未注册）/ 5000次请求（注册邮箱）
- 自动语言检测

**可选配置（提高限制）：**
如需提高每日请求限制，可以在代码中设置邮箱地址：
```python
# 在 translate_tool 方法中修改
"de": "your-email@domain.com"  # 替换为您的邮箱
```

**支持的语言：**
- 中文 (zh/zh-CN)
- 英文 (en)
- 日文 (ja)
- 韩文 (ko)
- 法文 (fr)
- 德文 (de)
- 西班牙文 (es)
- 俄文 (ru)
- 阿拉伯文 (ar)
- 印地文 (hi)
- 葡萄牙文 (pt)
- 意大利文 (it)

## 工具检测逻辑

系统会自动检测用户消息中的关键词，并调用相应的工具：

1. **数学计算**: 检测包含数字和运算符的消息
2. **天气查询**: 检测包含天气相关词汇和城市名的消息
3. **时间查询**: 检测包含时间相关词汇的消息
4. **文本翻译**: 检测包含翻译相关词汇和引号包围的文本

## 扩展工具

您可以通过以下方式添加新工具：

```python
# 在 ToolSystem 类中添加新工具方法
async def custom_tool(self, param1: str, param2: int) -> Dict[str, Any]:
    """自定义工具"""
    try:
        # 工具逻辑
        result = do_something(param1, param2)
        return {
            "param1": param1,
            "param2": param2,
            "result": result,
            "type": "custom"
        }
    except Exception as e:
        return {
            "error": f"工具执行错误: {str(e)}",
            "type": "error"
        }

# 在 _register_default_tools 方法中注册
self.register_tool("custom", self.custom_tool, "自定义工具描述")
```

## 注意事项

1. 工具调用是自动的，无需用户明确指定
2. 工具执行结果会包含在API响应中
3. 如果工具执行失败，不会影响正常的聊天功能
4. 可以通过设置 `use_tools: false` 来禁用工具功能 
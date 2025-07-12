# 智能对话Agent API

基于DeepSeek API的智能对话助手，支持多种工具调用。

## 📁 项目结构

```
backend/
├── app.py                 # FastAPI主应用文件
├── agent.py              # AI Agent核心类
├── config.py             # 配置文件
├── start.py              # 启动脚本
├── tools/                # 工具包
│   ├── __init__.py       # 工具包初始化
│   ├── base.py           # 基础工具类
│   ├── manager.py        # 工具管理器
│   ├── calculator.py     # 计算器工具
│   ├── weather.py        # 天气查询工具
│   ├── time_tool.py      # 时间查询工具
│   ├── translator.py     # 翻译工具
│   └── web_search.py     # 网络搜索工具
└── .env                  # 环境变量文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 可选：天气API配置
OPENWEATHER_API_KEY=your_openweather_api_key_here

# 可选：Google翻译API配置
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here
```

### 3. 启动服务器

#### Windows用户（推荐）
```bash
# 快速启动（自动检查环境和依赖）
quick_start.bat

# 或者分步启动
install_conda_en.bat  # 首次使用，安装依赖
start_backend.bat     # 启动服务器
```

#### 手动启动
```bash
# 激活conda环境
conda activate agent_env

# 启动服务器
python start.py
```

#### 直接使用uvicorn
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 核心组件

### AI Agent (`agent.py`)

AI Agent是系统的核心组件，负责：

- 管理对话记忆
- 调用DeepSeek API
- 检测和执行工具调用
- 提供流式输出

### 工具系统 (`tools/`)

模块化的工具系统，包含：

#### 基础工具类 (`base.py`)
- `BaseTool`: 所有工具的基类
- `ToolResult`: 工具执行结果模型

#### 工具管理器 (`manager.py`)
- `ToolManager`: 管理所有可用工具
- 提供工具注册、执行和查询功能

#### 具体工具实现
- **计算器** (`calculator.py`): 数学表达式计算
- **天气查询** (`weather.py`): 城市天气信息
- **时间查询** (`time_tool.py`): 当前时间信息
- **翻译工具** (`translator.py`): 文本翻译（使用MyMemory免费API）
- **网络搜索** (`web_search.py`): 网络信息搜索

### 配置系统 (`config.py`)

集中管理所有配置项：

- API密钥配置
- 模型参数配置
- CORS设置
- 应用元数据

## 📡 API端点

### 聊天相关
- `POST /chat/` - 普通聊天
- `POST /chat/stream` - 流式聊天
- `POST /chat/clear` - 清空对话历史
- `GET /chat/history` - 获取对话历史

### 工具相关
- `GET /tools` - 获取可用工具列表
- `POST /tools/execute` - 执行指定工具

### 系统相关
- `GET /` - 根路径信息
- `GET /health` - 健康检查
- `GET /docs` - API文档

## 🛠️ 添加新工具

### 1. 创建工具类

在 `tools/` 目录下创建新的工具文件：

```python
from .base import BaseTool, ToolResult

class MyNewTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="我的新工具描述"
        )
    
    async def execute(self, **parameters) -> ToolResult:
        # 实现工具逻辑
        try:
            # 工具执行代码
            result = "工具执行结果"
            return ToolResult(
                tool_name=self.name,
                result=result,
                success=True
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                result=None,
                success=False,
                error=str(e)
            )
```

### 2. 注册工具

在 `tools/manager.py` 中注册新工具：

```python
from .my_new_tool import MyNewTool

def _register_default_tools(self):
    """注册默认工具"""
    # ... 现有工具 ...
    self.register_tool(MyNewTool())
```

### 3. 更新导入

在 `tools/__init__.py` 中添加导入：

```python
from .my_new_tool import MyNewTool

__all__ = [
    # ... 现有工具 ...
    'MyNewTool'
]
```

## 🔍 工具调用检测

系统会自动检测用户意图并调用相应工具：

### 计算器
触发关键词：`计算`、`算`、`等于`、`+`、`-`、`*`、`/`
示例：`"帮我计算 25 * 4 + 10"`

### 天气查询
触发关键词：`天气`、`气温`、`温度`
示例：`"北京今天天气怎么样？"`

### 时间查询
触发关键词：`时间`、`几点`、`日期`、`今天`
示例：`"现在几点了？"`

### 翻译
触发关键词：`翻译`、`translate`、语言名称
示例：`"把'你好世界'翻译成英文"`

### 网络搜索
触发关键词：`搜索`、`查找`、`查询`、`search`、`了解`、`联网`、`上网`
示例：`"搜索Python编程教程"`、`"了解人工智能技术"`

## 🌐 免费API获取

### 天气API (OpenWeatherMap)
1. 访问 https://openweathermap.org/
2. 注册免费账户
3. 获取API密钥
4. 在 `.env` 文件中设置 `OPENWEATHER_API_KEY`

### 翻译API (MyMemory)
- 完全免费，无需API密钥
- 支持多种语言
- 有请求频率限制

## 📝 注意事项

1. **API密钥安全**: 确保 `.env` 文件不被提交到版本控制系统
2. **错误处理**: 所有工具都有完善的错误处理机制
3. **异步支持**: 所有工具都支持异步执行
4. **类型安全**: 使用Pydantic进行数据验证
5. **文档完整**: 每个组件都有详细的文档字符串

## 🐛 故障排除

### 常见问题

1. **导入错误**: 确保所有依赖都已正确安装
2. **API密钥错误**: 检查 `.env` 文件中的API密钥配置
3. **工具执行失败**: 查看日志中的具体错误信息
4. **流式输出问题**: 确保前端正确处理Server-Sent Events

### 调试模式

启动时添加详细日志：

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### 常见问题解决

#### 1. 中文乱码问题
- 确保使用UTF-8编码
- 在Windows中运行批处理文件时，脚本会自动设置编码

#### 2. Conda环境问题
```bash
# 检查conda环境
conda info --envs

# 重新创建环境
conda remove -n agent_env --all
conda create -n agent_env python=3.8 -y
```

#### 3. 依赖包安装失败
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或者使用conda安装
conda install fastapi uvicorn python-dotenv requests pytz -c conda-forge
pip install langchain-deepseek
```

#### 4. API密钥配置
确保 `backend/.env` 文件包含正确的API密钥：
```env
DEEPSEEK_API_KEY=your_actual_deepseek_api_key
OPENWEATHER_API_KEY=your_actual_openweather_api_key
``` 
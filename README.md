# Agent Simple - 智能对话助手

一个基于Vite+Vue前端和FastAPI后端的智能对话助手项目，集成DeepSeek API实现AI对话功能。

## 项目结构

```
Agent_simple/
├── frontend/                  # Vue3 + Vite 前端
├── backend/                   # FastAPI 后端
├── requirements.txt           # Python依赖
├── start_conda_zh.bat         # 启动后端（中文无乱码）
├── start_frontend_conda_zh.bat# 启动前端（中文无乱码）
├── start_all_zh.bat           # 一键启动前后端（推荐）
├── install_conda_en.bat       # 安装依赖脚本
└── init_git.bat               # Git仓库初始化脚本
```

## 环境要求

- Python 3.8+
- Node.js 16+
- Conda (推荐使用conda环境管理)

## 快速开始

### 1. 环境准备

确保已安装Conda，并创建名为`agent_env`的conda环境：

```bash
conda create -n agent_env python=3.9
conda activate agent_env
```

### 2. 安装依赖

双击运行 `install_conda_en.bat` 文件，自动安装所有Python依赖。

### 3. 配置API密钥

在项目根目录创建 `.env` 文件，添加您的DeepSeek API密钥：

```
DEEPSEEK_API_KEY=your_api_key_here
```

### 4. 一键启动项目（推荐）

双击运行 `start_all_zh.bat` 文件，自动分别在新窗口启动后端和前端服务。

- 后端地址：http://localhost:8000
- 前端地址：http://localhost:5173

### 5. 访问应用

打开浏览器访问 http://localhost:5173 即可使用智能对话助手。

## 功能特性

- 🤖 集成DeepSeek AI模型
- 💬 实时对话交互
- 📱 响应式Web界面
- 🔄 对话历史管理
- 🌐 跨域支持
- ⚡ 快速开发体验

## 技术栈

### 前端
- Vue 3 + TypeScript
- Vite (构建工具)
- Tailwind CSS (样式)
- Axios (HTTP客户端)

### 后端
- FastAPI (Web框架)
- LangChain (AI集成)
- DeepSeek API (AI模型)
- Uvicorn (ASGI服务器)

## 开发说明

- 后端API文档：http://localhost:8000/docs
- 前端热重载：修改前端代码会自动刷新
- 后端热重载：修改后端代码需要重启服务器

## 版本管理

### 初始化Git仓库
双击运行 `init_git.bat` 文件，自动初始化Git仓库并提交v1.0.0版本。

### 添加远程仓库
```bash
git remote add origin <your-repo-url>
git push -u origin main
git push --tags
```

## 故障排除

1. **依赖安装失败**：确保使用conda环境，并检查网络连接
2. **API密钥错误**：检查.env文件中的DEEPSEEK_API_KEY是否正确
3. **端口占用**：如果8000或5173端口被占用，请修改相应的配置文件

## 许可证

MIT License 
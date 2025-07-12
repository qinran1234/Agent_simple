@echo off
chcp 65001 >nul
echo ========================================
echo 智能对话Agent API 启动脚本
echo ========================================
echo.

echo 激活conda环境...
call conda activate agent_env
if errorlevel 1 (
    echo 错误: 无法激活agent_env环境，请确保已创建该环境
    echo 创建环境命令: conda create -n agent_env python=3.8
    pause
    exit /b 1
)

echo 当前Python环境: %CONDA_DEFAULT_ENV%
echo.

cd backend

echo 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请确保已安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo 检查依赖包...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo 安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

echo.
echo 检查配置文件...
if not exist .env (
    echo 警告: 未找到.env文件，请确保已配置API密钥
    echo 创建示例.env文件...
    echo DEEPSEEK_API_KEY=your_deepseek_api_key_here > .env
    echo OPENWEATHER_API_KEY=your_openweather_api_key_here >> .env
    echo 请编辑backend/.env文件，设置正确的API密钥
    pause
)

echo.
echo 启动服务器...
echo 服务器地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 健康检查: http://localhost:8000/health
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================

python start.py

pause 
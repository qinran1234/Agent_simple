@echo off
chcp 65001 > nul
echo Installing dependencies in conda environment...
echo.

echo 1. Activating agent_env environment...
call conda activate agent_env

echo.
echo 2. Installing core dependencies...
pip install fastapi uvicorn python-dotenv httpx python-multipart requests

echo.
echo 3. Installing langchain-deepseek...
pip install -U langchain-deepseek

echo.
echo 4. Verifying installation...
python -c "from langchain_deepseek import ChatDeepSeek; print('ChatDeepSeek import success!')"

echo.
echo 5. Verifying FastAPI...
python -c "import fastapi; print('FastAPI import success!')"

echo.
echo Dependencies installation completed!
echo Now you can run start_conda.bat to start the backend server
pause 
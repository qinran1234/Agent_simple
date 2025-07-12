@echo off
chcp 65001 > nul
echo 启动前端开发服务器...
echo.

echo 1. 切换到frontend目录...
cd frontend

echo.
echo 2. 安装前端依赖...
npm install

echo.
echo 3. 启动开发服务器...
echo 前端地址: http://localhost:5173
echo.
echo 按 Ctrl+C 终止服务器
echo.

npm run dev

pause 
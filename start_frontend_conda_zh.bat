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

start "前端服务" cmd /k "chcp 65001 > nul && echo 启动前端开发服务器... && npm run dev"

echo.
echo 4. 等待服务器启动...
timeout /t 5 /nobreak > nul

echo.
echo 5. 自动打开浏览器...
start http://localhost:5173

echo.
echo 前端服务已启动并自动打开浏览器！
echo 如需手动打开，请访问: http://localhost:5173
echo.
echo 按任意键退出...
pause > nul 
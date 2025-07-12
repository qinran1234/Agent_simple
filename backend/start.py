#!/usr/bin/env python3
"""
简单的后端服务器启动脚本
"""

import uvicorn
import signal
import sys

def signal_handler(signum, frame):
    """信号处理器"""
    print(f"\n收到信号 {signum}，正在关闭服务器...")
    sys.exit(0)

def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 50)
    print("智能对话Agent API 服务器")
    print("=" * 50)
    print("服务器地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("健康检查: http://localhost:8000/health")
    print("=" * 50)
    print("按 Ctrl+C 可以正常终止服务器")
    print("=" * 50)
    
    try:
        # 启动服务器
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            workers=1,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
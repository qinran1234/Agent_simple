"""
启动脚本
"""
import uvicorn
from config import settings

if __name__ == "__main__":
    print("🚀 启动智能对话Agent API...")
    print(f"📝 应用标题: {settings.APP_TITLE}")
    print(f"📋 应用描述: {settings.APP_DESCRIPTION}")
    print(f"🔧 版本: {settings.APP_VERSION}")
    print(f"🌐 文档地址: http://localhost:8000/docs")
    print(f"📊 健康检查: http://localhost:8000/health")
    print("-" * 50)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 
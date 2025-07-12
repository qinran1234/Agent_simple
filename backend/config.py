"""
配置文件
"""
import os
from dotenv import load_dotenv

# 加载环境变量
try:
    load_dotenv()
except UnicodeDecodeError as e:
    print(f"Error loading .env file: {e}")
    print("Please run fix_env.py to fix the encoding issue")
    raise
except Exception as e:
    print(f"Error loading .env file: {e}")
    print("Please check if .env file exists and has correct format")
    raise

class Settings:
    """应用配置类"""
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_TEMPERATURE: float = 0.7
    DEEPSEEK_MAX_TOKENS: int = 1000
    
    # 外部API配置
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    GOOGLE_TRANSLATE_API_KEY: str = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
    
    # CORS配置
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # 应用配置
    APP_TITLE: str = "智能对话Agent API"
    APP_DESCRIPTION: str = "基于DeepSeek API的智能对话助手"
    APP_VERSION: str = "1.0.0"
    
    @classmethod
    def validate_config(cls):
        """验证配置"""
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DeepSeek API密钥未配置，请在.env文件中设置DEEPSEEK_API_KEY")

# 全局配置实例
settings = Settings()

# 验证配置
try:
    settings.validate_config()
except ValueError as e:
    print(f"配置错误: {e}")
    print("请在backend/.env文件中设置DEEPSEEK_API_KEY") 
import os
from typing import Optional

class Settings:
    """应用配置类"""
    
    # 基本设置
    APP_NAME: str = "八字能量解读系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    # 服务器设置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS设置
    ALLOWED_ORIGINS: list = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
        "https://*.vercel.app",
        "https://*.railway.app",
        "https://*.render.com"
    ]
    
    # 安全设置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 限流设置
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1小时
    
    # 日志设置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 数据库设置（如果需要）
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Redis设置（如果需要缓存）
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    
    # 监控设置
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "False").lower() in ("true", "1", "yes")
    
    # 八字相关设置
    MAX_BAZI_LENGTH: int = 100
    MAX_QUESTION_LENGTH: int = 500
    
    # Claude API设置
    CLAUDE_API_BASE_URL: str = os.getenv("CLAUDE_API_BASE_URL", "https://dashscope.aliyuncs.com/api/v2/apps/claude-code-proxy")
    CLAUDE_API_KEY: Optional[str] = os.getenv("CLAUDE_API_KEY")
    
    class Config:
        env_file = ".env"

# 创建全局设置实例
settings = Settings()
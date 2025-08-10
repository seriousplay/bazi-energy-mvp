from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional
import uvicorn
import os
import logging
from bazi_engine_enhanced import comprehensive_bazi_analysis
from config import settings
from middleware import RateLimitMiddleware, LoggingMiddleware, SecurityMiddleware, InputValidationMiddleware

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="基于传统命理学的现代化能量分析平台",
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 添加自定义中间件
app.add_middleware(SecurityMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.RATE_LIMIT_REQUESTS)
app.add_middleware(InputValidationMiddleware)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

class InterpretRequest(BaseModel):
    name: str
    gender: str  # "male" or "female"
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: int
    birth_minute: int = 0
    location: str = "北京"
    question: Optional[str] = ""
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('姓名不能为空')
        v = v.strip()
        if len(v) > 50:
            raise ValueError('姓名长度不能超过50字符')
        return v
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v not in ["male", "female"]:
            raise ValueError('性别必须是 male 或 female')
        return v
    
    @field_validator('birth_year')
    @classmethod
    def validate_birth_year(cls, v):
        if not (1900 <= v <= 2100):
            raise ValueError('出生年份必须在1900-2100之间')
        return v
    
    @field_validator('birth_month')
    @classmethod
    def validate_birth_month(cls, v):
        if not (1 <= v <= 12):
            raise ValueError('出生月份必须在1-12之间')
        return v
    
    @field_validator('birth_day')
    @classmethod
    def validate_birth_day(cls, v):
        if not (1 <= v <= 31):
            raise ValueError('出生日期必须在1-31之间')
        return v
    
    @field_validator('birth_hour')
    @classmethod
    def validate_birth_hour(cls, v):
        if not (0 <= v <= 23):
            raise ValueError('出生小时必须在0-23之间')
        return v
    
    @field_validator('birth_minute')
    @classmethod
    def validate_birth_minute(cls, v):
        if not (0 <= v <= 59):
            raise ValueError('出生分钟必须在0-59之间')
        return v
    
    @field_validator('location')
    @classmethod
    def validate_location(cls, v):
        if len(v) > 100:
            raise ValueError('出生地点长度不能超过100字符')
        return v
    
    @field_validator('question')
    @classmethod
    def validate_question(cls, v):
        if v and len(v) > settings.MAX_QUESTION_LENGTH:
            raise ValueError(f'问题长度不能超过{settings.MAX_QUESTION_LENGTH}字符')
        return v

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回主页面"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="页面文件未找到")

@app.post("/interpret")
def interpret(req: InterpretRequest):
    """八字解读API端点"""
    try:
        logger.info(f"解读请求 - 姓名: {req.name}, 出生: {req.birth_year}-{req.birth_month}-{req.birth_day} {req.birth_hour}:{req.birth_minute}, 地点: {req.location}, 问题: {req.question or '无'}")
        
        # 使用增强版引擎，传入完整出生信息
        input_data = {
            "birth_info": {
                "year": req.birth_year,
                "month": req.birth_month,
                "day": req.birth_day,
                "hour": req.birth_hour,
                "minute": req.birth_minute,
                "location": req.location,
                "name": req.name,
                "gender": req.gender
            },
            "question": req.question or ""
        }
        
        out = comprehensive_bazi_analysis(input_data)
        
        # 在结果中添加用户基本信息
        out["用户信息"] = {
            "姓名": req.name,
            "性别": "男" if req.gender == "male" else "女",
            "出生时间": f"{req.birth_year}年{req.birth_month}月{req.birth_day}日 {req.birth_hour}时{req.birth_minute}分",
            "出生地点": req.location
        }
        
        logger.info(f"解读完成 - 姓名: {req.name}")
        return {"ok": True, "result": out}
        
    except ValueError as e:
        logger.warning(f"输入验证错误: {str(e)} - 姓名: {req.name}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"解读错误: {str(e)} - 姓名: {req.name}")
        raise HTTPException(status_code=500, detail="系统内部错误，请稍后重试")

@app.get("/api/health")
def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "八字能量解读系统",
        "version": "1.0.0"
    }

@app.get("/api/info")  
def api_info():
    """API信息"""
    return {
        "name": "八字能量解读系统",
        "version": "1.0.0",
        "description": "基于传统命理学的现代化能量分析平台",
        "endpoints": {
            "/": "主页面",
            "/interpret": "八字解读API",
            "/api/health": "健康检查",
            "/api/info": "API信息"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
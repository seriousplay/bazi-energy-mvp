"""
Enhanced Bazi Energy Analysis API
增强版八字能量分析API - 符合MVP需求
"""

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional, Dict, Any, List
import uvicorn
import os
import logging
from datetime import datetime
import io

# 导入自定义模块
from bazi_engine_enhanced import comprehensive_bazi_analysis
from llm_interpreter import generate_natural_language_interpretation
from claude_api_client import generate_claude_api_interpretation
from pdf_generator import generate_bazi_pdf
from config import settings
from middleware import RateLimitMiddleware, LoggingMiddleware, SecurityMiddleware

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="八字能量分析系统 MVP",
    description="基于能量易学的专业八字分析平台，支持生辰转换、格局判定、寒燥分析、病药判定、大运分析",
    version="2.0.0",
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

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 数据模型定义
class BirthInfoModel(BaseModel):
    """出生信息模型"""
    name: str
    gender: str  # male/female
    year: int
    month: int
    day: int
    hour: int
    minute: int = 0
    location: str
    # 以下字段由系统自动计算，不需要用户输入
    timezone: str = "Asia/Shanghai"
    hemisphere: str = "north"  # north/south

class EnhancedInterpretRequest(BaseModel):
    """增强版解读请求"""
    # 方式1：直接输入八字
    bazi_string: Optional[str] = None
    
    # 方式2：输入生辰信息
    birth_info: Optional[BirthInfoModel] = None
    
    # 用户问题
    question: str = ""
    
    # 解读模式
    mode: str = "general"  # general/expert/detailed
    
    # 当前年龄（用于大运分析）
    current_age: int = 25
    
    # LLM解读选项
    llm_option: str = "local"  # local/claude_api
    
    @field_validator('question')
    @classmethod
    def validate_question(cls, v):
        if v and len(v) > 300:
            raise ValueError('问题长度不能超过300字符')
        return v
    
    @field_validator('bazi_string')
    @classmethod
    def validate_bazi_string(cls, v):
        if v:
            v = v.strip()
            if len(v) > 100:
                raise ValueError('八字字符串过长')
            # 简单格式验证
            import re
            pattern = r'^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\s+[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\s+[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\s+[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]$'
            if not re.match(pattern, v):
                raise ValueError('八字格式不正确，应为：年柱 月柱 日柱 时柱')
        return v

    def model_post_init(self, __context):
        """验证必须提供八字或生辰信息之一"""
        if not self.bazi_string and not self.birth_info:
            raise ValueError('必须提供八字字符串或出生信息之一')

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回主页面"""
    try:
        # 读取增强版HTML页面
        html_path = "static/index_enhanced.html"
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            # 返回基础版本
            with open("static/index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="页面文件未找到")

@app.post("/api/v2/comprehensive-analysis")
async def comprehensive_analysis(req: EnhancedInterpretRequest):
    """
    综合八字分析API v2.0
    支持生辰→八字转换、完整规则引擎分析、LLM解读
    """
    try:
        logger.info(f"综合分析请求 - 问题: {req.question[:50]}..., 模式: {req.mode}")
        
        # 准备输入数据
        input_data = {
            "question": req.question,
            "current_age": req.current_age
        }
        
        if req.bazi_string:
            input_data["bazi_string"] = req.bazi_string
        elif req.birth_info:
            input_data["birth_info"] = req.birth_info.model_dump()
        
        # 1. 结构化分析
        structured_result = comprehensive_bazi_analysis(input_data)
        
        # 2. LLM自然语言解读（支持本地和Claude API选项）
        if req.llm_option == "claude_api":
            logger.info("使用Claude API进行解读")
            interpretation = generate_claude_api_interpretation(
                structured_result=structured_result,
                user_question=req.question,
                mode='detailed',
                api_url=settings.CLAUDE_API_BASE_URL,
                api_key=settings.CLAUDE_API_KEY
            )
        else:
            logger.info("使用本地LLM进行解读")
            interpretation = generate_natural_language_interpretation(
                structured_result=structured_result,
                user_question=req.question,
                mode='detailed'
            )
        
        # 3. 构建响应
        response = {
            "success": True,
            "data": {
                "structured_analysis": structured_result,
                "natural_language_interpretation": interpretation,
                "metadata": {
                    "analysis_time": datetime.now().isoformat(),
                    "engine_version": "2.0.0",
                    "mode": req.mode,
                    "llm_option": req.llm_option
                }
            }
        }
        
        logger.info(f"综合分析完成")
        return response
        
    except ValueError as e:
        logger.warning(f"输入验证错误: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"分析错误: {str(e)}")
        raise HTTPException(status_code=500, detail="分析过程中发生错误，请稍后重试")

@app.post("/api/v2/generate-pdf")
async def generate_analysis_pdf(req: EnhancedInterpretRequest):
    """
    生成分析报告PDF
    """
    try:
        logger.info(f"PDF生成请求")
        
        # 准备输入数据
        input_data = {
            "question": req.question,
            "current_age": req.current_age
        }
        
        if req.bazi_string:
            input_data["bazi_string"] = req.bazi_string
        elif req.birth_info:
            input_data["birth_info"] = req.birth_info.model_dump()
        
        # 1. 获取分析结果
        structured_result = comprehensive_bazi_analysis(input_data)
        
        # 添加个人信息到结构化结果中（用于PDF生成）
        personal_info = {}
        if req.birth_info:
            personal_info = {
                'name': req.birth_info.name,
                'gender': req.birth_info.gender,
                'year': req.birth_info.year,
                'month': req.birth_info.month,
                'day': req.birth_info.day,
                'hour': req.birth_info.hour,
                'location': req.birth_info.location,
                'current_age': req.current_age
            }
        structured_result['个人信息'] = personal_info
        
        # 2. 生成自然语言解读（支持本地和Claude API选项）
        if req.llm_option == "claude_api":
            interpretation = generate_claude_api_interpretation(
                structured_result=structured_result,
                user_question=req.question,
                mode='detailed',
                api_url=settings.CLAUDE_API_BASE_URL,
                api_key=settings.CLAUDE_API_KEY
            )
        else:
            interpretation = generate_natural_language_interpretation(
                structured_result=structured_result,
                user_question=req.question,
                mode='detailed'
            )
        
        # 3. 生成PDF
        pdf_data = generate_bazi_pdf(structured_result, interpretation)
        
        # 4. 返回PDF文件
        filename = f"BaziAnalysisReport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return StreamingResponse(
            io.BytesIO(pdf_data),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"PDF生成错误: {str(e)}")
        raise HTTPException(status_code=500, detail="PDF生成失败")

@app.get("/api/v2/health")
def health_check_v2():
    """增强版健康检查"""
    return {
        "status": "healthy",
        "service": "八字能量分析系统",
        "version": "2.0.0",
        "features": [
            "生辰→八字转换",
            "格局判定",
            "寒燥分析", 
            "病药判定",
            "大运分析",
            "LLM自然语言解读",
            "PDF报告导出"
        ],
        "timestamp": datetime.now().isoformat()
    }

class ClaudeAPIConfigModel(BaseModel):
    """Claude API配置模型"""
    base_url: Optional[str] = None
    api_key: Optional[str] = None

@app.post("/api/v2/configure-claude-api")
async def configure_claude_api(config: ClaudeAPIConfigModel):
    """配置Claude API设置"""
    try:
        base_url = config.base_url or settings.CLAUDE_API_BASE_URL
        api_key = config.api_key
        
        # 验证URL格式
        if not base_url.startswith('https://'):
            raise ValueError('API URL必须使用HTTPS')
        
        # 验证API Key
        if not api_key:
            raise ValueError('API Key不能为空')
        
        # 测试API连接
        from claude_api_client import create_claude_api_client
        client = create_claude_api_client(base_url, api_key)
        
        return {
            "success": True,
            "message": "Claude API配置测试成功",
            "config": {
                "base_url": base_url,
                "api_key_configured": bool(api_key),
                "status": "ready"
            }
        }
        
    except Exception as e:
        logger.error(f"Claude API配置错误: {str(e)}")
        raise HTTPException(status_code=400, detail=f"配置失败: {str(e)}")

@app.get("/api/v2/claude-api-status")
async def get_claude_api_status():
    """获取Claude API状态"""
    try:
        from claude_api_client import create_claude_api_client
        
        api_key_configured = bool(settings.CLAUDE_API_KEY)
        client = create_claude_api_client(settings.CLAUDE_API_BASE_URL, settings.CLAUDE_API_KEY)
        
        return {
            "status": "configured" if api_key_configured else "not_configured",
            "base_url": settings.CLAUDE_API_BASE_URL,
            "api_key_configured": api_key_configured,
            "timeout": client.config.timeout,
            "message": "Claude API已配置" if api_key_configured else "需要配置API Key才能使用Claude API"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Claude API配置检查失败"
        }

@app.get("/api/v2/analysis-demo")
def get_analysis_demo():
    """获取分析示例（用于前端展示）"""
    return {
        "demo_inputs": [
            {
                "name": "示例1：直接输入八字",
                "data": {
                    "bazi_string": "甲子 乙丑 丙寅 丁巳",
                    "question": "我适合创业吗？",
                    "mode": "general"
                }
            },
            {
                "name": "示例2：输入生辰信息",
                "data": {
                    "birth_info": {
                        "year": 1990,
                        "month": 3,
                        "day": 15,
                        "hour": 14,
                        "minute": 30,
                        "timezone": "Asia/Shanghai",
                        "hemisphere": "north",
                        "location": "北京",
                        "gender": "male"
                    },
                    "question": "未来五年的事业发展如何？",
                    "mode": "expert",
                    "current_age": 34
                }
            }
        ],
        "supported_questions": [
            "我适合创业吗？",
            "未来几年的事业发展如何？",
            "我的性格特点是什么？",
            "如何改善我的财运？",
            "我适合什么样的伴侣？",
            "健康方面需要注意什么？",
            "什么时候是我的人生转折点？"
        ]
    }

# 保留兼容性的旧版API
@app.post("/interpret")
def interpret_legacy(req: dict):
    """兼容旧版本的简单解读API"""
    try:
        bazi_string = req.get('bazi', '')
        question = req.get('question', '')
        
        # 转换为新版格式
        enhanced_req = EnhancedInterpretRequest(
            bazi_string=bazi_string,
            question=question,
            mode="general"
        )
        
        # 调用新版分析
        input_data = {"bazi_string": bazi_string, "question": question}
        structured_result = comprehensive_bazi_analysis(input_data)
        interpretation = generate_natural_language_interpretation(
            structured_result=structured_result,
            user_question=question,
            mode="detailed"
        )
        
        # 简化输出以保持兼容性
        return {
            "ok": True,
            "result": {
                "八字信息": structured_result["bazi"],
                "五行统计": structured_result["五行统计"],
                "格局分析": structured_result["定格局"],
                "寒燥分析": structured_result["定寒燥"],
                "基础解读": interpretation["energy_portrait"],
                "问题回答": interpretation.get("question_answer", "")
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/info")
def api_info():
    """API信息"""
    return {
        "name": "八字能量分析系统",
        "version": "2.0.0",
        "description": "基于能量易学的专业八字分析平台",
        "endpoints": {
            "/": "主页面",
            "/api/v2/comprehensive-analysis": "综合八字分析 v2.0",
            "/api/v2/generate-pdf": "生成PDF报告",
            "/api/v2/configure-claude-api": "配置Claude API",
            "/api/v2/claude-api-status": "Claude API状态",
            "/api/v2/health": "系统健康检查",
            "/api/v2/analysis-demo": "分析示例",
            "/interpret": "兼容旧版解读API",
            "/api/info": "API信息"
        },
        "features": {
            "birth_to_bazi": "生辰转八字",
            "pattern_analysis": "格局判定",
            "cold_hot_analysis": "寒燥分析", 
            "medicine_analysis": "病药判定",
            "fortune_timeline": "大运分析",
            "llm_interpretation": "智能解读",
            "claude_api_integration": "Claude API集成",
            "pdf_export": "PDF导出",
            "expert_mode": "专家模式"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app_enhanced:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
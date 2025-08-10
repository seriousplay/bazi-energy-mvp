import time
import logging
from typing import Dict
from collections import defaultdict
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """简单的内存限流中间件"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        
    async def dispatch(self, request: Request, call_next):
        # 获取客户端IP
        client_ip = request.client.host if request.client else "unknown"
        
        # 清理过期的请求记录
        now = time.time()
        minute_ago = now - 60
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if req_time > minute_ago
        ]
        
        # 检查限流
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "请求过于频繁，请稍后再试"}
            )
        
        # 记录请求时间
        self.requests[client_ip].append(now)
        
        response = await call_next(request)
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 获取请求信息
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        url = str(request.url)
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # 记录成功请求
            logger.info(
                f"{method} {url} - {client_ip} - "
                f"Status: {response.status_code} - "
                f"Time: {process_time:.3f}s"
            )
            
            # 添加响应头
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            
            # 记录错误请求
            logger.error(
                f"{method} {url} - {client_ip} - "
                f"Error: {str(e)} - "
                f"Time: {process_time:.3f}s"
            )
            
            # 返回通用错误响应
            return JSONResponse(
                status_code=500,
                content={"detail": "服务器内部错误"}
            )

class SecurityMiddleware(BaseHTTPMiddleware):
    """安全头中间件"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # 添加安全响应头
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # 如果是HTTPS，添加HSTS头
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

class InputValidationMiddleware(BaseHTTPMiddleware):
    """输入验证中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 检查请求大小
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
            return JSONResponse(
                status_code=413,
                content={"detail": "请求体过大"}
            )
        
        # 对于POST请求，验证JSON格式
        if request.method == "POST" and request.url.path == "/interpret":
            try:
                body = await request.body()
                if body:
                    data = json.loads(body)
                    
                    # 验证八字字段
                    if "bazi" in data:
                        bazi = data["bazi"]
                        if not isinstance(bazi, str) or len(bazi.strip()) == 0:
                            return JSONResponse(
                                status_code=400,
                                content={"detail": "八字格式无效"}
                            )
                        if len(bazi) > 100:
                            return JSONResponse(
                                status_code=400,
                                content={"detail": "八字内容过长"}
                            )
                    
                    # 验证问题字段
                    if "question" in data and data["question"]:
                        question = data["question"]
                        if len(question) > 1000:
                            return JSONResponse(
                                status_code=400,
                                content={"detail": "问题内容过长"}
                            )
                
                # 重构request以便后续处理
                async def receive():
                    return {"type": "http.request", "body": body}
                
                request._receive = receive
                
            except json.JSONDecodeError:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "无效的JSON格式"}
                )
        
        response = await call_next(request)
        return response
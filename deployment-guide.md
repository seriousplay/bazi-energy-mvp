# 八字能量系统部署指南

## 项目概览

八字能量解读系统是一个基于 FastAPI 的现代化 Web 应用，提供传统命理学八字分析功能。系统包含完整的前端界面、后端API和生产就绪的部署配置。

## 核心功能

✅ **完整的八字解读引擎**
- 十神关系判定（比肩、劫财、正印、偏印等）
- 五行生克分析
- 地支藏干计算
- 日主强弱判断
- 个性化问题解答

✅ **现代化Web界面**
- 响应式设计，支持移动端
- 实时输入验证
- 美观的结果展示
- 示例八字快速输入

✅ **生产就绪的后端**
- 安全中间件（CORS、XSS防护、限流）
- 结构化日志记录
- 健康检查端点
- 输入验证和错误处理

✅ **完善的部署配置**
- Docker 多阶段构建优化
- Docker Compose 本地开发
- CI/CD 流水线配置
- 多平台部署支持

## 快速开始

### 方法一：Docker（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd bazi-energy-mvp

# 使用 Docker Compose 启动
docker-compose up --build

# 访问 http://localhost:8000
```

### 方法二：本地开发

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 安装依赖
pip install -r requirements.txt

# 启动应用
python app.py

# 访问 http://localhost:8000
```

### 方法三：测试核心功能

```bash
# 运行单元测试
pytest -v

# 测试八字解读
python -c "
from bazi_engine_d1d2 import interpret_bazi
result = interpret_bazi('甲子 乙丑 丙寅 丁巳', '我适合创业吗？')
print('解读成功!')
"
```

## 生产部署

### 1. Railway 部署

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录并部署
railway login
railway up

# Railway 会自动识别 railway.toml 配置
```

### 2. Vercel 部署

```bash
# 安装 Vercel CLI  
npm install -g vercel

# 部署
vercel --prod

# Vercel 会使用 vercel.json 配置
```

### 3. Docker 生产部署

```bash
# 构建生产镜像
docker build -t bazi-energy-mvp:prod .

# 运行容器
docker run -d \\
  --name bazi-energy \\
  -p 8000:8000 \\
  -e DEBUG=false \\
  -e SECRET_KEY=your-production-secret \\
  --restart unless-stopped \\
  bazi-energy-mvp:prod
```

## 环境配置

创建 `.env` 文件（基于 `.env.example`）：

```bash
# 基础配置
DEBUG=false
SECRET_KEY=your-secure-secret-key

# 性能配置
RATE_LIMIT_REQUESTS=60
LOG_LEVEL=INFO

# 安全配置
MAX_BAZI_LENGTH=100
MAX_QUESTION_LENGTH=500
```

## 监控和维护

### 健康检查
- GET `/api/health` - 应用健康状态
- GET `/api/info` - API版本信息

### 日志监控
- 请求日志自动记录
- 错误追踪和报告
- 性能指标统计

### 安全特性
- 请求速率限制（默认60次/分钟）
- 输入验证和清理
- CORS 跨域保护
- 安全响应头

## 技术栈

**后端**
- FastAPI - 现代 Python Web 框架
- Uvicorn - 高性能 ASGI 服务器
- Pydantic - 数据验证

**前端**
- 原生 HTML/CSS/JavaScript
- 响应式设计
- Font Awesome 图标

**部署**
- Docker + Docker Compose
- GitHub Actions CI/CD
- 多云平台支持

## 扩展建议

1. **增强功能**
   - 集成日期转换库（公历→农历）
   - 添加更多命理算法
   - 支持大运、流年分析

2. **性能优化**
   - 添加 Redis 缓存
   - 数据库持久化
   - CDN 静态资源

3. **用户体验**
   - 用户账号系统
   - 解读历史记录
   - 分享功能

## 支持

如有问题，请检查：
- 健康检查端点是否正常
- 日志文件错误信息
- Docker 容器状态
- 环境变量配置

项目已完全准备好生产部署！
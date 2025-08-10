# Claude API Integration Guide

The Bazi Energy Analysis System now supports external Claude API integration as an additional LLM interpretation option alongside the local interpreter.

## ✅ Features Implemented

### 1. Backend Integration
- **Claude API Client** (`claude_api_client.py`) - Full-featured API client with authentication
- **Environment Configuration** - API settings via environment variables  
- **Dual LLM Support** - Users can choose between local and Claude API interpretation
- **Error Handling** - Graceful fallback when API is unavailable
- **API Management Endpoints** - Configuration and status checking

### 2. Frontend Interface
- **LLM Option Selection** - Dropdown to choose AI interpretation engine
- **API Settings Modal** - User-friendly configuration interface
- **Status Display** - Real-time API availability checking
- **Test Connection** - Validate API key before using

### 3. Security & Configuration
- **API Key Authentication** - Secure Bearer token authentication
- **HTTPS Enforcement** - Only secure endpoints allowed
- **Session-only Storage** - API keys not permanently stored
- **Environment Variables** - Secure configuration management

## 🚀 Setup Instructions

### 1. Environment Configuration

Create or update your `.env` file:

```bash
# Claude API配置
CLAUDE_API_BASE_URL=https://dashscope.aliyuncs.com/api/v2/apps/claude-code-proxy
CLAUDE_API_KEY=your-dashscope-api-key-here
```

### 2. Get DashScope API Key

1. Visit [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)
2. Login to your Aliyun account
3. Navigate to API-KEY management page
4. Create a new API Key
5. Copy the API Key for configuration

### 3. Configuration Options

**Option A: Environment Variables (Recommended)**
```bash
export CLAUDE_API_KEY="your-api-key-here"
```

**Option B: Frontend Configuration**
1. Click the "API设置" button in the analysis results
2. Enter your API Key in the modal
3. Test the connection
4. Save configuration (session-only)

## 📚 Usage

### 1. Basic Usage
1. Select "Claude API分析" from the AI解读选项 dropdown
2. Perform analysis as normal
3. The system will use Claude API for interpretation

### 2. API Status Checking
- **Green**: API configured and ready
- **Yellow**: API Key needed
- **Red**: Configuration error

### 3. Automatic Fallback
If Claude API fails, the system automatically falls back to local interpretation with an informative error message.

## 🔧 API Endpoints

- `GET /api/v2/claude-api-status` - Check API configuration status
- `POST /api/v2/configure-claude-api` - Configure API settings
- `POST /api/v2/comprehensive-analysis` - Supports `llm_option` parameter

## 🛡️ Security Features

- API keys are never stored permanently
- HTTPS-only API endpoints
- Bearer token authentication
- Input validation and sanitization
- Error messages don't expose sensitive data

## 🧪 Testing

Test the integration:

```bash
# Check API status
curl http://localhost:8000/api/v2/claude-api-status

# Test configuration
curl -X POST http://localhost:8000/api/v2/configure-claude-api \
  -H "Content-Type: application/json" \
  -d '{"base_url": "https://dashscope.aliyuncs.com/api/v2/apps/claude-code-proxy", "api_key": "your-key"}'
```

## ⚠️ Important Notes

1. **API Key Security**: Never commit API keys to version control
2. **Rate Limits**: Respect DashScope API rate limiting
3. **Cost Management**: Monitor API usage and costs
4. **Fallback Ready**: Local interpretation always available as backup
5. **Session Storage**: Frontend API key configuration is temporary

## 🐛 Troubleshooting

### Common Issues

**"API Key配置错误"**
- Verify API key is correct
- Check DashScope console for key status
- Ensure key has necessary permissions

**"连接超时"**
- Check internet connectivity
- Verify API base URL
- Try increasing timeout in configuration

**"认证失败"**
- API key may be expired or invalid
- Check DashScope account status
- Regenerate API key if needed

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
```

This will provide detailed API request/response information for troubleshooting.

---

**Ready to use!** The Claude API integration provides a powerful alternative interpretation engine while maintaining full compatibility with the existing Bazi analysis system. 🎯
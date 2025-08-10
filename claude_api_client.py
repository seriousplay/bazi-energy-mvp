"""
Claude API Client for External LLM Integration
外部Claude API集成客户端
"""

import json
import requests
from typing import Dict, Any, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ClaudeAPIConfig:
    """Claude API配置"""
    base_url: str = "https://dashscope.aliyuncs.com/api/v2/apps/claude-code-proxy"
    api_key: str = ""
    timeout: int = 30
    max_retries: int = 3

class ClaudeAPIClient:
    """Claude API客户端"""
    
    def __init__(self, config: ClaudeAPIConfig = None):
        self.config = config or ClaudeAPIConfig()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'BaziEnergyMVP/2.0'
        })
        
        # 添加API Key认证
        if self.config.api_key:
            # DashScope通常使用Authorization Bearer token
            self.session.headers.update({
                'Authorization': f'Bearer {self.config.api_key}'
            })
    
    def generate_interpretation(self, structured_result: Dict[str, Any], 
                              user_question: str = "", mode: str = "general") -> Dict[str, str]:
        """使用外部Claude API生成解读"""
        try:
            # 构建提示词
            prompt = self._build_interpretation_prompt(structured_result, user_question, mode)
            
            # 调用API
            response = self._call_api(prompt)
            
            # 解析响应
            return self._parse_interpretation_response(response)
            
        except Exception as e:
            logger.error(f"Claude API调用失败: {str(e)}")
            # 检查是否是认证问题
            if "401" in str(e) or "Unauthorized" in str(e):
                error_msg = "外部AI服务认证失败，请检查API Key配置。"
            elif "403" in str(e) or "Forbidden" in str(e):
                error_msg = "外部AI服务访问被拒绝，请检查API权限。"
            else:
                error_msg = "外部AI服务暂时不可用，请使用本地解读模式。"
            
            return {
                "energy_portrait": error_msg,
                "question_answer": "",
                "practice_suggestions": "",
                "disclaimer": "本解读由本地系统生成，外部AI服务暂时不可用。"
            }
    
    def _build_interpretation_prompt(self, structured_result: Dict[str, Any], 
                                   user_question: str, mode: str) -> str:
        """构建解读提示词"""
        
        bazi_info = structured_result.get("bazi", {})
        wuxing_info = structured_result.get("五行统计", {})
        geju_info = structured_result.get("定格局", {})
        hanzao_info = structured_result.get("定寒燥", {})
        bingyao_info = structured_result.get("定病药", {})
        dayun_info = structured_result.get("看大运", {})
        
        prompt = f"""
你是一位专业的八字命理分析师，基于以下结构化分析结果，为用户生成自然语言解读。

## 八字信息
年柱: {bazi_info.get('year', '')}
月柱: {bazi_info.get('month', '')}
日柱: {bazi_info.get('day', '')}
时柱: {bazi_info.get('hour', '')}

## 五行统计
木: {wuxing_info.get('wood', 0)}
火: {wuxing_info.get('fire', 0)}
土: {wuxing_info.get('earth', 0)}
金: {wuxing_info.get('metal', 0)}
水: {wuxing_info.get('water', 0)}
最旺: {wuxing_info.get('最旺', '未知')}
最弱: {wuxing_info.get('最弱', '未知')}

## 格局分析
格局类型: {geju_info.get('格局类型', '未知')}
强弱: {geju_info.get('强弱', '未知')}
根: {geju_info.get('根', '未知')}
扶抑关系: {geju_info.get('扶抑关系', '未知')}

## 寒燥调候
类型: {hanzao_info.get('类型', '未知')}
需要调候: {hanzao_info.get('需要调候', '未知')}
原因: {hanzao_info.get('原因', '未知')}

## 大运分析
{self._format_dayun_info(dayun_info)}

## 用户问题
{user_question if user_question else "无具体问题"}

## 解读模式
{mode}

请基于以上信息，生成以下四个部分的解读：

1. **能量画像** (一句话的隐喻描述，要有画面感)
2. **针对性建议** (如果有用户问题，针对问题回答；如果没有问题，可以留空)
3. **调候练习建议** (基于寒燥分析给出具体的调候建议)
4. **免责声明** (标准的命理分析免责声明)

请以JSON格式返回结果：
{{
    "energy_portrait": "能量画像内容...",
    "question_answer": "问题回答内容...",
    "practice_suggestions": "调候建议内容...",
    "disclaimer": "免责声明内容..."
}}
"""
        
        return prompt.strip()
    
    def _format_dayun_info(self, dayun_info: Dict[str, Any]) -> str:
        """格式化大运信息"""
        if not dayun_info:
            return "大运信息不可用"
        
        current_dayun = dayun_info.get("当前大运", {})
        if not current_dayun:
            return "当前大运信息不可用"
        
        return f"""当前大运: {current_dayun.get('age_range', '未知')}岁
大运干支: {current_dayun.get('gan', '')}{current_dayun.get('zhi', '')}
影响分析: {current_dayun.get('influence', '未知')}"""
    
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """调用Claude API"""
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"调用Claude API，尝试 {attempt + 1}/{self.config.max_retries}")
                
                response = self.session.post(
                    self.config.base_url,
                    json=payload,
                    timeout=self.config.timeout
                )
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"API调用失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt == self.config.max_retries - 1:
                    raise
                
        raise Exception("API调用达到最大重试次数")
    
    def _parse_interpretation_response(self, response: Dict[str, Any]) -> Dict[str, str]:
        """解析API响应"""
        try:
            # 假设响应格式为 {"content": "JSON字符串"}
            content = response.get("content", "")
            if not content:
                # 尝试其他可能的响应格式
                content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not content:
                raise ValueError("响应中没有找到内容")
            
            # 尝试解析JSON
            try:
                parsed_content = json.loads(content)
                return {
                    "energy_portrait": parsed_content.get("energy_portrait", ""),
                    "question_answer": parsed_content.get("question_answer", ""),
                    "practice_suggestions": parsed_content.get("practice_suggestions", ""),
                    "disclaimer": parsed_content.get("disclaimer", "基于传统命理学分析，仅供参考。")
                }
            except json.JSONDecodeError:
                # 如果不是JSON格式，尝试直接使用内容
                return {
                    "energy_portrait": content[:200] + "..." if len(content) > 200 else content,
                    "question_answer": "",
                    "practice_suggestions": "",
                    "disclaimer": "基于外部AI分析，仅供参考。"
                }
                
        except Exception as e:
            logger.error(f"响应解析失败: {str(e)}")
            raise ValueError(f"无法解析API响应: {str(e)}")


# 工厂函数
def create_claude_api_client(base_url: str = None, api_key: str = None) -> ClaudeAPIClient:
    """创建Claude API客户端"""
    config = ClaudeAPIConfig()
    if base_url:
        config.base_url = base_url
    if api_key:
        config.api_key = api_key
    
    return ClaudeAPIClient(config)


# 主要接口函数
def generate_claude_api_interpretation(
    structured_result: Dict[str, Any], 
    user_question: str = "",
    mode: str = "general",
    api_url: str = None,
    api_key: str = None
) -> Dict[str, str]:
    """使用外部Claude API生成自然语言解读"""
    client = create_claude_api_client(api_url, api_key)
    return client.generate_interpretation(structured_result, user_question, mode)
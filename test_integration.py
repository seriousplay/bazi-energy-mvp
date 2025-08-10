#!/usr/bin/env python3
"""
集成测试脚本 - 验证八字系统的核心功能
"""

import requests
import json
import sys

def test_api(endpoint, payload, description):
    """测试API端点"""
    try:
        url = f"http://127.0.0.1:8000{endpoint}"
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {description}: 成功")
            return data
        else:
            print(f"❌ {description}: 失败 ({response.status_code})")
            print(f"   错误: {response.text[:100]}...")
            return None
    except Exception as e:
        print(f"❌ {description}: 异常 - {str(e)}")
        return None

def main():
    print("🧪 八字能量分析系统 - 集成测试")
    print("=" * 50)
    
    # 测试案例
    test_cases = [
        {
            "description": "测试1: 北京用户(自动识别北半球)",
            "payload": {
                "birth_info": {
                    "name": "张三",
                    "gender": "male",
                    "year": 1990,
                    "month": 3,
                    "day": 15,
                    "hour": 14,
                    "location": "北京"
                },
                "question": "我适合创业吗？",
                "mode": "general"
            }
        },
        {
            "description": "测试2: 悉尼用户(自动识别南半球)", 
            "payload": {
                "birth_info": {
                    "name": "李四",
                    "gender": "female",
                    "year": 1985,
                    "month": 8,
                    "day": 22,
                    "hour": 10,
                    "location": "悉尼"
                },
                "question": "未来发展如何？",
                "mode": "expert"
            }
        },
        {
            "description": "测试3: 纽约用户(自动识别时区)",
            "payload": {
                "birth_info": {
                    "name": "王五",
                    "gender": "male",
                    "year": 1992,
                    "month": 12,
                    "day": 5,
                    "hour": 18,
                    "location": "纽约"
                },
                "question": "性格特点分析",
                "mode": "detailed"
            }
        }
    ]
    
    success_count = 0
    
    for i, case in enumerate(test_cases, 1):
        result = test_api("/api/v2/comprehensive-analysis", case["payload"], case["description"])
        
        if result and result.get("success"):
            # 检查关键数据结构
            data = result.get("data", {})
            structured = data.get("structured_analysis", {})
            interpretation = data.get("natural_language_interpretation", {})
            
            print(f"   📊 八字: {structured.get('bazi', {})}")
            print(f"   🔮 能量画像: {interpretation.get('energy_portrait', '')[:50]}...")
            print(f"   💡 问题回答: {interpretation.get('question_answer', '')[:50]}...")
            
            success_count += 1
        
        print()
    
    # 健康检查
    try:
        health_response = requests.get("http://127.0.0.1:8000/api/v2/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ 系统健康检查: {health_data.get('status', 'unknown')}")
            print(f"   版本: {health_data.get('version', 'unknown')}")
            print(f"   功能: {', '.join(health_data.get('features', []))}")
        else:
            print("❌ 系统健康检查: 失败")
    except:
        print("❌ 系统健康检查: 无法连接")
    
    print("\n" + "=" * 50)
    print(f"📈 测试结果: {success_count}/{len(test_cases)} 通过")
    
    if success_count == len(test_cases):
        print("🎉 所有测试通过！系统运行正常。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查系统配置。")
        return 1

if __name__ == "__main__":
    exit(main())
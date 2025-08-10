#!/usr/bin/env python3
"""
测试新的病药体系
Test the new illness-medicine system
"""

from bazi_engine_enhanced import BaziEngineEnhanced
from bingyao_system import analyze_bingyao_system, format_bingyao_result, DESTINY_PATTERNS

def test_bingyao_examples():
    """测试病药体系的例子"""
    
    engine = BaziEngineEnhanced()
    
    # 测试案例1: 命旺局 - 君药：伤官，臣药：煞，次药：财
    test_cases = [
        {
            "name": "命旺局测试",
            "bazi": "甲子 甲子 甲子 甲子",  # 全甲木，命旺
            "expected_pattern": "命旺",
            "expected_medicines": {"君药": "伤官", "臣药": "煞", "次药": "财"}
        },
        {
            "name": "印重局测试", 
            "bazi": "壬子 壬子 甲子 甲子",  # 水多生木，印重
            "expected_pattern": "印重",
            "expected_medicines": {"君药": "财", "臣药": "伤官", "次药": "煞"}
        },
        {
            "name": "财旺局测试",
            "bazi": "戊子 戊子 甲子 甲子",  # 土多被木克，财旺
            "expected_pattern": "财旺", 
            "expected_medicines": {"君药": "比肩", "臣药": "印", "次药": "生"}
        }
    ]
    
    print("=" * 60)
    print("病药体系测试结果")
    print("=" * 60)
    
    for case in test_cases:
        print(f"\n【{case['name']}】")
        print(f"测试八字: {case['bazi']}")
        
        try:
            # 解析八字
            chart = engine.parse_bazi_string(case["bazi"])
            
            # 计算五行统计
            element_stats = engine.calculate_element_stats(chart)
            
            # 准备数据格式
            chart_data = {
                "year": str(chart.year),
                "month": str(chart.month),
                "day": str(chart.day), 
                "hour": str(chart.hour)
            }
            
            element_stats_dict = {
                "wood": element_stats.wood,
                "fire": element_stats.fire,
                "earth": element_stats.earth,
                "metal": element_stats.metal,
                "water": element_stats.water
            }
            
            # 病药分析
            bingyao_analysis = analyze_bingyao_system(chart_data, element_stats_dict)
            result = format_bingyao_result(bingyao_analysis)
            
            print(f"实际命局类型: {result['命局类型']}")
            print(f"期望命局类型: {case['expected_pattern']}")
            print(f"匹配结果: {'✓' if result['命局类型'] == case['expected_pattern'] else '✗'}")
            
            print(f"\n病药配置:")
            for level, medicine in result["病药配置"].items():
                expected = case['expected_medicines'].get(level, "未定义")
                match = "✓" if medicine == expected else "✗"
                print(f"  {level}: {medicine} (期望: {expected}) {match}")
            
            print(f"\n能量本质: {result['能量本质']}")
            print(f"关系类型: {result['关系类型']}")
            print(f"意识特质: {result['意识特质']}")
            
            print(f"\n药效分析:")
            for level, effectiveness in result["药效分析"].items():
                print(f"  {level}: {effectiveness}")
                
            print(f"\n五行统计:")
            for element, value in element_stats_dict.items():
                print(f"  {element}: {value}")
                
        except Exception as e:
            print(f"测试失败: {e}")
        
        print("-" * 40)

def test_destiny_patterns_info():
    """展示五大命局的完整信息"""
    
    print("\n" + "=" * 60) 
    print("五大命局病药体系规则")
    print("=" * 60)
    
    for pattern_name, pattern_info in DESTINY_PATTERNS.items():
        print(f"\n【{pattern_name}】")
        print(f"描述: {pattern_info['description']}")
        print(f"君药: {pattern_info['medicines']['君药']}")
        print(f"臣药: {pattern_info['medicines']['臣药']}")
        print(f"次药: {pattern_info['medicines']['次药']}")
        print(f"能量本质: {pattern_info['energy_nature']}")
        print(f"关系: {pattern_info['relationship']}")
        print(f"意识特质: {pattern_info['consciousness']}")

if __name__ == "__main__":
    # 显示规则信息
    test_destiny_patterns_info()
    
    # 运行测试
    test_bingyao_examples()
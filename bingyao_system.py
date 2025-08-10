"""
病药体系 - 基于五大命局的病药突系
Illness-Medicine System based on Five Major Destiny Patterns
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# 十神映射 (Ten Gods Mapping)
TEN_GODS_MAP = {
    "比肩": {"type": "self", "element_relation": "same", "consciousness": "同类帮助、兄弟姐妹、团队朋友"},
    "劫财": {"type": "self", "element_relation": "same", "consciousness": "低气、承载力、社交思维、组织力、担当、果敢、勇气、自大"},
    "食神": {"type": "output", "element_relation": "generates", "consciousness": "思考、理性逻辑、抽象思维、长远规划、规则标准、道理、挑剔、信仰、亲誉、虚荣心、自以为是"},
    "伤官": {"type": "output", "element_relation": "generates", "consciousness": "发散思维、感性、聪明、同理心、直觉感知、创造力、创意、走心感染力、敏感、惰性化"},
    "正财": {"type": "wealth", "element_relation": "destroys", "consciousness": "机会、钱物、落地性、成果意识"},
    "偏财": {"type": "wealth", "element_relation": "destroys", "consciousness": "点式思维、执行力、行动力"},
    "正官": {"type": "authority", "element_relation": "destroyed_by", "consciousness": "危机意识、谨慎、担忧恐惧、严格、压迫、持续力、专注力、技能技术技巧、方法手段"},
    "七杀": {"type": "authority", "element_relation": "destroyed_by", "consciousness": "压力约束、文夫(女)、子女(男)、领导权威"}
}

# 五大命局的病药规则 (Five Major Destiny Patterns' Illness-Medicine Rules)
DESTINY_PATTERNS = {
    "命旺": {
        "description": "命主强旺",
        "pattern_code": "strong_day_master",
        "medicines": {
            "君药": "伤官",  # Chief medicine
            "臣药": "煞",    # Minister medicine  
            "次药": "财"     # Assistant medicine
        },
        "energy_nature": "比肩",
        "relationship": "同类帮助",
        "consciousness": "低气、承载力、社交思维、组织力、担当、果敢、勇气、自大"
    },
    
    "印重": {
        "description": "印星过重",
        "pattern_code": "heavy_seal",
        "medicines": {
            "君药": "财",    # Chief medicine
            "臣药": "伤官", # Minister medicine
            "次药": "煞"     # Assistant medicine  
        },
        "energy_nature": "印",
        "relationship": "安全感、母亲、长辈、师长",
        "consciousness": "思考、理性逻辑、抽象思维、长远规划、规则标准、道理、挑剔、信仰、亲誉、虚荣心、自以为是"
    },
    
    "财旺": {
        "description": "财星过旺",
        "pattern_code": "strong_wealth", 
        "medicines": {
            "君药": "比肩",  # Chief medicine
            "臣药": "印",    # Minister medicine
            "次药": "生"     # Assistant medicine
        },
        "energy_nature": "财",
        "relationship": "短期成果、妻子(男)、父亲",
        "consciousness": "机会、钱物、落地性、成果意识、点式思维、执行力、行动力"
    },
    
    "煞重": {
        "description": "七杀过重", 
        "pattern_code": "heavy_authority",
        "medicines": {
            "君药": "印",    # Chief medicine
            "臣药": "比肩", # Minister medicine
            "次药": "扶"     # Assistant medicine
        },
        "energy_nature": "煞",
        "relationship": "压力约束、文夫(女)、子女(男)、领导权威",
        "consciousness": "危机意识、谨慎、担忧恐惧、严格、压迫、持续力、专注力、技能技术技巧、方法手段"
    },
    
    "伤官": {
        "description": "伤官当令",
        "pattern_code": "strong_injury_officer",
        "medicines": {
            "君药": "印",    # Chief medicine
            "臣药": "比肩", # Minister medicine  
            "次药": "扶"     # Assistant medicine
        },
        "energy_nature": "伤官",
        "relationship": "生发、孩子(女)",
        "consciousness": "发散思维、感性、聪明、同理心、直觉感知、创造力、创意、走心感染力、敏感、惰性化"
    }
}

# 十神与天干地支的对应关系
def determine_ten_god(day_gan: str, other_gan: str) -> str:
    """
    根据日干和其他天干确定十神关系
    """
    from bazi_engine_enhanced import TIAN_GAN_PROPS
    
    day_element = TIAN_GAN_PROPS[day_gan]["element"]
    other_element = TIAN_GAN_PROPS[other_gan]["element"] 
    day_yin_yang = TIAN_GAN_PROPS[day_gan]["yin_yang"]
    other_yin_yang = TIAN_GAN_PROPS[other_gan]["yin_yang"]
    
    # 五行生克关系
    element_relations = {
        "wood": {"generates": "fire", "destroys": "earth", "generated_by": "water", "destroyed_by": "metal"},
        "fire": {"generates": "earth", "destroys": "metal", "generated_by": "wood", "destroyed_by": "water"},
        "earth": {"generates": "metal", "destroys": "water", "generated_by": "fire", "destroyed_by": "wood"},
        "metal": {"generates": "water", "destroys": "wood", "generated_by": "earth", "destroyed_by": "fire"},
        "water": {"generates": "wood", "destroys": "fire", "generated_by": "metal", "destroyed_by": "earth"},
    }
    
    if day_element == other_element:
        # 同五行
        if day_yin_yang == other_yin_yang:
            return "比肩"
        else:
            return "劫财"
    elif other_element == element_relations[day_element]["generates"]:
        # 日干生其他干
        if day_yin_yang == other_yin_yang:
            return "食神"
        else:
            return "伤官"
    elif other_element == element_relations[day_element]["destroys"]:
        # 日干克其他干
        if day_yin_yang == other_yin_yang:
            return "偏财"
        else:
            return "正财"
    elif other_element == element_relations[day_element]["generated_by"]:
        # 其他干生日干
        if day_yin_yang == other_yin_yang:
            return "偏印"
        else:
            return "正印"
    elif other_element == element_relations[day_element]["destroyed_by"]:
        # 其他干克日干
        if day_yin_yang == other_yin_yang:
            return "七杀"
        else:
            return "正官"
    else:
        return "未知"

@dataclass
class BingYaoAnalysis:
    """病药分析结果"""
    pattern_type: str           # 命局类型
    pattern_description: str    # 命局描述
    chief_medicine: str         # 君药
    minister_medicine: str      # 臣药
    assistant_medicine: str     # 次药
    energy_nature: str          # 能量本质
    relationship: str           # 关系类型
    consciousness: str          # 意识特质
    strength_analysis: Dict[str, Any]  # 强度分析
    medicine_effectiveness: Dict[str, str]  # 药效分析

def analyze_destiny_pattern(chart_data: Dict[str, Any], element_stats: Dict[str, float]) -> str:
    """
    根据八字盘和五行统计判定命局类型
    """
    day_gan = chart_data["day"][0]  # 日干
    
    # 获取日干五行
    from bazi_engine_enhanced import TIAN_GAN_PROPS
    day_element = TIAN_GAN_PROPS[day_gan]["element"]
    day_strength = element_stats.get(day_element, 0)
    
    # 获取各种十神的力量
    ten_god_strength = {}
    pillars = [chart_data["year"], chart_data["month"], chart_data["hour"]]  # 除了日柱
    
    for pillar_str in pillars:
        gan = pillar_str[0]
        ten_god = determine_ten_god(day_gan, gan)
        if ten_god not in ten_god_strength:
            ten_god_strength[ten_god] = 0
        ten_god_strength[ten_god] += 1
    
    # 判定逻辑
    if day_strength >= 3.0:
        return "命旺"
    elif ten_god_strength.get("正印", 0) + ten_god_strength.get("偏印", 0) >= 2:
        return "印重"
    elif ten_god_strength.get("正财", 0) + ten_god_strength.get("偏财", 0) >= 2:
        return "财旺"
    elif ten_god_strength.get("七杀", 0) >= 2:
        return "煞重"
    elif ten_god_strength.get("伤官", 0) >= 2:
        return "伤官"
    else:
        # 默认按最强的十神判定
        max_ten_god = max(ten_god_strength.items(), key=lambda x: x[1], default=("命旺", 0))[0]
        if "印" in max_ten_god:
            return "印重"
        elif "财" in max_ten_god:
            return "财旺" 
        elif "杀" in max_ten_god or "官" in max_ten_god:
            return "煞重"
        elif "伤官" in max_ten_god:
            return "伤官"
        else:
            return "命旺"

def analyze_bingyao_system(chart_data: Dict[str, Any], element_stats: Dict[str, float]) -> BingYaoAnalysis:
    """
    基于新规则的病药体系分析
    """
    # 判定命局类型
    pattern_type = analyze_destiny_pattern(chart_data, element_stats)
    pattern_info = DESTINY_PATTERNS[pattern_type]
    
    # 分析各十神在盘中的实际力量
    day_gan = chart_data["day"][0]
    all_gans = [chart_data[pillar][0] for pillar in ["year", "month", "day", "hour"]]
    
    ten_god_analysis = {}
    for gan in all_gans:
        ten_god = determine_ten_god(day_gan, gan)
        if ten_god not in ten_god_analysis:
            ten_god_analysis[ten_god] = {"count": 0, "positions": []}
        ten_god_analysis[ten_god]["count"] += 1
        ten_god_analysis[ten_god]["positions"].append(gan)
    
    # 评估药效
    medicines = pattern_info["medicines"]
    medicine_effectiveness = {}
    
    for medicine_level, ten_god in medicines.items():
        if ten_god in ten_god_analysis:
            count = ten_god_analysis[ten_god]["count"]
            if count >= 2:
                effectiveness = "药力充足"
            elif count == 1:
                effectiveness = "药力一般"
            else:
                effectiveness = "药力不足"
        else:
            effectiveness = "缺药"
        medicine_effectiveness[medicine_level] = f"{ten_god}({effectiveness})"
    
    return BingYaoAnalysis(
        pattern_type=pattern_type,
        pattern_description=pattern_info["description"],
        chief_medicine=medicines["君药"],
        minister_medicine=medicines["臣药"],
        assistant_medicine=medicines["次药"],
        energy_nature=pattern_info["energy_nature"],
        relationship=pattern_info["relationship"],
        consciousness=pattern_info["consciousness"],
        strength_analysis=ten_god_analysis,
        medicine_effectiveness=medicine_effectiveness
    )

def format_bingyao_result(analysis: BingYaoAnalysis) -> Dict[str, Any]:
    """
    格式化病药分析结果
    """
    return {
        "命局类型": analysis.pattern_type,
        "命局描述": analysis.pattern_description,
        "病药配置": {
            "君药": analysis.chief_medicine,
            "臣药": analysis.minister_medicine, 
            "次药": analysis.assistant_medicine
        },
        "能量本质": analysis.energy_nature,
        "关系类型": analysis.relationship,
        "意识特质": analysis.consciousness,
        "药效分析": analysis.medicine_effectiveness,
        "十神分布": analysis.strength_analysis
    }
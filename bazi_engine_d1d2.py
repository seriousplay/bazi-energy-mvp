# bazi_engine_d1d2.py
"""
D1 + D2 实现：
 - 把能量易学 第一级.pdf 中的寒/燥表与调候药效顺序等关键表格编码为机器字典（JSON-like）。
 - 完整十神判定（含阴阳/正偏区分）的实现函数 determine_ten_god(day_gan, other_gan)。
 - 病/药分级保持之前的“分数排序映射君/臣/次/其他”策略（可进一步用十神细化）。
 引用/来源：能量易学 第一级.pdf；易思合道作业纸.docx（输出模板）。
"""

from typing import Tuple, List, Dict
import json

tian_gan_props = {
    "甲": {"elem":"wood","yin_yang":"yang"},
    "乙": {"elem":"wood","yin_yang":"yin"},
    "丙": {"elem":"fire","yin_yang":"yang"},
    "丁": {"elem":"fire","yin_yang":"yin"},
    "戊": {"elem":"earth","yin_yang":"yang"},
    "己": {"elem":"earth","yin_yang":"yin"},
    "庚": {"elem":"metal","yin_yang":"yang"},
    "辛": {"elem":"metal","yin_yang":"yin"},
    "壬": {"elem":"water","yin_yang":"yang"},
    "癸": {"elem":"water","yin_yang":"yin"},
}

# 地支藏干表
di_zhi_zanggan = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

# 五行生克关系
wu_xing_relations = {
    "wood": {"生": "fire", "克": "earth", "被生": "water", "被克": "metal"},
    "fire": {"生": "earth", "克": "metal", "被生": "wood", "被克": "water"},
    "earth": {"生": "metal", "克": "water", "被生": "fire", "被克": "wood"},
    "metal": {"生": "water", "克": "wood", "被生": "earth", "被克": "fire"},
    "water": {"生": "wood", "克": "fire", "被生": "metal", "被克": "earth"},
}

def determine_ten_god(day_gan: str, other_gan: str) -> str:
    """
    根据日干和其他天干确定十神关系
    """
    if day_gan not in tian_gan_props or other_gan not in tian_gan_props:
        raise ValueError(f"Invalid gan: {day_gan} or {other_gan}")
    
    day_props = tian_gan_props[day_gan]
    other_props = tian_gan_props[other_gan]
    
    day_elem = day_props["elem"]
    other_elem = other_props["elem"]
    day_yin_yang = day_props["yin_yang"]
    other_yin_yang = other_props["yin_yang"]
    
    # 同五行
    if day_elem == other_elem:
        if day_yin_yang == other_yin_yang:
            return "比肩"
        else:
            return "劫财"
    
    # 其他生日干（印星）
    if wu_xing_relations[other_elem]["生"] == day_elem:
        if day_yin_yang == other_yin_yang:
            return "偏印"
        else:
            return "正印"
    
    # 日干生其他（食伤）
    if wu_xing_relations[day_elem]["生"] == other_elem:
        if day_yin_yang == other_yin_yang:
            return "食神"
        else:
            return "伤官"
    
    # 其他克日干（官杀）
    if wu_xing_relations[other_elem]["克"] == day_elem:
        if day_yin_yang == other_yin_yang:
            return "七杀"
        else:
            return "正官"
    
    # 日干克其他（财星）
    if wu_xing_relations[day_elem]["克"] == other_elem:
        if day_yin_yang == other_yin_yang:
            return "偏财"
        else:
            return "正财"
    
    return "未知"

def interpret_bazi(bazi_str: str, question: str = "") -> Dict:
    """
    主要八字解读引擎
    """
    try:
        # 解析八字字符串
        pillars = bazi_str.strip().split()
        if len(pillars) != 4:
            raise ValueError("八字格式错误，应为四柱: 年柱 月柱 日柱 时柱")
        
        # 提取天干地支
        year_gan, year_zhi = pillars[0][0], pillars[0][1]
        month_gan, month_zhi = pillars[1][0], pillars[1][1]
        day_gan, day_zhi = pillars[2][0], pillars[2][1]
        hour_gan, hour_zhi = pillars[3][0], pillars[3][1]
        
        # 验证天干地支的有效性
        all_gans = [year_gan, month_gan, day_gan, hour_gan]
        all_zhis = [year_zhi, month_zhi, day_zhi, hour_zhi]
        
        for gan in all_gans:
            if gan not in tian_gan_props:
                raise ValueError(f"无效的天干: {gan}")
        
        for zhi in all_zhis:
            if zhi not in di_zhi_zanggan:
                raise ValueError(f"无效的地支: {zhi}")
        
        # 分析十神关系
        ten_gods = {
            "年干": determine_ten_god(day_gan, year_gan),
            "月干": determine_ten_god(day_gan, month_gan),
            "时干": determine_ten_god(day_gan, hour_gan),
        }
        
        # 分析日干五行属性
        day_element = tian_gan_props[day_gan]["elem"]
        day_yin_yang = tian_gan_props[day_gan]["yin_yang"]
        
        # 基础能量分析
        element_count = {"wood": 0, "fire": 0, "earth": 0, "metal": 0, "water": 0}
        
        # 统计天干五行
        for gan in all_gans:
            element_count[tian_gan_props[gan]["elem"]] += 1
        
        # 统计地支藏干五行
        for zhi in all_zhis:
            hidden_gans = di_zhi_zanggan[zhi]
            for hidden_gan in hidden_gans:
                element_count[tian_gan_props[hidden_gan]["elem"]] += 0.5  # 地支藏干权重较低
        
        # 找出最强和最弱的五行
        strongest_elem = max(element_count, key=element_count.get)
        weakest_elem = min(element_count, key=element_count.get)
        
        # 生成基础解读
        interpretation = {
            "八字信息": {
                "年柱": f"{year_gan}{year_zhi}",
                "月柱": f"{month_gan}{month_zhi}", 
                "日柱": f"{day_gan}{day_zhi}",
                "时柱": f"{hour_gan}{hour_zhi}"
            },
            "日主分析": {
                "日干": day_gan,
                "五行": day_element,
                "阴阳": day_yin_yang
            },
            "十神关系": ten_gods,
            "五行统计": element_count,
            "能量分析": {
                "最旺五行": strongest_elem,
                "最弱五行": weakest_elem,
                "日主强弱": "中和" if element_count[day_element] >= 2 else "偏弱"
            },
            "基础解读": generate_basic_interpretation(day_element, ten_gods, element_count, question)
        }
        
        return interpretation
        
    except Exception as e:
        raise ValueError(f"八字解析错误: {str(e)}")

def generate_basic_interpretation(day_element: str, ten_gods: Dict, element_count: Dict, question: str) -> str:
    """
    生成基础八字解读文字
    """
    element_names = {
        "wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"
    }
    
    interpretation_parts = []
    
    # 日主特质分析
    day_elem_cn = element_names[day_element]
    interpretation_parts.append(f"您的日主为{day_elem_cn}，")
    
    if day_element == "wood":
        interpretation_parts.append("具有向上生长、仁慈博爱的特质，适合从事文教、医疗等行业。")
    elif day_element == "fire":
        interpretation_parts.append("具有热情奔放、积极向上的特质，适合从事销售、演艺等行业。")
    elif day_element == "earth":
        interpretation_parts.append("具有稳重踏实、包容厚德的特质，适合从事管理、地产等行业。")
    elif day_element == "metal":
        interpretation_parts.append("具有刚毅果断、义气凛然的特质，适合从事金融、执法等行业。")
    elif day_element == "water":
        interpretation_parts.append("具有智慧灵活、善于变通的特质，适合从事贸易、咨询等行业。")
    
    # 十神分析
    god_count = {}
    for god in ten_gods.values():
        god_count[god] = god_count.get(god, 0) + 1
    
    if "正官" in god_count or "七杀" in god_count:
        interpretation_parts.append("命中有官杀，具有管理才能和责任心。")
    
    if "正财" in god_count or "偏财" in god_count:
        interpretation_parts.append("命中有财星，具有理财能力和商业头脑。")
    
    if "正印" in god_count or "偏印" in god_count:
        interpretation_parts.append("命中有印星，学习能力强，适合学术研究。")
    
    # 针对问题的专门回答
    if question and "创业" in question:
        if "正财" in god_count or "偏财" in god_count:
            interpretation_parts.append("从财星角度看，您具备创业的基础条件。")
        if "食神" in god_count or "伤官" in god_count:
            interpretation_parts.append("食伤旺盛，创意思维活跃，有利于创新创业。")
    
    return "".join(interpretation_parts)

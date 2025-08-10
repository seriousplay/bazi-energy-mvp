"""
LLM Integration Module for Natural Language Interpretation
LLM集成模块：将结构化分析结果转换为自然语言解读
"""

import json
from typing import Dict, Any, Optional
import os
from dataclasses import dataclass

@dataclass
class InterpretationRequest:
    """解读请求"""
    structured_result: Dict[str, Any]
    user_question: str
    user_info: Optional[Dict[str, Any]] = None
    mode: str = "general"  # general/expert/detailed

class LLMInterpreter:
    """LLM解读器"""
    
    def __init__(self):
        self.element_names = {
            "wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"
        }
        
        self.element_traits = {
            "wood": "向上生长、仁慈博爱、创新进取",
            "fire": "热情奔放、积极向上、善于表达",
            "earth": "稳重踏实、包容厚德、务实可靠",
            "metal": "刚毅果断、义气凛然、理性决断",
            "water": "智慧灵活、善于变通、深沉内敛"
        }
        
        self.geju_interpretations = {
            "比劫旺格": "同类力量强，具有坚强意志和独立性格，适合创业或独当一面的工作",
            "印星旺格": "学习能力强，贵人运好，适合学术、教育或需要持续学习的行业",
            "食伤旺格": "创意思维活跃，表达能力强，适合创新、艺术或自媒体相关工作",
            "财星旺格": "理财能力强，商业头脑敏锐，适合商业、投资或财务相关工作",
            "官杀旺格": "管理才能突出，责任心强，适合管理、公职或需要威权的工作"
        }
    
    def generate_energy_portrait(self, result: Dict[str, Any]) -> str:
        """生成有画面感的隐喻能量画像"""
        bazi_info = result["bazi"]
        wuxing = result["五行统计"]
        geju = result["定格局"]
        hanzao = result["定寒燥"]
        
        # 解析日主
        day_pillar = bazi_info["day"]
        day_gan = day_pillar[0]  # 日干
        day_element = self._get_element_from_gan(day_gan)
        
        # 获取命局特征
        geju_type = geju["格局类型"]
        geju_strength = geju["强弱"]
        strongest = wuxing["最旺"]
        weakest = wuxing["最弱"]
        hanzao_type = hanzao["类型"]
        
        # 生成隐喻画像
        metaphor = self._generate_metaphor(
            day_element=day_element,
            day_gan=day_gan,
            geju_type=geju_type,
            geju_strength=geju_strength,
            strongest=strongest,
            weakest=weakest,
            hanzao_type=hanzao_type,
            wuxing=wuxing
        )
        
        return metaphor
    
    def _get_element_from_gan(self, gan: str) -> str:
        """根据天干获取五行"""
        gan_element_map = {
            "甲": "wood", "乙": "wood",
            "丙": "fire", "丁": "fire", 
            "戊": "earth", "己": "earth",
            "庚": "metal", "辛": "metal",
            "壬": "water", "癸": "water"
        }
        return gan_element_map.get(gan, "earth")
    
    def _generate_metaphor(self, day_element, day_gan, geju_type, geju_strength, 
                          strongest, weakest, hanzao_type, wuxing) -> str:
        """根据五行组合生成隐喻画像"""
        
        # 核心隐喻模板库
        metaphor_templates = {
            # 水性隐喻 - 智慧、变通、深沉
            ("water", "强", "比劫旺格"): [
                "一条奔腾的大河，水势浩荡但尚未找到最佳的入海口。",
                "深海中的蓝鲸，拥有巨大的智慧和力量，但仍在寻找属于自己的深度。",
                "山间的瀑布，水流湍急而有力，正等待合适的时机汇入更大的江河。"
            ],
            ("water", "弱", "印星旺格"): [
                "清澈的山泉，虽然细小但源源不断，正在积蓄力量准备奔流。",
                "池塘中的荷花，根系深扎水底，等待适当时机绽放出惊人的美丽。"
            ],
            ("water", "中", "食伤旺格"): [
                "智慧的溪流，曲折婉转地流过山谷，将滋养沿途的每一寸土地。"
            ],
            
            # 木性隐喻 - 成长、创新、向上
            ("wood", "强", "比劫旺格"): [
                "参天大树，根深叶茂但枝干过于繁茂，需要适当修剪才能结出最好的果实。",
                "茂密的森林，生命力旺盛但需要阳光透过林间，照亮前进的道路。"
            ],
            ("wood", "弱", "印星旺格"): [
                "春天的嫩芽，虽然柔弱但充满生机，正等待雨露的滋养破土而出。",
                "盆景中的幼松，虽小但已显现出将来的挺拔姿态。"
            ],
            
            # 火性隐喻 - 热情、表达、光明
            ("fire", "强", "比劫旺格"): [
                "熊熊燃烧的篝火，光芒四射但需要找到更多可以点亮的灯火。",
                "太阳般的热情，光热充足但需要找到最适合照耀的大地。"
            ],
            ("fire", "弱", "印星旺格"): [
                "黎明前的第一缕阳光，温和而珍贵，正准备唤醒整个世界。",
                "烛火般的坚持，光芒不大但足以照亮身边最重要的人。"
            ],
            
            # 土性隐喻 - 稳重、包容、务实  
            ("earth", "强", "比劫旺格"): [
                "深厚的大地，承载力强大但需要找到最值得培育的种子。",
                "稳固的山峰，巍峨不动但等待着成为他人攀登的基石。"
            ],
            ("earth", "弱", "印星旺格"): [
                "肥沃的土壤，虽然谦逊低调，但正在孕育着惊人的生命力。"
            ],
            
            # 金性隐喻 - 理性、决断、坚韧
            ("metal", "强", "比劫旺格"): [
                "锋利的宝剑，削铁如泥但还需要找到最值得守护的事物。",
                "精钢般的意志，坚硬无比但需要合适的锻造才能成器。"
            ],
            ("metal", "弱", "印星旺格"): [
                "待磨砺的璞玉，虽未成型但已蕴含着令人惊艳的光华。",
                "深藏的宝矿，等待着慧眼识珠的人来发掘其真正价值。"
            ]
        }
        
        # 根据寒燥调候添加情境修饰
        climate_modifiers = {
            "寒重": "在凛冽的寒风中",
            "微寒": "在清冷的秋夜里", 
            "燥重": "在炽热的沙漠中",
            "微燥": "在温暖的午后阳光下",
            "平和": "在四季如春的环境中"
        }
        
        # 生成基础隐喻
        key = (day_element, geju_strength, geju_type)
        base_metaphors = metaphor_templates.get(key, [])
        
        # 如果没有精确匹配，用通用规则生成
        if not base_metaphors:
            base_metaphors = self._generate_fallback_metaphor(
                day_element, geju_strength, day_gan
            )
        
        # 选择最合适的隐喻
        chosen_metaphor = base_metaphors[0] if base_metaphors else "独特的能量组合，正在寻找属于自己的表达方式。"
        
        # 添加情境修饰
        climate_modifier = climate_modifiers.get(hanzao_type, "")
        if climate_modifier:
            chosen_metaphor = f"{climate_modifier}，{chosen_metaphor}"
        
        return chosen_metaphor
    
    def _generate_fallback_metaphor(self, element, strength, gan) -> list:
        """生成备用隐喻"""
        element_base = {
            "water": "智慧的江河",
            "wood": "生长的树木", 
            "fire": "跳动的火焰",
            "earth": "厚重的大地",
            "metal": "坚韧的金石"
        }
        
        strength_modifier = {
            "强": "力量充沛但需要找到合适的方向",
            "弱": "蓄势待发，等待适当的时机绽放",
            "中": "能量均衡，正在寻找最佳的表达方式"
        }
        
        base = element_base.get(element, "独特的能量")
        modifier = strength_modifier.get(strength, "正在探索自己的道路")
        
        return [f"{base}，{modifier}。"]
    
    def generate_question_answer(self, result: Dict[str, Any], question: str) -> str:
        """针对具体问题生成回答"""
        if not question or question.strip() == "":
            return ""
        
        question = question.strip()
        geju = result["定格局"]
        bingyao = result["定病药"]
        dayun = result["看大运"]
        hanzao = result["定寒燥"]
        
        answer_parts = []
        answer_parts.append(f"针对您的问题「{question}」，基于您的八字分析：")
        
        # 根据问题类型给出不同建议
        if any(keyword in question for keyword in ["创业", "生意", "投资", "赚钱", "财富"]):
            # 财运相关问题
            answer_parts.append("\n**财富发展分析：**")
            
            # 检查财星情况
            财星力量 = 0
            for item in bingyao["分级"]:
                if item["element"] in ["earth", "metal"] and item["level"] in ["君", "臣"]:  # 简化的财星判定
                    财星力量 += 1
            
            if 财星力量 > 0:
                answer_parts.append("- 命中财星有力，具备理财和商业头脑的基础")
                answer_parts.append("- 建议选择与您五行喜用相符的行业方向")
            else:
                answer_parts.append("- 命中财星较弱，建议通过专业技能和服务创造价值")
                answer_parts.append("- 可考虑合伙经营或依托平台发展")
            
            # 大运影响
            current_dayun = dayun["当前大运"]
            answer_parts.append(f"- 当前大运({current_dayun['age_range']})：{current_dayun['influence']}")
            
        elif any(keyword in question for keyword in ["工作", "职业", "事业", "升职", "跳槽"]):
            # 事业相关问题
            answer_parts.append("\n**事业发展建议：**")
            
            geju_type = geju["格局类型"] 
            if "印星" in geju_type:
                answer_parts.append("- 适合教育培训、文化传媒、学术研究等需要持续学习的行业")
            elif "食伤" in geju_type:
                answer_parts.append("- 适合创意设计、艺术创作、自媒体等需要表达创新的工作")
            elif "官杀" in geju_type:
                answer_parts.append("- 适合管理职位、公务员、律师等需要威权和责任心的职业")
            elif "财星" in geju_type:
                answer_parts.append("- 适合商业贸易、金融投资、销售等与财富直接相关的工作")
            else:
                answer_parts.append("- 适合发挥个人专长，选择能体现自主性的工作环境")
            
        elif any(keyword in question for keyword in ["健康", "身体", "养生", "调理"]):
            # 健康相关问题
            answer_parts.append("\n**健康调养建议：**")
            
            hanzao_type = hanzao["类型"]
            need_element = hanzao["需要调候"]
            
            if "寒" in hanzao_type and need_element == "fire":
                answer_parts.append("- 体质偏寒，建议多接触阳光，适量运动增加阳气")
                answer_parts.append("- 饮食上可选择温热性食物，避免过多寒凉")
            elif "燥" in hanzao_type and need_element == "water":
                answer_parts.append("- 体质偏燥，建议多补充水分，保持作息规律")
                answer_parts.append("- 环境上宜选择湿润清净之处，避免过度燥热")
            else:
                answer_parts.append("- 体质相对平和，注意保持五行平衡的生活方式")
            
            answer_parts.append("- **免责声明：以上建议基于传统命理分析，不替代专业医疗意见**")
            
        elif any(keyword in question for keyword in ["感情", "婚姻", "恋爱", "配偶", "对象"]):
            # 感情相关问题
            answer_parts.append("\n**感情关系分析：**")
            
            # 简化的感情分析
            answer_parts.append("- 基于您的五行特质，在感情中展现出相应的性格特点")
            answer_parts.append("- 建议寻找能与您五行互补或相生的伴侣类型")
            answer_parts.append("- 重要时机可参考大运流年的影响")
            
        else:
            # 通用回答
            answer_parts.append("\n**综合建议：**")
            answer_parts.append("- 发挥您的五行优势，补强相对薄弱的方面")
            answer_parts.append("- 关注大运流年的变化时机，顺势而为")
            answer_parts.append("- 保持身心平衡，注意调候养生")
        
        # 时间维度建议
        answer_parts.append("\n**时机分析：**")
        current_dayun = dayun["当前大运"]
        answer_parts.append(f"- 短期({current_dayun['age_range']}岁)：{current_dayun['influence']}")
        
        if dayun["未来大运"]:
            next_dayun = dayun["未来大运"][0]
            answer_parts.append(f"- 中期({next_dayun['age_range']}岁)：{next_dayun['influence']}")
        
        return "".join(answer_parts)
    
    def generate_practice_suggestions(self, result: Dict[str, Any]) -> str:
        """生成调候练习建议"""
        hanzao = result["定寒燥"]
        need_element = hanzao["需要调候"]
        
        if need_element == "none":
            return "您的命局五行较为平衡，建议保持规律作息，适度运动，维持身心和谐即可。"
        
        suggestions = []
        suggestions.append("**调候练习建议：**")
        
        if need_element == "fire":
            suggestions.extend([
                "- **时间选择**：上午9-11点（巳时），下午1-3点（午时）进行重要活动",
                "- **方向选择**：多面向南方，居住工作环境采用暖色调",
                "- **活动建议**：适量运动发汗，练习太极或瑜伽等舒缓功法",
                "- **心理调节**：保持积极乐观心态，多与热情开朗的人接触"
            ])
        elif need_element == "water":
            suggestions.extend([
                "- **时间选择**：晚上9-11点（亥时），夜间11-1点（子时）进行冥想休息",
                "- **方向选择**：多面向北方，环境宜选择安静清净之处",
                "- **活动建议**：游泳、散步、静坐等舒缓活动，避免过度激烈运动",
                "- **心理调节**：培养内观智慧，学会在宁静中思考和决策"
            ])
        elif need_element == "wood":
            suggestions.extend([
                "- **时间选择**：早晨5-7点（卯时），春季时节多户外活动",
                "- **方向选择**：多面向东方，环境中增加绿植和自然元素",
                "- **活动建议**：接触大自然，园艺活动，学习新技能",
                "- **心理调节**：保持成长心态，设定发展目标并循序渐进"
            ])
        elif need_element == "metal":
            suggestions.extend([
                "- **时间选择**：下午3-7点（申酉时），秋季时节注意收敛",
                "- **方向选择**：多面向西方，环境简洁有序，金属装饰适量",
                "- **活动建议**：规律作息，练习书法或乐器等需要专注的技艺",
                "- **心理调节**：培养理性思维和决断力，学会舍弃和取舍"
            ])
        elif need_element == "earth":
            suggestions.extend([
                "- **时间选择**：季月之末（辰戌丑未时），四季交替时注意调养",
                "- **方向选择**：中央方位，环境稳定温和，土黄色调",
                "- **活动建议**：规律饮食，适量户外活动，培养耐心和专注",
                "- **心理调节**：保持包容心态，注重实际行动胜过空想"
            ])
        
        suggestions.append("\n**重要提醒**：以上建议基于传统五行调候理论，旨在帮助达到身心平衡，请结合个人实际情况适度调整，不构成医疗建议。")
        
        return "\n".join(suggestions)
    
    def generate_expert_analysis(self, result: Dict[str, Any]) -> str:
        """生成专家分析模式内容"""
        expert_data = result["专家模式数据"]
        
        analysis_parts = []
        analysis_parts.append("## 专家分析详情")
        analysis_parts.append(f"**规则依据：** {expert_data['规则依据']}")
        analysis_parts.append(f"**判定优先级：** {' > '.join(expert_data['判定优先级'])}")
        analysis_parts.append(f"**引擎版本：** {expert_data['审计信息']}")
        
        analysis_parts.append("\n### 详细判定过程：")
        
        # 格局判定详情
        geju = result["定格局"]
        analysis_parts.append(f"**格局判定：** {geju['格局类型']} | 强弱：{geju['强弱']} | 根：{geju['根']}")
        analysis_parts.append(f"**扶抑关系：** {geju['扶抑关系']}")
        
        # 寒燥判定详情
        hanzao = result["定寒燥"]
        analysis_parts.append(f"**寒燥判定：** {hanzao['类型']} | 原因：{hanzao['原因']}")
        if hanzao["调候药效顺序"]:
            analysis_parts.append(f"**调候顺序：** {' > '.join(hanzao['调候药效顺序'])}")
        
        # 病药分级详情
        analysis_parts.append("\n**病药分级表：**")
        for item in result["定病药"]["分级"]:
            analysis_parts.append(f"- {item['level']}药：{item['element_cn']}（{item['has']}/{item['prosperity']}，{item['consciousness']}）")
        
        # 大运分析
        analysis_parts.append(f"\n**大运分析：** 当前{result['看大运']['当前大运']['age_range']}岁大运")
        
        return "\n".join(analysis_parts)
    
    def comprehensive_interpretation(self, request: InterpretationRequest) -> Dict[str, str]:
        """综合解读生成"""
        result = request.structured_result
        
        interpretation = {}
        
        # 1. 能量画像
        interpretation["energy_portrait"] = self.generate_energy_portrait(result)
        
        # 2. 问题回答
        interpretation["question_answer"] = self.generate_question_answer(result, request.user_question)
        
        # 3. 调候建议
        interpretation["practice_suggestions"] = self.generate_practice_suggestions(result)
        
        # 4. 专家分析（如果是专家模式）
        if request.mode == "expert":
            interpretation["expert_analysis"] = self.generate_expert_analysis(result)
        
        # 5. 免责声明
        interpretation["disclaimer"] = (
            "**免责声明：** 本解读基于传统命理学和能量易学理论，"
            "旨在提供人生参考和思维启发，不构成医疗、法律、投资等专业建议。"
            "重要决策请咨询相关领域专业人士。结果仅供参考，请理性对待。"
        )
        
        return interpretation

# 主要接口函数
def generate_natural_language_interpretation(
    structured_result: Dict[str, Any], 
    user_question: str = "",
    mode: str = "general"
) -> Dict[str, str]:
    """生成自然语言解读"""
    interpreter = LLMInterpreter()
    request = InterpretationRequest(
        structured_result=structured_result,
        user_question=user_question,
        mode=mode
    )
    return interpreter.comprehensive_interpretation(request)
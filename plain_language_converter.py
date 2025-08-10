"""
大白话转换引擎
Plain Language Converter

功能：
1. 将专业命理术语转化为通俗易懂的生活语言
2. 用具体的生活场景替代抽象概念
3. 将命理分析转化为心理和行为描述
4. 确保所有用户都能理解解读内容
"""

from typing import Dict, Any, List, Optional
import re

class PlainLanguageConverter:
    """大白话转换引擎"""
    
    def __init__(self):
        # 专业术语到生活语言的映射
        self.terminology_mapping = {
            # 格局类型
            "比肩旺": "天生不服输，喜欢掌控主动权",
            "劫财旺": "团队合作能力强，但有时容易与人竞争",
            "印重": "安全感需求强，喜欢稳定和被认可",
            "正印": "学习能力强，容易获得长辈喜爱",
            "偏印": "思维独特，喜欢另辟蹊径",
            "财旺": "目标导向，善于把想法变成现实",
            "正财": "做事踏实，追求稳定的收入",
            "偏财": "机会意识强，敢于冒险投资",
            "煞重": "责任心强，在压力下反而能发挥更好",
            "正官": "规则意识强，适合稳定的工作环境",
            "七杀": "承压能力强，适合有挑战的工作",
            "伤官旺": "创意十足，不喜欢被条条框框限制",
            "食神": "思考能力强，善于长远规划",
            
            # 特殊格局
            "从财": "善于借力打力，懂得与环境合作共赢",
            "从杀": "在规则和约束中反而能找到自己的位置",
            "从印": "学习能力超强，容易获得他人支持",
            "从儿": "创造力丰富，适合自由发挥的环境",
            "化气格": "专注力强，容易在某个领域深度发展",
            "专旺格": "某方面能力特别突出，但需要平衡发展",
            "无根局": "灵活性强，但需要找到稳定的支撑",
            "虚透格": "想法很多，但需要加强行动力",
            
            # 强弱描述
            "旺": "能量充足，活力满满",
            "强": "底气足，有自信",
            "弱": "比较敏感，需要更多支持",
            "极旺": "能量过盛，需要适当释放",
            "极弱": "能量不足，需要好好休养",
            
            # 五行元素
            "木旺": "生命力旺盛，总想尝试新事物",
            "火旺": "热情洋溢，很有感染力",
            "土旺": "踏实稳重，让人有安全感",
            "金旺": "原则性强，做事有条理",
            "水旺": "聪明灵活，适应能力强",
            
            # 调候描述
            "寒重": "内心比较安静，需要更多温暖和激励",
            "燥重": "容易急躁，需要保持内心平静",
            "偏寒": "有时候缺乏行动力，需要适当的推动",
            "偏燥": "有时候比较急性子，需要学会耐心",
            "平和": "性格比较温和，能量相对平衡",
            
            # 根的状态
            "有明根": "基础很扎实，有稳定的支撑",
            "有藏根": "虽然表面看不出来，但内在很有实力",
            "无根": "比较灵活，但需要外界的支持",
            
            # 扶抑关系  
            "扶抑格": "需要平衡发展，既要发挥优势也要补足不足",
            "从格": "顺势而为，借助外力发展",
            "化格": "专注于某个方向深度发展"
        }
        
        # 生活场景映射
        self.life_scenarios = {
            "比肩旺": [
                "在团队会议上，您总是那个提出不同意见的人",
                "做决定时，您更相信自己的判断而不是大众的选择",
                "朋友找您商量事情，因为您敢说真话"
            ],
            "印重": [
                "您喜欢把事情研究透彻了再行动",
                "购买东西前会看很多评价和攻略",
                "遇到问题时习惯先咨询专家或查资料"
            ],
            "财旺": [
                "您做任何事都会先考虑这能带来什么收获",
                "您很善于发现生活中的商机和机会",
                "您的朋友都觉得您很有生意头脑"
            ],
            "煞重": [
                "您是那种'答应了就一定要做到'的人",
                "在紧急情况下，大家都会想到您",
                "您对自己和他人都有比较高的标准"
            ],
            "伤官旺": [
                "您总有很多新奇的想法和创意",
                "您不喜欢按照固定的模式做事",
                "您希望能用自己的方式表达和创造"
            ]
        }
        
        # 心理状态描述
        self.psychological_descriptions = {
            "焦虑型": "您容易为未来担心，总想把所有可能的风险都考虑到",
            "行动型": "您是想到就要去做的人，不喜欢拖延和犹豫",
            "思考型": "您喜欢把问题想清楚，认为充分的思考比匆忙的行动更重要",
            "感受型": "您很敏感，能感受到别人察觉不到的细微变化",
            "目标型": "您是有明确目标的人，喜欢看到自己的进步和成果"
        }
    
    def convert_to_plain_language(self, technical_analysis: Dict[str, Any]) -> Dict[str, str]:
        """将技术分析转换为大白话"""
        converted = {}
        
        # 转换格局分析
        if "定格局" in technical_analysis:
            converted["格局说明"] = self._convert_geju_analysis(technical_analysis["定格局"])
        
        # 转换五行分析
        if "五行统计" in technical_analysis:
            converted["五行说明"] = self._convert_wuxing_analysis(technical_analysis["五行统计"])
        
        # 转换病药分析
        if "定病药" in technical_analysis:
            converted["病药说明"] = self._convert_bingyao_analysis(technical_analysis["定病药"])
        
        # 转换调候分析
        if "定寒燥" in technical_analysis:
            converted["调候说明"] = self._convert_hanzao_analysis(technical_analysis["定寒燥"])
        
        # 转换大运分析
        if "看大运" in technical_analysis:
            converted["大运说明"] = self._convert_dayun_analysis(technical_analysis["看大运"])
        
        return converted
    
    def _convert_geju_analysis(self, geju_data: Dict[str, Any]) -> str:
        """转换格局分析为大白话"""
        geju_type = geju_data.get("格局类型", "")
        strength = geju_data.get("强弱", "")
        root_status = geju_data.get("根", "")
        
        plain_description = []
        
        # 基础格局转换
        if geju_type in self.terminology_mapping:
            basic_desc = self.terminology_mapping[geju_type]
            plain_description.append(f"您的性格特点：{basic_desc}")
        
        # 强弱转换
        strength_descriptions = {
            "旺": "您这方面的能量很充足，是您的优势所在",
            "强": "您在这方面比较有底气和自信",
            "弱": "您这方面比较敏感，需要更多的支持和鼓励",
            "极旺": "您这方面的能量非常强，但也要注意不要过犹不及",
            "极弱": "您这方面需要特别的关注和培养"
        }
        
        if strength in strength_descriptions:
            plain_description.append(strength_descriptions[strength])
        
        # 根的状态转换
        root_descriptions = {
            "有明根": "您的基础很扎实，做事有底气",
            "有藏根": "虽然表面看起来温和，但内在很有实力",
            "无根": "您很灵活，但需要找到稳定的支撑点"
        }
        
        if root_status in root_descriptions:
            plain_description.append(root_descriptions[root_status])
        
        return "。".join(plain_description) + "。"
    
    def _convert_wuxing_analysis(self, wuxing_data: Dict[str, Any]) -> str:
        """转换五行分析为大白话"""
        strongest = wuxing_data.get("最旺", "")
        weakest = wuxing_data.get("最弱", "")
        
        element_personalities = {
            "木": "您有很强的成长欲望，总想尝试新事物，不喜欢一成不变",
            "火": "您很有热情和感染力，容易带动周围的气氛，但有时可能有点急性子",
            "土": "您很踏实可靠，朋友都喜欢找您商量事情，但有时可能有点保守",
            "金": "您做事很有原则和条理，追求完美和效率，但有时可能有点严格",
            "水": "您很聪明灵活，善于观察和思考，但有时可能想得太多"
        }
        
        descriptions = []
        
        if strongest:
            element_clean = strongest.replace("元素", "")
            if element_clean in element_personalities:
                descriptions.append(f"您最突出的特质：{element_personalities[element_clean]}")
        
        if weakest and weakest != strongest:
            element_clean = weakest.replace("元素", "")
            weakness_descriptions = {
                "木": "有时候可能缺乏成长的动力，需要多给自己一些新的刺激",
                "火": "有时候可能不够有激情，需要多接触正能量的人和事",
                "土": "有时候可能不够踏实，需要多培养耐心和坚持",
                "金": "有时候可能不够有原则，需要多培养自己的底线和标准",
                "水": "有时候可能不够灵活，需要多培养变通的智慧"
            }
            if element_clean in weakness_descriptions:
                descriptions.append(f"需要注意的方面：{weakness_descriptions[element_clean]}")
        
        return "。".join(descriptions) + "。"
    
    def _convert_bingyao_analysis(self, bingyao_data: Dict[str, Any]) -> str:
        """转换病药分析为大白话"""
        if not bingyao_data.get("分级"):
            return "暂无病药分析结果。"
        
        first_level = bingyao_data["分级"][0]
        pattern_type = first_level.get("命局类型", "")
        medicine_config = first_level.get("病药配置", {})
        
        descriptions = []
        
        # 命局类型说明
        if pattern_type in self.terminology_mapping:
            descriptions.append(f"您的能量模式：{self.terminology_mapping[pattern_type]}")
        
        # 用药说明（转换为意识建议）
        medicine_explanations = {
            "君药": "最重要的是",
            "臣药": "其次需要", 
            "次药": "也可以考虑"
        }
        
        for medicine_level, medicine_name in medicine_config.items():
            if medicine_level in medicine_explanations and medicine_name:
                plain_medicine = self.terminology_mapping.get(medicine_name, medicine_name)
                action_verb = medicine_explanations[medicine_level]
                descriptions.append(f"{action_verb}培养{plain_medicine}的品质")
        
        return "。".join(descriptions) + "。"
    
    def _convert_hanzao_analysis(self, hanzao_data: Dict[str, Any]) -> str:
        """转换寒燥分析为大白话"""
        climate_type = hanzao_data.get("类型", "")
        need_element = hanzao_data.get("需要调候", "")
        
        climate_descriptions = {
            "寒重": "您的性格比较内敛沉静，但有时候可能缺乏行动的热情",
            "燥重": "您的性格比较急躁活跃，但有时候需要保持内心的平静",
            "偏寒": "您大部分时候比较温和，但有时候需要一些外在的激励",
            "偏燥": "您大部分时候比较有活力，但有时候需要学会慢下来",
            "平和": "您的性格比较温和平衡，这是很好的特质"
        }
        
        base_desc = climate_descriptions.get(climate_type, "您有着独特的性格特质")
        
        # 调候建议转换
        adjustment_advice = {
            "fire": "建议多接触阳光、运动、热情的人和事，给自己增加一些活力",
            "water": "建议多在安静的环境中思考，保持内心的宁静和深度",
            "wood": "建议多接触自然，给自己一些成长和学习的机会",
            "metal": "建议培养一些规律性的习惯，让自己更有条理",
            "earth": "建议保持脚踏实地的态度，一步一个脚印地前进"
        }
        
        advice = adjustment_advice.get(need_element, "保持现在的状态就很好")
        
        return f"{base_desc}。{advice}。"
    
    def _convert_dayun_analysis(self, dayun_data: Dict[str, Any]) -> str:
        """转换大运分析为大白话"""
        current_dayun = dayun_data.get("当前大运", {})
        future_dayuns = dayun_data.get("未来大运", [])
        
        if not current_dayun:
            return "暂无大运分析信息。"
        
        age_range = current_dayun.get("age_range", "")
        influence = current_dayun.get("influence", "")
        
        descriptions = []
        descriptions.append(f"您现在{age_range}岁这个阶段：{influence}")
        
        # 未来大运的简单说明
        if future_dayuns:
            next_dayun = future_dayuns[0]
            next_age = next_dayun.get("age_range", "")
            next_influence = next_dayun.get("influence", "")
            descriptions.append(f"到了{next_age}岁左右：{next_influence}")
        
        # 添加通用的时机把握建议
        timing_advice = [
            "每个人生阶段都有不同的重点，关键是要顺应自己的内在节奏",
            "重要的不是抢在别人前面，而是在合适的时候做合适的事"
        ]
        
        descriptions.extend(timing_advice[:1])
        
        return "。".join(descriptions) + "。"
    
    def simplify_consciousness_description(self, consciousness_text: str) -> str:
        """简化意识描述为生活语言"""
        # 替换复杂的心理学术语
        replacements = {
            "意识品质": "性格特点",
            "能量模式": "行为方式",
            "内在驱动": "内心想法",
            "外在表现": "平时表现",
            "心理机制": "心理状态",
            "认知模式": "思维方式",
            "行为倾向": "做事习惯",
            "情绪特质": "情绪表现",
            "社交模式": "与人相处的方式",
            "决策风格": "做决定的习惯"
        }
        
        simplified_text = consciousness_text
        for technical, plain in replacements.items():
            simplified_text = simplified_text.replace(technical, plain)
        
        return simplified_text
    
    def add_life_examples(self, abstract_description: str, user_context: Dict[str, Any]) -> str:
        """为抽象描述添加生活实例"""
        # 根据用户上下文添加具体的生活场景
        age = user_context.get("age", 25)
        gender = user_context.get("gender", "")
        question_category = user_context.get("question_category", "")
        
        # 年龄段特定的例子
        age_examples = {
            "young": "比如在选择专业、找工作、谈恋爱时",
            "middle": "比如在职业发展、家庭规划、投资理财时", 
            "mature": "比如在事业转型、子女教育、健康管理时"
        }
        
        if age < 30:
            age_context = age_examples["young"]
        elif age < 50:
            age_context = age_examples["middle"]
        else:
            age_context = age_examples["mature"]
        
        # 为描述添加具体情境
        if "您" in abstract_description and age_context:
            enhanced_description = abstract_description.replace(
                "您", f"您（{age_context}）", 1
            )
            return enhanced_description
        
        return abstract_description
    
    def format_final_interpretation(self, all_sections: Dict[str, str], user_context: Dict[str, Any]) -> str:
        """格式化最终解读结果"""
        output_parts = []
        
        # 标题
        user_name = user_context.get("name", "您")
        output_parts.append(f"## 📊 {user_name}的能量解读报告")
        output_parts.append("")
        
        # 各部分内容按优先级排列
        section_order = [
            ("八字基本信息", "bazi_info"),
            ("您的能量画像", "energy_portrait"),
            ("关于您的问题", "question_analysis"),
            ("破解的关键", "solution_key"),
            ("更深层的思考", "deeper_reflection"),
            ("具体建议", "actionable_advice"),
            ("时机把握", "timing_guidance"),
            ("能量调节", "energy_management")
        ]
        
        for title, section_key in section_order:
            if section_key in all_sections and all_sections[section_key]:
                output_parts.append(f"### {title}")
                content = all_sections[section_key]
                # 确保内容是大白话
                simplified_content = self.simplify_consciousness_description(content)
                enhanced_content = self.add_life_examples(simplified_content, user_context)
                output_parts.append(enhanced_content)
                output_parts.append("")
        
        # 结语
        output_parts.append("---")
        output_parts.append("💝 **温馨提醒**：这份解读是基于传统命理学的分析框架，目的是帮助您更好地了解自己，为人生决策提供参考。每个人都是独一无二的，最终的选择权始终在您自己手中。")
        
        return "\n".join(output_parts)
    
    def extract_key_messages(self, full_interpretation: str) -> List[str]:
        """提取关键信息点"""
        # 使用简单的规则提取重要信息
        key_patterns = [
            r"您的核心特质[：:](.+?)[\。\.]",
            r"最重要的是(.+?)[\。\.]", 
            r"关键在于(.+?)[\。\.]",
            r"建议您(.+?)[\。\.]"
        ]
        
        key_messages = []
        for pattern in key_patterns:
            matches = re.findall(pattern, full_interpretation)
            key_messages.extend(matches[:2])  # 每个模式最多取2个
        
        return key_messages[:5]  # 总共最多5个关键信息
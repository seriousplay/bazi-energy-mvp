"""
个性化破解方案生成器
Personalized Solution Generator

功能：
1. 基于用户独特的命理结构，提供个性化的问题破解思路
2. 识别用户的优势能量模式并转化为具体能力
3. 温和地指出可能的盲点和挑战
4. 提供基于个人特质的可执行行动建议
5. 将病药分析转化为意识层面的指导
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class PersonalizedSolution:
    """个性化解决方案"""
    strength_patterns: List[str]    # 优势模式
    blind_spots: List[str]         # 盲点提醒
    actionable_steps: List[str]    # 可执行步骤
    medicine_guidance: Dict[str, str] # 用药指导
    timing_advice: str             # 时机建议
    energy_management: str         # 能量管理

class PersonalizedSolutionGenerator:
    """个性化方案生成器"""
    
    def __init__(self):
        # 优势模式映射表
        self.strength_patterns = {
            "比肩旺": {
                "core_strengths": [
                    "天生的领导力和独立思考能力",
                    "在困难时期能够坚持不懈的韧性",
                    "不被外界声音轻易影响的内在定力",
                    "能够承担责任和独自面对挑战的勇气"
                ],
                "practical_applications": [
                    "在团队中，您往往能提出独特而有价值的观点",
                    "在决策时，您的直觉往往比分析更准确",
                    "在压力下，您反而能发挥出更好的状态",
                    "在需要突破的时候，您有敢于第一个尝试的魄力"
                ]
            },
            "印重": {
                "core_strengths": [
                    "强大的学习能力和知识吸收能力",
                    "深度思考和系统性分析的天赋",
                    "获得他人信任和依赖的亲和力",
                    "在复杂情况下保持冷静判断的能力"
                ],
                "practical_applications": [
                    "您很善于从失败中吸取教训",
                    "您能看到别人看不到的深层次问题",
                    "您在需要耐心和坚持的任务上表现优异",
                    "您能够在混乱中建立秩序和体系"
                ]
            },
            "财旺": {
                "core_strengths": [
                    "强烈的目标导向和结果意识",
                    "善于发现机会和把握时机的敏锐度",
                    "将想法转化为现实的执行力",
                    "在资源配置和价值创造上的天赋"
                ],
                "practical_applications": [
                    "您很善于制定实际可行的计划",
                    "您能在复杂的选择中找到最有价值的方向",
                    "您知道如何用最小的投入获得最大的回报",
                    "您在商业和投资方面有天然的嗅觉"
                ]
            },
            "煞重": {
                "core_strengths": [
                    "强大的责任心和使命感",
                    "在压力下反而能发挥更好的能力",
                    "对规则和标准的深度理解",
                    "能够承担他人不愿承担的重任"
                ],
                "practical_applications": [
                    "您在需要严谨和精确的工作中表现卓越",
                    "您能够在危机时刻保持冷静和理性",
                    "您的承诺和保证往往比合同更有效力",
                    "您能够建立和维护高效的规则体系"
                ]
            },
            "伤官旺": {
                "core_strengths": [
                    "丰富的创造力和独特的表达方式",
                    "敏锐的直觉和情感感知能力",
                    "不被传统思维束缚的创新精神",
                    "能够感染和启发他人的个人魅力"
                ],
                "practical_applications": [
                    "您在需要创新和突破的项目中表现出色",
                    "您能够用独特的方式解决常规方法解决不了的问题",
                    "您的想法往往能给团队带来新的灵感",
                    "您在艺术、设计、创意类工作中有天然优势"
                ]
            }
        }
        
        # 盲点和挑战映射
        self.blind_spots = {
            "比肩旺": [
                "有时候过于坚持己见，可能会错过他人的好建议",
                "在需要妥协和协调的时候可能显得过于强硬",
                "可能会因为太独立而错过合作的机会"
            ],
            "印重": [
                "有时候想得太多，行动得太少",
                "可能会过分依赖外界的认可和支持",
                "在需要快速决策的时候可能会犹豫不决"
            ],
            "财旺": [
                "可能会过分关注短期收益而忽略长期价值",
                "有时候会为了目标而忽略过程中的感受",
                "可能会在人际关系中显得太功利"
            ],
            "煞重": [
                "有时候对自己和他人的要求过于严格",
                "可能会因为太注重规则而缺乏灵活性",
                "在轻松的环境中可能反而不知道怎么放松"
            ],
            "伤官旺": [
                "有时候太过追求创新而忽略了现实的限制",
                "可能会因为太个性化而难以与他人配合",
                "在需要遵守规则的环境中可能会感到压抑"
            ]
        }
        
        # 用药指导（将病药理论转化为意识层面的指导）
        self.medicine_guidance = {
            "君药": {
                "比肩": {
                    "positive": "培养底气和承载力，相信自己有能力处理各种挑战",
                    "practice": "每天给自己一些独立决策的机会，从小事开始建立自信"
                },
                "印": {
                    "positive": "发挥学习能力和智慧积累，成为值得依赖的专家",
                    "practice": "持续学习，同时也要敢于分享您的知识和见解"
                },
                "财": {
                    "positive": "发挥目标导向和执行力，创造实际价值",
                    "practice": "设定具体可达成的目标，并制定详细的行动计划"
                },
                "煞": {
                    "positive": "发挥责任心和承压能力，成为团队的定海神针",
                    "practice": "主动承担有挑战性的任务，在完成中建立威信"
                },
                "伤官": {
                    "positive": "发挥创造力和表达能力，为世界带来新的可能",
                    "practice": "找到适合的创意表达渠道，让您的想法能够影响他人"
                }
            }
        }
    
    def generate_solution(self, bazi_analysis: Dict[str, Any], question_analysis: Any, 
                         bingyao_analysis: Dict[str, Any]) -> PersonalizedSolution:
        """生成个性化解决方案"""
        
        # 获取主要格局类型
        geju_info = bazi_analysis.get("定格局", {})
        geju_type = geju_info.get("格局类型", "平衡格局")
        
        # 获取病药配置
        bingyao_config = bingyao_analysis.get("病药配置", {})
        jun_yao = bingyao_config.get("君药", "")
        chen_yao = bingyao_config.get("臣药", "")
        ci_yao = bingyao_config.get("次药", "")
        
        # 获取大运信息
        dayun_info = bazi_analysis.get("看大运", {})
        current_dayun = dayun_info.get("当前大运", {})
        
        # 1. 识别优势模式
        strength_patterns = self._identify_strength_patterns(geju_type, bazi_analysis)
        
        # 2. 指出盲点（温和方式）
        blind_spots = self._identify_blind_spots(geju_type)
        
        # 3. 生成可执行步骤
        actionable_steps = self._generate_actionable_steps(question_analysis, geju_type, bingyao_config)
        
        # 4. 用药指导
        medicine_guidance = self._generate_medicine_guidance(jun_yao, chen_yao, ci_yao)
        
        # 5. 时机建议
        timing_advice = self._generate_timing_advice(current_dayun, geju_type)
        
        # 6. 能量管理
        energy_management = self._generate_energy_management(bazi_analysis)
        
        return PersonalizedSolution(
            strength_patterns=strength_patterns,
            blind_spots=blind_spots,
            actionable_steps=actionable_steps,
            medicine_guidance=medicine_guidance,
            timing_advice=timing_advice,
            energy_management=energy_management
        )
    
    def _identify_strength_patterns(self, geju_type: str, bazi_analysis: Dict[str, Any]) -> List[str]:
        """识别优势模式"""
        base_strengths = self.strength_patterns.get(geju_type, {}).get("core_strengths", [])
        practical_apps = self.strength_patterns.get(geju_type, {}).get("practical_applications", [])
        
        # 结合具体的五行分布进行个性化
        wuxing_stats = bazi_analysis.get("五行统计", {})
        strongest_element = wuxing_stats.get("最旺", "")
        
        personalized_strengths = []
        personalized_strengths.extend(base_strengths[:2])  # 取前两个核心优势
        personalized_strengths.extend(practical_apps[:2])  # 取前两个实际应用
        
        return personalized_strengths
    
    def _identify_blind_spots(self, geju_type: str) -> List[str]:
        """识别盲点（温和提醒）"""
        base_spots = self.blind_spots.get(geju_type, [])
        
        # 转换为温和的提醒语言
        gentle_reminders = []
        for spot in base_spots:
            gentle_version = spot.replace("可能会", "有时候").replace("过于", "稍微")
            gentle_reminders.append(f"温馨提醒：{gentle_version}，这也是您可以继续优化的地方。")
        
        return gentle_reminders[:2]  # 最多两个提醒
    
    def _generate_actionable_steps(self, question_analysis: Any, geju_type: str, bingyao_config: Dict[str, str]) -> List[str]:
        """生成可执行的行动步骤"""
        category = getattr(question_analysis, 'question_category', 'general')
        
        # 基于问题类型和命局类型生成具体步骤
        action_templates = {
            ("career_entrepreneurship", "比肩旺"): [
                "第一步：列出您最擅长和最感兴趣的3个领域",
                "第二步：在每个领域中找到1-2个具体的机会点",
                "第三步：从最小风险的机会开始尝试，积累经验",
                "第四步：根据实际效果调整方向，保持行动的持续性"
            ],
            ("career_entrepreneurship", "印重"): [
                "第一步：找到一个您尊敬的导师或成功榜样",
                "第二步：系统学习相关的知识和技能",
                "第三步：从小项目开始实践，积累实战经验",
                "第四步：在确认可行性后再扩大规模"
            ],
            ("relationships_marriage", "比肩旺"): [
                "第一步：明确您在关系中的底线和原则",
                "第二步：学会在坚持自我的同时给对方空间",
                "第三步：找到共同的目标和价值观",
                "第四步：在冲突中学会理性沟通而不是情绪对抗"
            ]
        }
        
        key = (category, geju_type)
        specific_steps = action_templates.get(key)
        
        if specific_steps:
            return specific_steps
        
        # 通用行动步骤模板
        return [
            "第一步：明确您真正想要的是什么",
            "第二步：评估现有的资源和能力",
            "第三步：制定渐进式的行动计划",
            "第四步：在行动中不断调整和优化"
        ]
    
    def _generate_medicine_guidance(self, jun_yao: str, chen_yao: str, ci_yao: str) -> Dict[str, str]:
        """生成用药指导（意识层面）"""
        
        # 十神的正向意识品质（作为药的时候）
        positive_consciousness = {
            "比肩": "底气、承载力、自我肯定、内在力量、坚定意志",
            "劫财": "团队精神、协作能力、分享意识、集体利益",
            "食神": "理性思考、长远规划、系统思维、智慧分享",
            "伤官": "创造力、表达能力、突破精神、个性魅力",
            "正财": "目标意识、执行力、成果导向、价值创造",
            "偏财": "机会意识、行动力、灵活应变、快速决策",
            "正官": "责任心、规则意识、稳重可靠、社会责任",
            "七杀": "承压能力、决断力、危机处理、领导威严",
            "正印": "学习能力、智慧积累、贵人运、稳定发展",
            "偏印": "直觉洞察、独立思考、另类智慧、创新思维"
        }
        
        # 十神的负向表达（作为病的时候）
        negative_consciousness = {
            "比肩": "自大、刚愎自用、过分独立、不善合作",
            "劫财": "争强好胜、资源争夺、过分竞争、损人利己",
            "食神": "过分挑剔、理想主义、脱离现实、空谈理论",
            "伤官": "叛逆任性、情绪化、破坏规则、过分个性",
            "正财": "过分功利、短视近利、忽略感情、物质至上",
            "偏财": "投机取巧、缺乏坚持、见异思迁、浮躁不安",
            "正官": "过分保守、缺乏创新、依赖权威、害怕变化",
            "七杀": "过分严厉、压抑自由、独断专行、缺乏温情",
            "正印": "过分依赖、缺乏行动、逃避责任、安于现状",
            "偏印": "孤僻离群、思维偏执、过分另类、难以理解"
        }
        
        guidance = {}
        
        if jun_yao:
            positive_traits = positive_consciousness.get(jun_yao, "积极正向的品质")
            guidance["君药指导"] = f"重点培养{jun_yao}的正向品质：{positive_traits}。这是您最需要加强的核心能力。"
        
        if chen_yao:
            positive_traits = positive_consciousness.get(chen_yao, "辅助性的品质")
            guidance["臣药指导"] = f"同时发展{chen_yao}的优势：{positive_traits}。这能为您的核心能力提供有力支撑。"
        
        if ci_yao:
            positive_traits = positive_consciousness.get(ci_yao, "补充性的品质")
            guidance["次药指导"] = f"适当培养{ci_yao}的特质：{positive_traits}。这能让您的能力更加全面。"
        
        return guidance
    
    def _generate_timing_advice(self, current_dayun: Dict[str, Any], geju_type: str) -> str:
        """生成时机建议"""
        if not current_dayun:
            return "把握当下，顺其自然地发展。"
        
        age_range = current_dayun.get("age_range", "")
        influence = current_dayun.get("influence", "")
        
        timing_templates = {
            "比肩旺": f"当前{age_range}岁的大运阶段，{influence}。这是您发挥独立能力的好时机，建议主动出击，不要等待。",
            "印重": f"在{age_range}岁这个阶段，{influence}。建议您在充分准备的基础上，也要给自己一些行动的机会。",
            "财旺": f"目前{age_range}岁的运势，{influence}。这是追求具体成果的有利时期，要抓住时机行动。",
            "煞重": f"当前{age_range}岁，{influence}。这个阶段您的承压能力会得到很好的发挥，可以接受一些挑战性的任务。",
            "伤官旺": f"在{age_range}岁这个创造力旺盛的时期，{influence}。建议多尝试创新和表达，不要压抑自己的想法。"
        }
        
        return timing_templates.get(geju_type, f"当前{age_range}岁，{influence}。建议顺应自己的内在节奏，该行动时行动，该等待时等待。")
    
    def _generate_energy_management(self, bazi_analysis: Dict[str, Any]) -> str:
        """生成能量管理建议"""
        hanzao_info = bazi_analysis.get("定寒燥", {})
        climate_type = hanzao_info.get("类型", "平和")
        need_element = hanzao_info.get("需要调候", "")
        
        wuxing_stats = bazi_analysis.get("五行统计", {})
        strongest = wuxing_stats.get("最旺", "")
        weakest = wuxing_stats.get("最弱", "")
        
        energy_tips = []
        
        # 基于调候需求
        if "寒" in climate_type:
            energy_tips.append("您的能量容易内敛，建议多接触阳光和正能量的环境，适当增加社交活动。")
        elif "燥" in climate_type:
            energy_tips.append("您的能量容易过热，建议保持内心的宁静，多在安静的环境中思考和休息。")
        else:
            energy_tips.append("您的能量相对平衡，保持现有的生活节奏即可。")
        
        # 基于五行分布
        if strongest and weakest:
            energy_tips.append(f"您的{strongest}能量很充沛，可以多发挥这方面的优势；{weakest}相对较弱，需要适当补充和平衡。")
        
        # 日常能量管理建议
        daily_tips = [
            "每天留出一些安静的时间与自己对话，了解内在的声音。",
            "在做重要决定之前，问问自己：这个选择是否符合我的核心价值观？",
            "定期检视自己的能量状态，该休息时休息，该行动时行动。"
        ]
        
        energy_tips.extend(daily_tips[:2])
        
        return " ".join(energy_tips)
    
    def format_solution_output(self, solution: PersonalizedSolution) -> str:
        """格式化解决方案输出"""
        output_parts = []
        
        output_parts.append("### 🌟 您的优势模式")
        for pattern in solution.strength_patterns:
            output_parts.append(f"✨ {pattern}")
        output_parts.append("")
        
        if solution.blind_spots:
            output_parts.append("### 💝 温馨提醒")
            for spot in solution.blind_spots:
                output_parts.append(f"💡 {spot}")
            output_parts.append("")
        
        output_parts.append("### 📋 具体行动建议")
        for step in solution.actionable_steps:
            output_parts.append(f"▶️ {step}")
        output_parts.append("")
        
        if solution.medicine_guidance:
            output_parts.append("### 💊 意识能量调节")
            for medicine_type, guidance in solution.medicine_guidance.items():
                output_parts.append(f"🔹 **{medicine_type}**: {guidance}")
            output_parts.append("")
        
        output_parts.append("### ⏰ 时机把握")
        output_parts.append(f"🕐 {solution.timing_advice}")
        output_parts.append("")
        
        output_parts.append("### ⚡ 能量管理")
        output_parts.append(f"🔋 {solution.energy_management}")
        
        return "\n".join(output_parts)
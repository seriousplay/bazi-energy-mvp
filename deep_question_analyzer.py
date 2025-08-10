"""
深度问题解析模块
Deep Question Analysis Module

功能：
1. 分析用户问题的深层次动机和潜在担忧
2. 解释为什么这个问题对当事人重要
3. 提供启发性的反思问题
4. 从更高维度重新框定问题
"""

import re
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class QuestionAnalysis:
    """问题分析结果"""
    original_question: str
    question_category: str
    deep_motivation: str
    why_important: str
    core_issue: str
    reflection_questions: List[str]
    reframed_question: str
    emotional_undertone: str

class DeepQuestionAnalyzer:
    """深度问题分析器"""
    
    def __init__(self):
        # 问题类别识别模式
        self.question_patterns = {
            "career_entrepreneurship": {
                "keywords": ["创业", "生意", "投资", "赚钱", "财富", "事业", "职业", "工作", "升职", "跳槽", "开店", "做买卖"],
                "deep_motivations": [
                    "渴望财务自由和独立",
                    "希望证明自己的价值和能力", 
                    "不满于被他人控制的现状",
                    "寻求更大的人生成就感",
                    "害怕错过时机或后悔"
                ]
            },
            "relationships_marriage": {
                "keywords": ["感情", "婚姻", "恋爱", "配偶", "对象", "分手", "离婚", "桃花", "姻缘", "相亲"],
                "deep_motivations": [
                    "寻求安全感和归属感",
                    "渴望被理解和接纳",
                    "害怕孤独或被抛弃",
                    "希望找到人生伴侣共同成长",
                    "担心错过最佳的感情时机"
                ]
            },
            "health_wellbeing": {
                "keywords": ["健康", "身体", "养生", "调理", "生病", "体质", "精神", "心理"],
                "deep_motivations": [
                    "对生命质量的担忧",
                    "希望保持活力和状态",
                    "担心身体透支影响未来",
                    "寻求身心平衡的生活方式",
                    "害怕疾病带来的不确定性"
                ]
            },
            "family_children": {
                "keywords": ["孩子", "子女", "家庭", "父母", "教育", "生育", "怀孕", "养育"],
                "deep_motivations": [
                    "希望给下一代更好的未来",
                    "担心教育方式是否正确",
                    "渴望家庭和谐幸福",
                    "害怕在关键时刻做错决定",
                    "寻求代际传承的意义"
                ]
            },
            "personal_growth": {
                "keywords": ["学习", "成长", "改变", "性格", "习惯", "能力", "技能", "提升"],
                "deep_motivations": [
                    "渴望成为更好的自己",
                    "不满于现在的状态",
                    "希望获得他人认可",
                    "担心被时代淘汰",
                    "寻求人生的意义和价值"
                ]
            },
            "life_direction": {
                "keywords": ["人生", "方向", "选择", "决定", "迷茫", "困惑", "未来", "道路"],
                "deep_motivations": [
                    "对未来的不确定性感到焦虑",
                    "希望找到属于自己的道路",
                    "担心做出错误的人生选择",
                    "渴望活出真实的自己",
                    "寻求生命的深层意义"
                ]
            }
        }
        
        # 情感基调识别
        self.emotional_patterns = {
            "anxiety": ["担心", "害怕", "焦虑", "紧张", "不安", "恐惧"],
            "confusion": ["迷茫", "困惑", "不知道", "该怎么办", "选择", "纠结"],
            "aspiration": ["想要", "希望", "渴望", "追求", "实现", "成功"],
            "doubt": ["怀疑", "不确定", "犹豫", "是否", "会不会", "能不能"],
            "urgency": ["紧急", "马上", "立刻", "赶紧", "错过", "来不及"]
        }
        
    def analyze_question(self, question: str, bazi_analysis: Dict[str, Any]) -> QuestionAnalysis:
        """深度分析用户问题"""
        if not question or not question.strip():
            return self._create_default_analysis()
            
        question = question.strip()
        
        # 识别问题类别
        category = self._identify_question_category(question)
        
        # 分析情感基调
        emotional_undertone = self._analyze_emotional_undertone(question)
        
        # 提取深层动机
        deep_motivation = self._extract_deep_motivation(question, category, bazi_analysis)
        
        # 解释重要性
        why_important = self._explain_why_important(question, category, bazi_analysis)
        
        # 识别核心议题
        core_issue = self._identify_core_issue(question, category, bazi_analysis)
        
        # 生成反思问题
        reflection_questions = self._generate_reflection_questions(question, category, bazi_analysis)
        
        # 重新框定问题
        reframed_question = self._reframe_question(question, category, bazi_analysis)
        
        return QuestionAnalysis(
            original_question=question,
            question_category=category,
            deep_motivation=deep_motivation,
            why_important=why_important,
            core_issue=core_issue,
            reflection_questions=reflection_questions,
            reframed_question=reframed_question,
            emotional_undertone=emotional_undertone
        )
    
    def _identify_question_category(self, question: str) -> str:
        """识别问题类别"""
        question_lower = question.lower()
        
        for category, pattern_info in self.question_patterns.items():
            for keyword in pattern_info["keywords"]:
                if keyword in question_lower:
                    return category
        
        return "general"
    
    def _analyze_emotional_undertone(self, question: str) -> str:
        """分析情感基调"""
        emotions_found = []
        
        for emotion, keywords in self.emotional_patterns.items():
            for keyword in keywords:
                if keyword in question:
                    emotions_found.append(emotion)
        
        if not emotions_found:
            return "neutral"
        
        # 返回最可能的情感基调
        emotion_counts = {emotion: emotions_found.count(emotion) for emotion in set(emotions_found)}
        return max(emotion_counts, key=emotion_counts.get)
    
    def _extract_deep_motivation(self, question: str, category: str, bazi_analysis: Dict[str, Any]) -> str:
        """提取深层动机"""
        base_motivations = self.question_patterns.get(category, {}).get("deep_motivations", [])
        
        if not base_motivations:
            return "寻求对人生方向的确认和指引"
        
        # 基于命局特征选择最匹配的动机
        geju_info = bazi_analysis.get("定格局", {})
        bingyao_info = bazi_analysis.get("定病药", {})
        
        # 简单的匹配逻辑，可以进一步优化
        if "比肩" in str(geju_info) or "劫财" in str(bingyao_info):
            # 自主性强的人更可能有独立和掌控的渴望
            return base_motivations[0] if len(base_motivations) > 0 else "渴望独立和自主"
        elif "印" in str(geju_info):
            # 印重的人更注重安全感和认可
            return base_motivations[-1] if len(base_motivations) > 1 else "寻求安全感和认可"
        else:
            return base_motivations[0] if base_motivations else "寻求内心的确定性"
    
    def _explain_why_important(self, question: str, category: str, bazi_analysis: Dict[str, Any]) -> str:
        """解释为什么这个问题对当事人重要"""
        geju_info = bazi_analysis.get("定格局", {})
        geju_type = geju_info.get("格局类型", "")
        
        base_templates = {
            "career_entrepreneurship": "这个问题触及您对人生掌控权的深层渴望。基于您的命局特征，您天生就有{trait}的特质，这使您对独立自主的生活方式有着强烈的内在需求。",
            "relationships_marriage": "这个问题反映了您对情感连接和归属感的核心需要。您的能量结构显示出{trait}的倾向，这让您格外看重人际关系中的{focus}。",
            "health_wellbeing": "这个问题体现了您对生活质量和长远发展的关注。您的命局{trait}，这让您比其他人更敏感于身心平衡的重要性。",
            "personal_growth": "这个问题源于您内在的成长驱动力。您的能量特质{trait}，这使您天然地渴望不断突破和完善自己。",
            "life_direction": "这个问题触及您对人生意义和价值的深度思考。您的命局显示{trait}，这让您比常人更需要找到属于自己的独特道路。"
        }
        
        template = base_templates.get(category, "这个问题反映了您对生活的深度思考和对未来的关注。")
        
        # 基于格局类型填充特质描述
        trait_descriptions = {
            "比劫旺格": "不甘于平凡、追求独立掌控",
            "印星旺格": "重视学习成长、渴望被认可",
            "食伤旺格": "富有创造力、需要表达和展现",
            "财星旺格": "目标导向、追求具体成果",
            "官杀旺格": "责任感强、在意规则和标准"
        }
        
        trait = trait_descriptions.get(geju_type, "独特的能量组合")
        
        if category == "relationships_marriage":
            focus_map = {
                "比劫旺格": "平等和相互尊重",
                "印星旺格": "理解和支持",
                "食伤旺格": "情感表达和创造性互动",
                "财星旺格": "实际的安全感和未来规划",
                "官杀旺格": "承诺和责任"
            }
            focus = focus_map.get(geju_type, "真诚和深度连接")
            return template.format(trait=trait, focus=focus)
        
        return template.format(trait=trait)
    
    def _identify_core_issue(self, question: str, category: str, bazi_analysis: Dict[str, Any]) -> str:
        """识别核心议题"""
        core_issues = {
            "career_entrepreneurship": "如何平衡风险与机遇，找到既能发挥优势又能实现价值的发展道路",
            "relationships_marriage": "如何在保持独立自我的同时，建立深度的情感连接",
            "health_wellbeing": "如何在追求目标的过程中，维持身心的可持续发展",
            "family_children": "如何在给予关爱的同时，培养出独立自主的下一代",
            "personal_growth": "如何接纳现在的自己，同时保持成长的动力",
            "life_direction": "如何在众多选择中，找到真正与内心价值观一致的道路"
        }
        
        return core_issues.get(category, "如何在变化中找到属于自己的确定性")
    
    def _generate_reflection_questions(self, question: str, category: str, bazi_analysis: Dict[str, Any]) -> List[str]:
        """生成启发性反思问题"""
        base_questions = {
            "career_entrepreneurship": [
                "您被创业吸引的最深层原因是什么——是为了证明能力，还是为了获得自由？",
                "如果不考虑他人的期待和社会标准，您真正想要创造的价值是什么？",
                "您准备为这个选择承受什么程度的不确定性？"
            ],
            "relationships_marriage": [
                "您希望在这段关系中成为什么样的人？",
                "您对伴侣的期待，是否也是对自己内在缺失部分的投射？",
                "如果这个人永远不会改变，您还会选择在一起吗？"
            ],
            "health_wellbeing": [
                "您的身体正在向您传达什么信息？",
                "您理想中的健康状态是什么样子的？",
                "是什么阻止了您做出更有利于健康的选择？"
            ],
            "personal_growth": [
                "您想要改变的，是真的需要改变，还是因为不够接纳现在的自己？",
                "您成长的动力来自内在的渴望，还是外在的压力？",
                "如果没有他人的评判，您会选择怎样的成长方向？"
            ],
            "life_direction": [
                "如果只剩五年生命，您会如何安排？",
                "您的内心深处，最不愿意妥协的是什么？",
                "什么样的生活会让您在回首时感到无悔？"
            ]
        }
        
        questions = base_questions.get(category, [
            "这个问题背后，您真正关心的是什么？",
            "如果完全按照内心的声音，您会如何选择？",
            "您希望通过这个决定成为什么样的人？"
        ])
        
        # 基于命局特征个性化问题
        geju_info = bazi_analysis.get("定格局", {})
        if "比劫" in str(geju_info) and category == "career_entrepreneurship":
            questions.append("您是否已经准备好独自承担所有的责任和后果？")
        elif "印" in str(geju_info):
            questions.append("您是否在寻求他人的认可，还是真心相信这是正确的方向？")
            
        return questions[:3]  # 限制在3个问题以内
    
    def _reframe_question(self, question: str, category: str, bazi_analysis: Dict[str, Any]) -> str:
        """重新框定问题"""
        reframe_templates = {
            "career_entrepreneurship": "与其问'{original}'，不如探索：我如何能在发挥自己独特优势的同时，创造真正有意义的价值？",
            "relationships_marriage": "比起'{original}'，更重要的可能是：我如何能在关系中既保持真实的自己，又给予对方需要的支持？",
            "health_wellbeing": "'{original}'的背后，核心问题是：我如何能建立一种可持续的生活方式，让身心都能长期保持最佳状态？",
            "personal_growth": "除了'{original}'，您也可以思考：我如何能在接纳现在的自己的基础上，自然而然地成长？",
            "life_direction": "'{original}'可以转换为：我如何能找到一条既符合我内在价值观，又能充分发挥我天赋的人生道路？"
        }
        
        template = reframe_templates.get(category, "'{original}'背后的核心是：我如何能做出最符合内心真实声音的选择？")
        return template.format(original=question)
    
    def _create_default_analysis(self) -> QuestionAnalysis:
        """创建默认分析结果"""
        return QuestionAnalysis(
            original_question="",
            question_category="general",
            deep_motivation="寻求人生方向的指引",
            why_important="每个人都有找到适合自己道路的内在需求",
            core_issue="如何在变化中找到内在的确定性",
            reflection_questions=[
                "您当前最关心的是什么？",
                "如果完全按照内心的声音，您会如何选择？",
                "什么样的生活会让您感到真正的满足？"
            ],
            reframed_question="我如何能活出最真实的自己？",
            emotional_undertone="neutral"
        )
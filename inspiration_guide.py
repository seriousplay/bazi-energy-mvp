"""
启发式问题引导模块
Inspiration Guide Module

功能：
1. 重新框定问题，从更高维度思考
2. 生成启发性的反思问题
3. 引导用户探索内在动机
4. 提供多角度的思考路径
5. 避免给出确定性答案，而是启发思考
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from deep_question_analyzer import QuestionAnalysis

@dataclass 
class InspirationResult:
    """启发引导结果"""
    reframed_perspective: str    # 重新框定的视角
    deeper_questions: List[str]  # 更深层的反思问题
    multiple_angles: List[str]   # 多角度思考
    wisdom_insights: List[str]   # 智慧洞察
    consciousness_elevation: str # 意识层次提升

class InspirationGuide:
    """启发式问题引导器"""
    
    def __init__(self):
        # 重新框定问题的模板
        self.reframe_templates = {
            "career_entrepreneurship": {
                "surface": "我适合创业吗？",
                "deeper": [
                    "我为什么会被创业这个想法吸引？",
                    "我想要通过创业获得什么——是金钱、自由、还是成就感？",
                    "除了创业，还有什么其他方式能让我获得内心真正渴望的东西？",
                    "我准备为了这个选择付出什么代价？"
                ]
            },
            "relationships_marriage": {
                "surface": "我们合适吗？",
                "deeper": [
                    "我在这段关系中能成为最好的自己吗？",
                    "我对伴侣的期待，是否也反映了我对自己的期待？",
                    "这段关系是在帮助我成长，还是让我停滞？",
                    "我是在寻找一个伴侣，还是在寻找内心的完整？"
                ]
            },
            "health_wellbeing": {
                "surface": "我的身体有什么问题？",
                "deeper": [
                    "我的身体状况反映了什么样的生活模式？",
                    "我是在真正关爱自己，还是在消耗自己？",
                    "什么样的生活节奏最符合我的内在需求？",
                    "我如何能让身体成为支持梦想的伙伴？"
                ]
            },
            "personal_growth": {
                "surface": "我需要改变什么？",
                "deeper": [
                    "我想要改变的，是真的需要改变，还是因为不够接纳自己？",
                    "我的成长动力是来自内在的渴望，还是外在的压力？",
                    "什么样的成长方向最符合我的天性？",
                    "我如何能在成长的同时保持内心的平静？"
                ]
            },
            "life_direction": {
                "surface": "我应该选择哪条路？",
                "deeper": [
                    "哪条路能让我在回首时感到无悔？",
                    "我内心最不愿意妥协的是什么？",
                    "如果没有外界的期待和压力，我会选择什么？",
                    "我想要留下什么样的人生印记？"
                ]
            }
        }
        
        # 基于命局的智慧洞察模板
        self.wisdom_insights = {
            "比肩旺": [
                "真正的独立不是拒绝一切帮助，而是知道什么时候需要独自前行，什么时候需要团队合作。",
                "您的优势在于坚持，但也要警惕固执。最好的决策往往需要既坚持原则，又保持灵活。",
                "您天生就是领导者的材料，但领导力不在于控制他人，而在于影响和激励他人。"
            ],
            "印重": [
                "学习是您的天赋，但不要让对完美的追求阻止了行动的开始。",
                "安全感不来自于拥有所有的答案，而来自于相信自己有能力面对未知。",
                "您的智慧在于深度思考，但有时候直觉和行动比分析更重要。"
            ],
            "财旺": [
                "成功不仅仅是达到目标，更重要的是成为能够持续达成目标的人。",
                "您善于抓住机会，但最大的机会往往是成为别人愿意与之合作的人。",
                "金钱和成就只是副产品，真正的财富是您能为这个世界创造的价值。"
            ],
            "煞重": [
                "您的力量在于能够承担责任，但不要忘记，最大的责任是对自己的人生负责。",
                "规则是为了保护大家，但您也有创造新规则的能力。",
                "您在压力下能发挥最佳状态，这是天赋，但也要学会在没有压力时保持动力。"
            ],
            "伤官旺": [
                "您的创造力是礼物，但要记住，最好的创造是既表达了自己又能够感动他人的。",
                "反叛有时是必要的，但反叛的目的应该是建设，而不是破坏。",
                "您不需要得到所有人的理解，但要确保理解您的人是真正重要的人。"
            ]
        }
    
    def generate_inspiration(self, question_analysis: QuestionAnalysis, bazi_analysis: Dict[str, Any]) -> InspirationResult:
        """生成完整的启发引导"""
        
        category = question_analysis.question_category
        original_q = question_analysis.original_question
        
        # 1. 重新框定视角
        reframed_perspective = self._generate_reframed_perspective(question_analysis, bazi_analysis)
        
        # 2. 生成更深层的问题
        deeper_questions = self._generate_deeper_questions(category, bazi_analysis)
        
        # 3. 提供多角度思考
        multiple_angles = self._generate_multiple_angles(question_analysis, bazi_analysis)
        
        # 4. 智慧洞察
        wisdom_insights = self._generate_wisdom_insights(bazi_analysis)
        
        # 5. 意识层次提升
        consciousness_elevation = self._generate_consciousness_elevation(question_analysis, bazi_analysis)
        
        return InspirationResult(
            reframed_perspective=reframed_perspective,
            deeper_questions=deeper_questions,
            multiple_angles=multiple_angles,
            wisdom_insights=wisdom_insights,
            consciousness_elevation=consciousness_elevation
        )
    
    def _generate_reframed_perspective(self, question_analysis: QuestionAnalysis, bazi_analysis: Dict[str, Any]) -> str:
        """重新框定问题视角"""
        category = question_analysis.question_category
        original = question_analysis.original_question
        
        geju_info = bazi_analysis.get("定格局", {})
        geju_type = geju_info.get("格局类型", "")
        
        reframe_logic = {
            "career_entrepreneurship": {
                "比劫旺格": f"您问'{original}'，但更重要的问题可能是：我如何能建立一个既能发挥我独立特质，又能与他人协作共赢的事业模式？",
                "印重格": f"比起'{original}'，您更需要思考：我如何能在保持学习成长的同时，也敢于把知识转化为实际行动？",
                "财旺格": f"与其纠结'{original}'，不如探索：我如何能创造一种既有稳定收益，又能持续增长的价值模式？"
            },
            "relationships_marriage": {
                "比劫旺格": f"您关心'{original}'，但核心问题可能是：我如何能在保持独立自我的同时，也给对方足够的空间和尊重？",
                "印重格": f"比起'{original}'，您更需要思考：我是在寻找一个伴侣，还是在寻找一个能让我感到安全的依靠？"
            }
        }
        
        category_templates = reframe_logic.get(category, {})
        specific_template = category_templates.get(geju_type)
        
        if specific_template:
            return specific_template
        
        # 通用重新框定
        return f"您问'{original}'，但更深层的问题可能是：我如何能做出既符合内心真实声音，又能带来长远幸福的选择？"
    
    def _generate_deeper_questions(self, category: str, bazi_analysis: Dict[str, Any]) -> List[str]:
        """生成更深层的反思问题"""
        base_questions = self.reframe_templates.get(category, {}).get("deeper", [])
        
        # 基于命局特征个性化问题
        geju_info = bazi_analysis.get("定格局", {})
        
        personalized_questions = []
        
        if "比劫" in str(geju_info):
            personalized_questions.extend([
                "您是否已经准备好独自承担所有的责任？",
                "您的独立是为了证明什么，还是为了获得什么？"
            ])
        elif "印" in str(geju_info):
            personalized_questions.extend([
                "您是在寻求他人的认可，还是真心相信这个方向？",
                "您需要多少准备才会觉得足够？"
            ])
        elif "伤" in str(geju_info):
            personalized_questions.extend([
                "您想要表达的真正内容是什么？",
                "您是在创造新的可能，还是在反对现有的规则？"
            ])
        
        # 合并基础问题和个性化问题
        all_questions = base_questions + personalized_questions
        return all_questions[:4]  # 限制在4个问题
    
    def _generate_multiple_angles(self, question_analysis: QuestionAnalysis, bazi_analysis: Dict[str, Any]) -> List[str]:
        """提供多角度思考"""
        category = question_analysis.question_category
        
        angle_templates = {
            "career_entrepreneurship": [
                "从能力角度：您具备什么独特的优势和资源？",
                "从时机角度：现在是不是最适合您的时间点？",
                "从内心角度：这个选择是否与您的核心价值观一致？",
                "从现实角度：您能承受可能的失败和不确定性吗？"
            ],
            "relationships_marriage": [
                "从成长角度：这段关系是否在帮助您成为更好的人？",
                "从价值观角度：您们在重要的人生议题上是否一致？",
                "从情感角度：您是被需要感吸引，还是被爱情本身吸引？",
                "从长远角度：您能想象和这个人一起度过人生的各个阶段吗？"
            ],
            "health_wellbeing": [
                "从生活方式角度：您的日常习惯是在支持健康还是在透支身体？",
                "从心理角度：您对身体的关注是来自爱护还是来自恐惧？",
                "从能量角度：什么样的活动能让您感到真正的活力？",
                "从平衡角度：您如何在工作和休息之间找到最佳的节奏？"
            ]
        }
        
        return angle_templates.get(category, [
            "从内心角度：这个选择真的符合您的价值观吗？",
            "从长远角度：这个决定会让您成为什么样的人？",
            "从现实角度：您准备为这个选择付出什么？",
            "从成长角度：这个经历会带给您什么样的学习？"
        ])
    
    def _generate_wisdom_insights(self, bazi_analysis: Dict[str, Any]) -> List[str]:
        """生成智慧洞察"""
        geju_info = bazi_analysis.get("定格局", {})
        geju_type = geju_info.get("格局类型", "")
        
        insights = self.wisdom_insights.get(geju_type, [
            "每个人都有自己独特的节奏，不要急于模仿他人的步伐。",
            "最好的决定往往不是最完美的，而是最适合当下的您的。",
            "信任自己的直觉，但也要用理性验证直觉的正确性。"
        ])
        
        return insights[:2]  # 限制在2条以内
    
    def _generate_consciousness_elevation(self, question_analysis: QuestionAnalysis, bazi_analysis: Dict[str, Any]) -> str:
        """生成意识层次提升的引导"""
        category = question_analysis.question_category
        emotional_tone = question_analysis.emotional_undertone
        
        elevation_templates = {
            "anxiety": "当我们能够从更高的维度看待这个问题时，焦虑往往会转化为清晰的洞察。您现在担心的事情，其实正是您内在智慧想要突破的地方。",
            "confusion": "迷茫不是坏事，它说明您正在成长的边界上。真正的清晰不是消除所有的不确定性，而是在不确定中找到内在的笃定。",
            "aspiration": "您的渴望是内在智慧的声音。但要记住，最持久的满足往往来自于过程中的成长，而不仅仅是结果的获得。",
            "doubt": "怀疑也是一种智慧。它提醒您不要盲目跟从，而要找到真正属于自己的答案。相信您的内心，它比您想象的更加聪明。"
        }
        
        base_elevation = elevation_templates.get(emotional_tone, 
            "每一个问题的背后，都是您内在智慧想要与您对话的机会。静下心来倾听，答案往往比您想象的更清晰。"
        )
        
        # 基于命局特征添加个性化提升
        geju_info = bazi_analysis.get("定格局", {})
        if "比劫" in str(geju_info):
            personal_note = "您天生就有独立思考的能力，相信自己的判断，但也要保持开放的心态。"
        elif "印" in str(geju_info):
            personal_note = "您的智慧在于深度思考，但有时候行动本身就是最好的学习。"
        elif "伤" in str(geju_info):
            personal_note = "您的创造力是天赋，用它来创造美好，而不仅仅是表达不满。"
        else:
            personal_note = "您有着独特的能量组合，这就是您最大的优势。"
        
        return f"{base_elevation} {personal_note}"
    
    def generate_breakthrough_insights(self, question_analysis: QuestionAnalysis, bazi_analysis: Dict[str, Any]) -> str:
        """生成突破性洞察"""
        category = question_analysis.question_category
        core_issue = question_analysis.core_issue
        
        # 基于不同类型的问题生成突破性思路
        breakthrough_templates = {
            "career_entrepreneurship": """
            真正的突破不在于选择创业还是打工，而在于理解：成功的定义是什么？
            
            如果您的内心渴望独立和掌控，那么即使在打工的环境中，您也可以寻找更多的自主权和决策空间。
            如果您的目标是财务自由，那么创业只是其中一条路径，投资、副业、技能变现都可能是更适合的选择。
            如果您想要证明自己的价值，那么最重要的是先在内心确认自己的价值，而不是通过外在的成功来证明。
            
            关键的突破在于：您能否找到一种既发挥优势又享受过程的工作方式？
            """,
            
            "relationships_marriage": """
            真正的突破不在于选择这个人还是那个人，而在于理解：我想要在关系中成为什么样的人？
            
            如果您总是在关系中感到不满，可能不是对方的问题，而是您还没有学会爱自己。
            如果您总是担心对方会离开，可能需要先建立起对自己的信心和安全感。
            如果您总是想要改变对方，可能是因为您还没有完全接纳现在的自己。
            
            关键的突破在于：您能否在关系中既保持真实的自己，又给予对方成长的空间？
            """,
            
            "health_wellbeing": """
            真正的突破不在于找到完美的健康方案，而在于理解：什么样的生活方式最符合我的本性？
            
            如果您总是感到疲惫，可能不是身体的问题，而是生活方式与内在节奏不匹配。
            如果您总是担心健康，可能需要先建立起对生命力的信任。
            如果您总是无法坚持健康习惯，可能是因为这些习惯不够符合您的天性。
            
            关键的突破在于：您能否找到一种既保持活力又可持续的生活节奏？
            """
        }
        
        return breakthrough_templates.get(category, """
        真正的突破往往不在于找到标准答案，而在于学会提出更好的问题。
        
        当我们能够从'我应该怎么选择'转向'我想要成为什么样的人'时，
        当我们能够从'这样做对不对'转向'这样做是否符合我的价值观'时，
        当我们能够从'别人会怎么看'转向'我真正关心什么'时，
        
        答案往往就自然而然地浮现了。
        """).strip()
    
    def format_inspiration_output(self, inspiration: InspirationResult) -> str:
        """格式化启发输出"""
        output_parts = []
        
        output_parts.append("### 🔄 换个角度看问题")
        output_parts.append(inspiration.reframed_perspective)
        output_parts.append("")
        
        output_parts.append("### 🤔 值得深思的问题")
        for i, question in enumerate(inspiration.deeper_questions, 1):
            output_parts.append(f"{i}. {question}")
        output_parts.append("")
        
        output_parts.append("### 🌟 多维度思考")
        for angle in inspiration.multiple_angles:
            output_parts.append(f"• {angle}")
        output_parts.append("")
        
        output_parts.append("### 💡 智慧洞察")
        for insight in inspiration.wisdom_insights:
            output_parts.append(f"💭 {insight}")
        output_parts.append("")
        
        output_parts.append("### ⬆️ 意识层次的提升")
        output_parts.append(inspiration.consciousness_elevation)
        
        return "\n".join(output_parts)
"""
意识能量画像生成器
Energy Portrait Generator

功能：
1. 用直观、画面性的语言勾勒命主的意识能量特征
2. 生成生动的比喻和意象
3. 连接到用户的情感共鸣
4. 避免专业术语，使用大白话表达
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
import random

@dataclass
class EnergyPortrait:
    """能量画像结果"""
    core_image: str          # 核心意象
    detailed_description: str # 详细描述
    life_manifestation: str  # 生活中的体现
    inner_voice: str         # 内心声音
    energy_rhythm: str       # 能量节奏

class EnergyPortraitGenerator:
    """意识能量画像生成器"""
    
    def __init__(self):
        # 五行基础意象库
        self.element_imagery = {
            "wood": {
                "strong": {
                    "images": ["参天大树", "茂密森林", "春天的竹林", "向上攀爬的藤蔓", "破土而出的新芽"],
                    "qualities": ["向上生长", "不断扩张", "生机勃勃", "柔韧坚强", "适应性强"],
                    "scenarios": ["总想尝试新事物", "不喜欢被限制", "容易感受到成长的冲动", "对未来充满期待"]
                },
                "weak": {
                    "images": ["等待雨露的幼苗", "盆景中的嫩枝", "准备发芽的种子", "春风中的柳絮"],
                    "qualities": ["蓄势待发", "需要滋养", "潜力巨大", "纯真善良"],
                    "scenarios": ["经常感到需要学习", "容易被他人影响", "内心有很多想法但不知如何表达"]
                }
            },
            "fire": {
                "strong": {
                    "images": ["熊熊燃烧的篝火", "正午的太阳", "跳动的火焰", "温暖的壁炉", "闪闪发光的星星"],
                    "qualities": ["热情洋溢", "照亮他人", "能量充沛", "感染力强", "直来直去"],
                    "scenarios": ["很容易带动气氛", "说话做事都比较直接", "喜欢成为焦点", "情绪表达丰富"]
                },
                "weak": {
                    "images": ["微弱的烛光", "黎明前的第一缕阳光", "温和的暖炉", "夜空中的萤火"],
                    "qualities": ["温和坚持", "默默温暖", "内在光明", "细水长流"],
                    "scenarios": ["虽然不张扬但很温暖", "用自己的方式影响身边的人", "内心其实很有想法"]
                }
            },
            "earth": {
                "strong": {
                    "images": ["厚重的大地", "稳固的山峰", "肥沃的土壤", "承载万物的平原", "深厚的根基"],
                    "qualities": ["包容厚德", "承载力强", "踏实可靠", "默默奉献", "持之以恒"],
                    "scenarios": ["朋友都喜欢找您倾诉", "做事认真负责", "不喜欢投机取巧", "更看重长期价值"]
                },
                "weak": {
                    "images": ["需要滋养的花园", "正在积累的土壤", "等待播种的田地", "蓄势的洼地"],
                    "qualities": ["默默积累", "潜在包容", "等待时机", "内在稳定"],
                    "scenarios": ["外表温和但内心坚定", "善于倾听和理解他人", "不急于表现自己"]
                }
            },
            "metal": {
                "strong": {
                    "images": ["锋利的宝剑", "精钢般的意志", "闪亮的钻石", "清脆的钟声", "凌厉的秋风"],
                    "qualities": ["决断果敢", "原则性强", "理性清晰", "追求完美", "不轻易妥协"],
                    "scenarios": ["做决定很快很准", "有自己的底线和原则", "说话直接有力", "追求效率和质量"]
                },
                "weak": {
                    "images": ["待雕琢的玉石", "深藏的宝矿", "正在磨砺的刀刃", "含苞的金桂"],
                    "qualities": ["内在坚韧", "潜在锋芒", "等待机会", "细致精准"],
                    "scenarios": ["看起来温和但很有主见", "关键时刻会展现出强大的力量", "追求品质和精致"]
                }
            },
            "water": {
                "strong": {
                    "images": ["奔腾的江河", "深邃的大海", "智慧的深潭", "包容的湖泊", "灵活的溪流"],
                    "qualities": ["智慧深沉", "适应力强", "包容性大", "流动变化", "润物无声"],
                    "scenarios": ["善于察言观色", "能够理解复杂的情况", "喜欢思考人生", "容易感受到他人情绪"]
                },
                "weak": {
                    "images": ["清澈的山泉", "宁静的小溪", "晶莹的露珠", "涓涓的细流"],
                    "qualities": ["纯净透明", "细腻敏感", "需要保护", "默默滋润"],
                    "scenarios": ["内心很敏感细腻", "容易被感动", "善于感受细微的变化", "需要安静的空间"]
                }
            }
        }
        
        # 命局类型的核心意象
        self.juju_core_imagery = {
            "比肩旺": {
                "metaphor": "一匹桀骜不驯的野马",
                "essence": "天生就不愿意被束缚，内心有着强烈的独立意志",
                "manifestation": "在人群中，您总是那个有自己想法的人。您不会因为大家都这么做就跟风，您需要理解了、认同了才会行动。"
            },
            "印重": {
                "metaphor": "一座正在积累知识的图书馆",
                "essence": "您天生就是一个学习者和思考者，喜欢在理解中获得安全感",
                "manifestation": "您总是希望把事情想清楚再行动，喜欢听取专家意见，重视长辈和权威的建议。"
            },
            "财旺": {
                "metaphor": "一台精准高效的收割机",
                "essence": "您的内心有着强烈的目标导向，善于把想法转化为具体的成果",
                "manifestation": "您是那种'想到就要做到'的人，不喜欢空谈，更喜欢看到实际的进展和收获。"
            },
            "煞重": {
                "metaphor": "一座在风雨中屹立的灯塔",
                "essence": "您在压力下反而能发挥出更好的状态，天生具有强大的承压能力",
                "manifestation": "别人觉得困难的事情，您反而觉得有挑战性。您不怕承担责任，甚至在关键时刻愿意挺身而出。"
            },
            "伤官旺": {
                "metaphor": "一朵正要绽放的奇花",
                "essence": "您的内心充满了创造力和表达欲，不喜欢被条条框框限制",
                "manifestation": "您总是有很多新奇的想法，喜欢用自己的方式做事，不太在意别人是否理解。"
            },
            "从财": {
                "metaphor": "一条顺水而下的小船",
                "essence": "您善于借力打力，懂得与环境和他人合作共赢",
                "manifestation": "您很善于发现机会，也愿意与他人分享成果。您知道什么时候该主动，什么时候该配合。"
            },
            "从杀": {
                "metaphor": "一块经过千锤百炼的钢铁",
                "essence": "您在规则和约束中反而能找到自己的位置和价值",
                "manifestation": "您不害怕严格的要求和高标准，甚至觉得这样的环境更能让您发挥出真正的实力。"
            },
            "化气格": {
                "metaphor": "一束专注而纯粹的激光",
                "essence": "您的能量非常集中，一旦确定方向就能深度投入",
                "manifestation": "您不是那种什么都想尝试的人，但一旦找到了感兴趣的领域，就会投入全部的热情和精力。"
            }
        }
        
        # 调候情境修饰
        self.climate_contexts = {
            "寒重": {
                "modifier": "在严寒的冬夜里",
                "need": "您的内心渴望温暖和光明",
                "advice": "需要更多的阳光和热情来激发您的潜能"
            },
            "燥重": {
                "modifier": "在炽热的夏日中",
                "need": "您的内心需要宁静和冷静",
                "advice": "需要更多的沉静和思考来平衡您的能量"
            },
            "平和": {
                "modifier": "在四季如春的环境中",
                "need": "您的内心相对平衡",
                "advice": "保持现有的平衡状态，顺其自然地发展"
            }
        }
    
    def generate_portrait(self, bazi_analysis: Dict[str, Any], jugu_detection: Dict[str, Any]) -> EnergyPortrait:
        """生成完整的能量画像 - 基于日主和月令的个性化组合"""
        
        # 获取核心信息
        primary_types = jugu_detection.get("primary", [])
        main_type = primary_types[0] if primary_types else "平衡格局"
        
        # 获取日主和月令信息
        bazi_info = bazi_analysis.get("bazi", {})
        day_gan = bazi_info.get("day", "甲子")[0] if bazi_info.get("day") else "甲"
        month_zhi = bazi_info.get("month", "甲子")[1] if bazi_info.get("month") else "子"
        
        # 获取五行信息
        wuxing_stats = bazi_analysis.get("五行统计", {})
        strongest_element = wuxing_stats.get("最旺", "").replace("元素", "")
        
        # 获取调候信息
        hanzao_info = bazi_analysis.get("定寒燥", {})
        climate_type = hanzao_info.get("类型", "平和")
        
        # 生成基于日主+月令的个性化意象
        personalized_imagery = self._generate_personalized_imagery(day_gan, month_zhi, main_type, strongest_element)
        
        # 添加调候情境修饰
        climate_context = self.climate_contexts.get(climate_type, self.climate_contexts["平和"])
        
        # 生成完整描述
        core_image = f"{climate_context['modifier']}，您就像{personalized_imagery['metaphor']}。"
        
        detailed_description = f"{personalized_imagery['essence']}。{climate_context['need']}，{climate_context['advice']}。"
        
        life_manifestation = f"在日常生活中，{personalized_imagery['manifestation']}"
        
        # 生成内心声音
        inner_voice = self._generate_inner_voice_personalized(day_gan, month_zhi, strongest_element)
        
        # 生成能量节奏
        energy_rhythm = self._generate_energy_rhythm_personalized(day_gan, month_zhi, wuxing_stats)
        
        return EnergyPortrait(
            core_image=core_image,
            detailed_description=detailed_description,
            life_manifestation=life_manifestation,
            inner_voice=inner_voice,
            energy_rhythm=energy_rhythm
        )
    
    def _generate_inner_voice(self, juju_type: str, strongest_element: str) -> str:
        """生成内心声音"""
        inner_voices = {
            "比肩旺": [
                "我要做自己人生的主人。",
                "为什么要听别人的安排？我有自己的想法。",
                "我相信自己的判断，我要走自己的路。"
            ],
            "印重": [
                "我需要先把这个问题想清楚。",
                "让我再学习一下，准备充分了再行动。",
                "我希望有人能给我一些指导和建议。"
            ],
            "财旺": [
                "我要看到实际的结果和收获。",
                "这样做能带来什么具体的好处？",
                "我要抓住这个机会，不能让它溜走。"
            ],
            "煞重": [
                "我必须对这件事负责到底。",
                "按照规则来做，这样最安全。",
                "我不能让大家失望，我要做好。"
            ],
            "伤官旺": [
                "为什么一定要按照传统的方式？",
                "我有更好的想法，让我试试看。",
                "我要表达出真正的自己。"
            ],
            "从财": [
                "我要跟着趋势走，抓住这个机会。",
                "大家都在做，说明这个方向是对的。",
                "我要找到最有价值的位置。"
            ],
            "从杀": [
                "我要跟着有能力的人学习。",
                "严格的要求能让我成长得更快。",
                "我愿意接受挑战，证明自己。"
            ]
        }
        
        voices = inner_voices.get(juju_type, ["我要找到属于自己的道路。"])
        return random.choice(voices)
    
    def _generate_energy_rhythm(self, juju_type: str, wuxing_stats: Dict[str, Any]) -> str:
        """生成能量节奏描述"""
        rhythms = {
            "比肩旺": "您的能量节奏是稳定而持续的，就像大地的脉搏，一旦确定方向就会坚持下去。",
            "印重": "您的能量像潮汐一样，有涨有落，需要在积累和释放之间找到平衡。",
            "财旺": "您的能量是目标导向的，就像箭射向靶心，专注而有力。",
            "煞重": "您的能量在压力下会被激发，就像被点燃的火药，关键时刻爆发出惊人的力量。",
            "伤官旺": "您的能量是创造性的，就像春天的万物生长，充满了无穷的可能性。",
            "从财": "您的能量是顺应性的，就像水流向低处，总能找到最适合的方向。",
            "从杀": "您的能量在规范中得到最好的发挥，就像精密的仪器，在精确中展现威力。"
        }
        
        base_rhythm = rhythms.get(juju_type, "您有着独特的能量节奏，正在寻找最适合的表达方式。")
        
        # 基于五行分布调整描述
        strongest = wuxing_stats.get("最旺", "")
        weakest = wuxing_stats.get("最弱", "")
        
        if strongest and weakest:
            balance_note = f"目前{strongest}的能量最为活跃，而{weakest}的能量相对安静，这种不平衡也是您独特魅力的来源。"
            return f"{base_rhythm} {balance_note}"
        
        return base_rhythm
    
    def generate_life_scenarios(self, juju_type: str, question_category: str) -> List[str]:
        """基于命局类型和问题类别生成生活场景"""
        scenarios = {
            ("比肩旺", "career_entrepreneurship"): [
                "您可能经常想：'为什么我总是想自己干，而不是给别人打工？'",
                "朋友聚会时，当大家抱怨工作，您心里想的是：'为什么不自己闯一闯？'",
                "看到成功的创业者，您会想：'如果是我，我会做得更好。'"
            ],
            ("印重", "career_entrepreneurship"): [
                "您经常纠结：'我是不是还没准备好？是不是应该再学习一段时间？'",
                "看到别人创业失败，您会想：'果然还是稳定的工作更安全。'",
                "您总希望有个有经验的导师能指导您。"
            ],
            ("伤官旺", "relationships_marriage"): [
                "您在感情中总想表达真实的自己，不愿意为了迎合而改变。",
                "您需要的不只是爱情，更是理解和欣赏您独特性的伴侣。",
                "您可能会想：'为什么要按照别人的标准找对象？'"
            ]
        }
        
        key = (juju_type, question_category)
        return scenarios.get(key, [
            "您用自己的方式理解和应对这个世界。",
            "您有着独特的思考模式和行为方式。",
            "您的内心其实比表面看起来更加丰富和复杂。"
        ])
    
    def generate_vivid_metaphor(self, bazi_analysis: Dict[str, Any], context: str = "") -> str:
        """生成生动的比喻描述"""
        # 这个函数专门用于生成用户要求的"画面性语言"描述
        pass
    
    def _generate_personalized_imagery(self, day_gan: str, month_zhi: str, main_type: str, strongest_element: str) -> Dict[str, str]:
        """基于日主和月令生成个性化意象"""
        
        # 日主特质映射
        day_gan_traits = {
            "甲": {"nature": "参天大树", "energy": "向上生长", "season_affinity": "春"},
            "乙": {"nature": "柔韧花草", "energy": "灵活适应", "season_affinity": "春"}, 
            "丙": {"nature": "烈日骄阳", "energy": "热情奔放", "season_affinity": "夏"},
            "丁": {"nature": "温暖烛火", "energy": "温和持久", "season_affinity": "夏"},
            "戊": {"nature": "厚重山峰", "energy": "稳固承载", "season_affinity": "四季"},
            "己": {"nature": "肥沃土地", "energy": "滋养包容", "season_affinity": "四季"},
            "庚": {"nature": "锋利宝剑", "energy": "果决直接", "season_affinity": "秋"},
            "辛": {"nature": "珍贵美玉", "energy": "精致细腻", "season_affinity": "秋"},
            "壬": {"nature": "浩瀚江河", "energy": "智慧深远", "season_affinity": "冬"},
            "癸": {"nature": "清澈甘露", "energy": "润物无声", "season_affinity": "冬"}
        }
        
        # 月令环境映射
        month_environments = {
            "子": {"season": "深冬", "atmosphere": "寒冷寂静", "challenge": "需要内在的温暖"},
            "丑": {"season": "冬末", "atmosphere": "积雪未消", "challenge": "蓄势待发"},
            "寅": {"season": "初春", "atmosphere": "万物萌芽", "challenge": "把握生机"},
            "卯": {"season": "仲春", "atmosphere": "生机盎然", "challenge": "顺势成长"},
            "辰": {"season": "春末", "atmosphere": "雨水充沛", "challenge": "平衡水土"},
            "巳": {"season": "初夏", "atmosphere": "阳光明媚", "challenge": "展现活力"},
            "午": {"season": "仲夏", "atmosphere": "烈日当空", "challenge": "保持理智"},
            "未": {"season": "夏末", "atmosphere": "暑热渐退", "challenge": "收敛锋芒"},
            "申": {"season": "初秋", "atmosphere": "凉风习习", "challenge": "适应变化"},
            "酉": {"season": "仲秋", "atmosphere": "金风送爽", "challenge": "收获成果"},
            "戌": {"season": "秋末", "atmosphere": "萧瑟肃杀", "challenge": "坚持到底"},
            "亥": {"season": "初冬", "atmosphere": "万物收藏", "challenge": "积蓄力量"}
        }
        
        day_trait = day_gan_traits.get(day_gan, {"nature": "独特的存在", "energy": "独特的方式", "season_affinity": "四季"})
        month_env = month_environments.get(month_zhi, {"season": "特殊时节", "atmosphere": "独特氛围", "challenge": "面对挑战"})
        
        # 结合日主和月令创造独特的比喻
        if day_trait["season_affinity"] == month_env["season"][:1]:
            # 日主与月令相配
            metaphor = f"一株在{month_env['season']}中茁壮成长的{day_trait['nature']}"
            essence = f"您的天性与环境完美契合，能够{day_trait['energy']}地应对{month_env['atmosphere']}的挑战"
            manifestation = f"您天生就适应当前的环境节奏，能够自然而然地{day_trait['energy']}"
        else:
            # 日主与月令形成对比
            metaphor = f"一株在{month_env['season']}中依然{day_trait['energy']}的{day_trait['nature']}"
            essence = f"您的内在天性与外在环境形成有趣的对比，这种反差让您显得特别独特"
            manifestation = f"您总是用自己独特的方式应对环境，不会轻易改变自己的本性"
        
        # 加入五行最旺元素的特色
        element_enhancements = {
            "wood": "充满生命力和创造力",
            "fire": "热情洋溢且富有感染力",
            "earth": "踏实可靠且让人安心",
            "metal": "理性清晰且有原则性",
            "water": "智慧深沉且善于变通"
        }
        
        enhancement = element_enhancements.get(strongest_element, "独特的个人魅力")
        essence += f"，同时您还具有{enhancement}的特质"
        
        return {
            "metaphor": metaphor,
            "essence": essence,
            "manifestation": manifestation
        }
    
    def _generate_inner_voice_personalized(self, day_gan: str, month_zhi: str, strongest_element: str) -> str:
        """生成个性化的内心声音"""
        
        # 日主内心声音模板
        inner_voices = {
            "甲": "我要做最好的自己，不断向上成长！",
            "乙": "我会找到属于自己的方式，灵活应对一切。",
            "丙": "我的热情能感染所有人，让世界更温暖！",
            "丁": "我要用我的温暖，为身边的人带来光明。",
            "戊": "我是可靠的，大家都可以依靠我。",
            "己": "我要用我的包容，让每个人都感到舒适。",
            "庚": "我有我的原则，绝不轻易妥协！",
            "辛": "我要追求完美，做最精致的自己。",
            "壬": "我要用智慧和包容，理解这个复杂的世界。",
            "癸": "我会默默地付出，润物细无声地影响身边的人。"
        }
        
        base_voice = inner_voices.get(day_gan, "我要做真实的自己！")
        
        # 根据月令环境调整
        seasonal_adjustments = {
            "子": "即使在最困难的时候，", "丑": "虽然现在还在积累期，",
            "寅": "趁着这个好机会，", "卯": "在这个充满机遇的时刻，",
            "辰": "面对复杂的局面，", "巳": "抓住这个活力时期，",
            "午": "在这个关键时刻，", "未": "在收获的季节里，",
            "申": "面对变化的环境，", "酉": "在成熟的阶段，",
            "戌": "即使环境严峻，", "亥": "在这个积蓄的时期，"
        }
        
        adjustment = seasonal_adjustments.get(month_zhi, "")
        
        return f"{adjustment}{base_voice}"
    
    def _generate_energy_rhythm_personalized(self, day_gan: str, month_zhi: str, wuxing_stats: Dict[str, Any]) -> str:
        """生成个性化的能量节奏描述"""
        
        # 日主能量节奏特征
        rhythm_patterns = {
            "甲": "您的能量像春天的树木，稳定向上，越挫越勇",
            "乙": "您的能量像微风中的花草，柔韧而有韧性，能适应各种环境",
            "丙": "您的能量像正午的太阳，强烈而直接，影响力巨大",
            "丁": "您的能量像夜晚的烛火，温暖而持久，给人安全感",
            "戊": "您的能量像大山一样厚重，稳定而可靠，承载力强",
            "己": "您的能量像肥沃的土壤，包容而滋养，让万物生长",
            "庚": "您的能量像秋天的金属，锋利而有力，关键时刻毫不犹豫",
            "辛": "您的能量像精美的珠宝，精致而珍贵，追求完美品质",
            "壬": "您的能量像流淌的江河，深沉而智慧，包容万象",
            "癸": "您的能量像清晨的甘露，细腻而润泽，润物无声"
        }
        
        base_rhythm = rhythm_patterns.get(day_gan, "您有着独特的能量节奏")
        
        # 根据月令调整节奏描述
        seasonal_modifiers = {
            "子": "在寒冷的环境中更显坚韧", "丑": "在积累期默默蓄力",
            "寅": "在春天的推动下更加活跃", "卯": "在生机环境中自由发挥",
            "辰": "在复杂环境中保持平衡", "巳": "在充满活力的时期全力以赴",
            "午": "在高峰期发挥最大潜能", "未": "在成熟期展现丰富内涵",
            "申": "在变化中显示适应能力", "酉": "在收获期展现最好状态",
            "戌": "在挑战中显示真正实力", "亥": "在沉淀期积累更大能量"
        }
        
        modifier = seasonal_modifiers.get(month_zhi, "")
        
        # 结合五行分布情况
        strongest = wuxing_stats.get("最旺", "")
        if strongest:
            energy_note = f"目前您的{strongest}能量最为活跃，为您的整体节奏增添了更多活力。"
            return f"{base_rhythm}，{modifier}。{energy_note}"
        
        return f"{base_rhythm}，{modifier}。"
        # 例如："一条奔腾不息的大河，但河堤地基不稳"
        
        wuxing_stats = bazi_analysis.get("五行统计", {})
        geju_info = bazi_analysis.get("定格局", {})
        hanzao_info = bazi_analysis.get("定寒燥", {})
        
        strongest = wuxing_stats.get("最旺", "")
        weakest = wuxing_stats.get("最弱", "")
        strength = geju_info.get("强弱", "")
        climate = hanzao_info.get("类型", "")
        
        # 主要意象库
        metaphor_library = {
            ("water", "强"): [
                "一条奔腾不息的大河，水势浩荡但还在寻找最佳的入海口",
                "深邃的海洋，表面平静但内心波涛汹涌", 
                "智慧的深潭，能看清很多事情但有时候想得太多"
            ],
            ("water", "弱"): [
                "一泓清澈的山泉，虽然细小但源源不断地滋养着周围",
                "晨露般的纯净，需要阳光的温暖才能展现出璀璨的光芒"
            ],
            ("wood", "强"): [
                "一片茂密的森林，生机勃勃但需要适当的修剪才能长得更好",
                "向天空伸展的大树，根深叶茂但有时枝干过于繁杂"
            ],
            ("wood", "弱"): [
                "春天的嫩芽，虽然柔弱但充满了向上生长的力量",
                "等待合适时机的种子，一旦条件成熟就会破土而出"
            ],
            ("fire", "强"): [
                "熊熊燃烧的篝火，光芒四射但需要找到值得照亮的方向",
                "正午的太阳，热情洋溢但有时会让人感到炙热"
            ],
            ("fire", "弱"): [
                "温暖的烛光，虽然不够明亮但足以照亮身边最重要的人",
                "黎明前的第一缕阳光，温和而珍贵"
            ],
            ("earth", "强"): [
                "厚重的大地，承载力强大但需要找到最值得培育的种子",
                "稳固的山峰，巍峨不动但等待着成为他人攀登的基石"
            ],
            ("earth", "弱"): [
                "肥沃的土壤，虽然谦逊低调但正在孕育着惊人的生命力",
                "宁静的花园，等待着合适的季节绽放"
            ],
            ("metal", "强"): [
                "锋利的宝剑，削铁如泥但还需要找到最值得守护的事物",
                "精钢般的意志，坚硬无比但需要合适的磨砺才能成器"
            ],
            ("metal", "弱"): [
                "待磨砺的璞玉，虽未成型但已蕴含着令人惊艳的光华",
                "深藏的宝矿，等待着慧眼识珠的人来发掘其真正价值"
            ]
        }
        
        # 基于最旺元素和强弱生成主要意象
        element_map = {"木": "wood", "火": "fire", "土": "earth", "金": "metal", "水": "water"}
        main_element = element_map.get(strongest.replace("元素", ""), "earth")
        
        key = (main_element, strength)
        base_metaphors = metaphor_library.get(key, metaphor_library.get((main_element, "中"), [
            "独特的能量组合，正在寻找属于自己的表达方式"
        ]))
        
        base_metaphor = random.choice(base_metaphors)
        
        # 添加调候修饰
        if climate in ["寒重", "燥重"]:
            climate_info = self.climate_contexts[climate]
            return f"{climate_info['modifier']}，您就像{base_metaphor}。{climate_info['need']}。"
        
        return f"您就像{base_metaphor}。"
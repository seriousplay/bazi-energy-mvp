"""
增强解读引擎
Enhanced Interpretation Engine

整合所有分析模块，提供完整的LLM增强八字解读服务：
1. 智能命局判定（juju_detector）
2. 深度问题分析（deep_question_analyzer）
3. 意识能量画像生成（energy_portrait_generator）
4. 启发式问题引导（inspiration_guide）
5. 个性化解决方案（personalized_solution_generator）
6. 大白话转换（plain_language_converter）
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json

# 导入所有分析模块
from juju_detector import detect_jugotype, build_prompt, JUJU_KEYWORDS
from deep_question_analyzer import DeepQuestionAnalyzer, QuestionAnalysis
from energy_portrait_generator import EnergyPortraitGenerator, EnergyPortrait
from inspiration_guide import InspirationGuide, InspirationResult
from personalized_solution_generator import PersonalizedSolutionGenerator, PersonalizedSolution
from plain_language_converter import PlainLanguageConverter

@dataclass
class EnhancedInterpretationResult:
    """增强解读结果"""
    user_info: Dict[str, Any]           # 用户基本信息
    bazi_display: Dict[str, Any]        # 八字显示信息
    dayun_info: Dict[str, Any]          # 大运信息
    energy_portrait: EnergyPortrait     # 能量画像
    question_analysis: QuestionAnalysis # 问题分析
    inspiration_guide: InspirationResult # 启发引导
    personalized_solution: PersonalizedSolution # 个性化方案
    plain_language_summary: Dict[str, str] # 大白话总结
    juju_detection: Dict[str, Any]      # 命局判定详情
    enhanced_bingyao: Dict[str, Any]    # 增强病药分析

class EnhancedInterpretationEngine:
    """增强解读引擎"""
    
    def __init__(self):
        self.question_analyzer = DeepQuestionAnalyzer()
        self.portrait_generator = EnergyPortraitGenerator()
        self.inspiration_guide = InspirationGuide()
        self.solution_generator = PersonalizedSolutionGenerator()
        self.language_converter = PlainLanguageConverter()
    
    def comprehensive_enhanced_analysis(self, structured_result: Dict[str, Any], 
                                      user_question: str = "", 
                                      user_info: Dict[str, Any] = None) -> EnhancedInterpretationResult:
        """执行完整的增强分析"""
        
        # 1. 准备分析数据
        analysis_data = self._prepare_analysis_data(structured_result)
        
        # 2. 智能命局判定
        juju_detection = detect_jugotype(analysis_data)
        
        # 3. 深度问题分析
        question_analysis = self.question_analyzer.analyze_question(user_question, structured_result)
        
        # 4. 生成能量画像
        energy_portrait = self.portrait_generator.generate_portrait(structured_result, juju_detection)
        
        # 5. 启发式引导
        inspiration_result = self.inspiration_guide.generate_inspiration(question_analysis, structured_result)
        
        # 6. 个性化解决方案
        bingyao_data = structured_result.get("定病药", {})
        personalized_solution = self.solution_generator.generate_solution(
            structured_result, question_analysis, bingyao_data
        )
        
        # 7. 大白话转换
        plain_language_summary = self.language_converter.convert_to_plain_language(structured_result)
        
        # 8. 增强病药分析（调候 + 强弱双重逻辑）
        enhanced_bingyao = self._generate_enhanced_bingyao(structured_result, juju_detection)
        
        # 9. 优化大运显示
        dayun_info = self._enhance_dayun_display(structured_result.get("看大运", {}), structured_result)
        
        return EnhancedInterpretationResult(
            user_info=user_info or {},
            bazi_display=structured_result.get("bazi", {}),
            dayun_info=dayun_info,
            energy_portrait=energy_portrait,
            question_analysis=question_analysis,
            inspiration_guide=inspiration_result,
            personalized_solution=personalized_solution,
            plain_language_summary=plain_language_summary,
            juju_detection=juju_detection,
            enhanced_bingyao=enhanced_bingyao
        )
    
    def _prepare_analysis_data(self, structured_result: Dict[str, Any]) -> Dict[str, Any]:
        """准备用于juju_detector的分析数据"""
        
        # 构建十神表（需要从现有数据中提取或生成）
        ten_gods_table = self._build_ten_gods_table(structured_result)
        
        # 准备五行分数
        wuxing_stats = structured_result.get("五行统计", {})
        five_elements_scores = {
            "wood": wuxing_stats.get("wood", 0),
            "fire": wuxing_stats.get("fire", 0),
            "earth": wuxing_stats.get("earth", 0),
            "metal": wuxing_stats.get("metal", 0),
            "water": wuxing_stats.get("water", 0)
        }
        
        # 提取八字原始数据
        bazi_info = structured_result.get("bazi", {})
        bazi_raw = {
            "stems": [bazi_info.get("year", "")[0], bazi_info.get("month", "")[0], 
                     bazi_info.get("day", "")[0], bazi_info.get("hour", "")[0]],
            "branches": [bazi_info.get("year", "")[1], bazi_info.get("month", "")[1], 
                        bazi_info.get("day", "")[1], bazi_info.get("hour", "")[1]]
        }
        
        # 确定日干和日主五行
        day_gan = bazi_info.get("day", "")[0] if bazi_info.get("day") else ""
        day_element = self._get_element_from_gan(day_gan)
        
        return {
            "十神表": ten_gods_table,
            "五行分数": five_elements_scores,
            "bazi_raw": bazi_raw,
            "day_element": day_element,
            "日干": day_gan
        }
    
    def _build_ten_gods_table(self, structured_result: Dict[str, Any]) -> Dict[str, str]:
        """构建十神表"""
        bazi_info = structured_result.get("bazi", {})
        day_gan = bazi_info.get("day", "")[0] if bazi_info.get("day") else ""
        
        ten_gods_table = {}
        pillars = ["year", "month", "day", "hour"]
        
        for i, pillar in enumerate(pillars):
            if pillar in bazi_info:
                pillar_str = bazi_info[pillar]
                if len(pillar_str) >= 2:
                    gan = pillar_str[0]
                    ten_god = self._calculate_ten_god(day_gan, gan)
                    ten_gods_table[f"柱{i+1}_天干_{gan}"] = ten_god
        
        return ten_gods_table
    
    def _calculate_ten_god(self, day_gan: str, other_gan: str) -> str:
        """计算十神关系（简化版）"""
        # 导入现有的十神计算函数
        try:
            from bazi_engine_d1d2 import determine_ten_god
            return determine_ten_god(day_gan, other_gan)
        except Exception as e:
            # 简化的十神计算逻辑
            if day_gan == other_gan:
                return "比肩"
            return "比肩"  # 默认值
    
    def _get_element_from_gan(self, gan: str) -> str:
        """从天干获取五行"""
        gan_element_map = {
            "甲": "wood", "乙": "wood",
            "丙": "fire", "丁": "fire",
            "戊": "earth", "己": "earth", 
            "庚": "metal", "辛": "metal",
            "壬": "water", "癸": "water"
        }
        return gan_element_map.get(gan, "earth")
    
    def _generate_enhanced_bingyao(self, structured_result: Dict[str, Any], 
                                  juju_detection: Dict[str, Any]) -> Dict[str, Any]:
        """生成增强的病药分析（调候 + 强弱双重逻辑）"""
        
        hanzao_info = structured_result.get("定寒燥", {})
        bingyao_info = structured_result.get("定病药", {})
        primary_types = juju_detection.get("primary", [])
        
        enhanced_analysis = {
            "双重病根分析": [],
            "综合用药策略": {},
            "意识层面指导": {}
        }
        
        # 调候病根
        climate_type = hanzao_info.get("类型", "")
        if "寒" in climate_type:
            enhanced_analysis["双重病根分析"].append({
                "病根类型": "调候病 - 寒性",
                "具体表现": "内在能量偏向收敛，缺乏外在的热情和行动力",
                "需要的药": "火性能量（热情、行动、表达）",
                "生活体现": "可能经常感到缺乏动力，需要外界的鼓励和推动"
            })
        elif "燥" in climate_type:
            enhanced_analysis["双重病根分析"].append({
                "病根类型": "调候病 - 燥性", 
                "具体表现": "内在能量过于外放，容易急躁和消耗",
                "需要的药": "水性能量（冷静、思考、沉淀）",
                "生活体现": "可能经常感到焦虑急躁，需要学会慢下来思考"
            })
        
        # 强弱病根
        if primary_types:
            main_type = primary_types[0]
            if "旺" in main_type:
                enhanced_analysis["双重病根分析"].append({
                    "病根类型": f"强弱病 - {main_type}",
                    "具体表现": f"某种能量过于强盛，需要平衡和疏导",
                    "需要的药": "相应的制衡能量",
                    "生活体现": "在某些方面可能过于执着，需要学会适当放松"
                })
        
        # 综合用药策略
        if bingyao_info.get("分级"):
            medicine_config = bingyao_info["分级"][0].get("病药配置", {})
            for level, medicine in medicine_config.items():
                enhanced_analysis["综合用药策略"][level] = {
                    "药名": medicine,
                    "意识指导": self._get_medicine_consciousness_guidance(medicine, "positive"),
                    "实践建议": self._get_medicine_practice_advice(medicine)
                }
        
        return enhanced_analysis
    
    def _get_medicine_consciousness_guidance(self, medicine: str, mode: str = "positive") -> str:
        """获取药物的意识指导"""
        consciousness_map = {
            "比肩": {
                "positive": "培养内在的底气和自信，相信自己有能力独立处理各种情况",
                "negative": "避免过分自我中心，学会倾听他人的意见"
            },
            "劫财": {
                "positive": "发挥团队协作精神，在合作中实现共赢",
                "negative": "避免过度竞争，学会分享和包容"
            },
            "食神": {
                "positive": "发挥理性思考能力，做好长远规划",
                "negative": "避免过分挑剔，学会接受不完美"
            },
            "伤官": {
                "positive": "发挥创造力和表达能力，勇于突破传统",
                "negative": "避免过分叛逆，学会在创新中保持建设性"
            },
            "正财": {
                "positive": "培养目标意识和执行力，创造实际价值",
                "negative": "避免过分功利，保持人情味"
            },
            "偏财": {
                "positive": "发挥机会意识和行动力，敢于尝试新领域",
                "negative": "避免投机心理，保持长远眼光"
            },
            "正官": {
                "positive": "发挥责任心和规则意识，建立威信",
                "negative": "避免过分保守，保持适度的灵活性"
            },
            "七杀": {
                "positive": "发挥承压能力和决断力，在困难中成长",
                "negative": "避免过分严苛，学会温和处理问题"
            },
            "正印": {
                "positive": "发挥学习能力和智慧积累，成为可靠的专家",
                "negative": "避免过分依赖，培养独立行动的勇气"
            },
            "偏印": {
                "positive": "发挥独特的洞察力和创新思维",
                "negative": "避免过分孤立，保持与他人的连接"
            }
        }
        
        guidance_map = consciousness_map.get(medicine, {})
        return guidance_map.get(mode, f"发挥{medicine}的正向能量")
    
    def _get_medicine_practice_advice(self, medicine: str) -> str:
        """获取药物的实践建议"""
        practice_advice = {
            "比肩": "每天给自己一些独立决策的机会，从小事开始建立自信",
            "劫财": "参与团队活动，在合作中学会既坚持自己又支持他人",
            "食神": "培养一个需要长期坚持的爱好，比如读书、写作、学习技能",
            "伤官": "找到适合的创意表达渠道，比如艺术、写作、设计等",
            "正财": "设定具体可达成的目标，制定详细的行动计划并执行",
            "偏财": "多关注新的机会和趋势，但要有选择地投入",
            "正官": "主动承担有意义的责任，在完成任务中建立威信",
            "七杀": "接受有挑战性的任务，在压力中锻炼自己的能力",
            "正印": "持续学习新知识，同时也要敢于分享自己的见解",
            "偏印": "培养独特的技能或爱好，发展自己的专业优势"
        }
        
        return practice_advice.get(medicine, f"在日常生活中有意识地运用{medicine}的能量")
    
    def _enhance_dayun_display(self, dayun_data: Dict[str, Any], structured_result: Dict[str, Any]) -> Dict[str, Any]:
        """增强大运显示信息 - 添加扶抑判断和机遇挑战分析"""
        if not dayun_data:
            return {}
        
        enhanced_dayun = dayun_data.copy()
        
        # 获取命局基本信息
        geju_info = structured_result.get("定格局", {})
        geju_type = geju_info.get("格局类型", "")
        day_element = geju_info.get("详情", {}).get("day_element", "fire")
        
        wuxing_stats = structured_result.get("五行统计", {})
        bazi_info = structured_result.get("bazi", {})
        day_gan = bazi_info.get("day", "甲子")[0] if bazi_info.get("day") else "甲"
        
        # 为当前大运添加详细解释
        current_dayun = dayun_data.get("当前大运", {})
        if current_dayun:
            enhanced_current = current_dayun.copy()
            age_range = current_dayun.get("age_range", "")
            dayun_gan = current_dayun.get("gan", "甲")
            dayun_zhi = current_dayun.get("zhi", "子")
            
            # 扶抑分析
            balance_analysis = self._analyze_dayun_balance_effect(
                day_gan, dayun_gan, dayun_zhi, geju_type, wuxing_stats
            )
            enhanced_current.update(balance_analysis)
            
            # 机遇挑战分析
            opportunity_analysis = self._analyze_dayun_opportunities_challenges(
                dayun_gan, dayun_zhi, age_range, geju_type
            )
            enhanced_current.update(opportunity_analysis)
            
            # 添加阶段性特征描述
            stage_descriptions = {
                "20-29": "探索和建立基础的关键阶段，重要的是找到自己的方向",
                "30-39": "发展和积累的黄金阶段，适合专注于能力建设和事业发展", 
                "40-49": "收获和影响的成熟阶段，可以考虑更大的责任和挑战",
                "50-59": "智慧和传承的深化阶段，适合分享经验和培养他人",
                "60-69": "享受和反思的安定阶段，重点是保持健康和内心平静"
            }
            
            # 匹配年龄段
            for age_desc, stage_desc in stage_descriptions.items():
                if any(age in age_range for age in age_desc.split("-")):
                    enhanced_current["人生阶段"] = stage_desc
                    break
            
            enhanced_dayun["当前大运"] = enhanced_current
        
        # 为未来大运添加详细分析
        future_dayuns = dayun_data.get("未来大运", [])
        if future_dayuns:
            enhanced_future = []
            for i, dayun in enumerate(future_dayuns[:3]):  # 只显示未来3步大运
                enhanced_dayun_item = dayun.copy()
                
                # 趋势分析
                trend_analysis = self._analyze_dayun_trend(
                    dayun.get("gan", "甲"), dayun.get("zhi", "子"), 
                    geju_type, i + 1
                )
                enhanced_dayun_item.update(trend_analysis)
                
                enhanced_future.append(enhanced_dayun_item)
            
            enhanced_dayun["未来大运"] = enhanced_future
        
        # 生成生命能量趋势图数据
        energy_timeline = self._generate_energy_timeline(
            current_dayun, future_dayuns, structured_result
        )
        enhanced_dayun["能量趋势图"] = energy_timeline
        
        return enhanced_dayun
    
    def _analyze_dayun_balance_effect(self, day_gan: str, dayun_gan: str, dayun_zhi: str, 
                                    geju_type: str, wuxing_stats: Dict[str, Any]) -> Dict[str, str]:
        """分析大运对命局平衡的影响"""
        
        # 大运五行属性
        gan_elements = {
            "甲": "wood", "乙": "wood", "丙": "fire", "丁": "fire",
            "戊": "earth", "己": "earth", "庚": "metal", "辛": "metal", 
            "壬": "water", "癸": "water"
        }
        
        zhi_elements = {
            "子": "water", "丑": "earth", "寅": "wood", "卯": "wood",
            "辰": "earth", "巳": "fire", "午": "fire", "未": "earth",
            "申": "metal", "酉": "metal", "戌": "earth", "亥": "water"
        }
        
        dayun_gan_element = gan_elements.get(dayun_gan, "earth")
        dayun_zhi_element = zhi_elements.get(dayun_zhi, "earth")
        day_gan_element = gan_elements.get(day_gan, "fire")
        
        # 获取当前最旺和最弱的五行
        strongest = wuxing_stats.get("最旺", "")
        weakest = wuxing_stats.get("最弱", "")
        
        balance_effects = []
        
        # 分析天干影响
        if dayun_gan_element == day_gan_element:
            balance_effects.append("大运天干与日主同类，增强您的核心能量")
        elif self._is_beneficial_element(dayun_gan_element, day_gan_element, geju_type):
            balance_effects.append("大运天干对您有利，带来正面的能量支持")
        else:
            balance_effects.append("大运天干带来挑战，需要调整应对策略")
        
        # 分析地支影响
        if dayun_zhi_element in weakest:
            balance_effects.append("大运地支补强您最弱的五行，有助于能量平衡")
        elif dayun_zhi_element in strongest:
            balance_effects.append("大运地支进一步加强您的优势五行，需要注意过犹不及")
        
        # 综合判断趋势
        if "扶抑" in geju_type or "平衡" in geju_type:
            if len([e for e in balance_effects if "有利" in e or "补强" in e]) > len([e for e in balance_effects if "挑战" in e]):
                balance_trend = "整体趋于平衡"
            else:
                balance_trend = "需要加强平衡调节"
        else:
            balance_trend = "保持现有格局特色"
        
        return {
            "平衡分析": "；".join(balance_effects),
            "平衡趋势": balance_trend
        }
    
    def _analyze_dayun_opportunities_challenges(self, dayun_gan: str, dayun_zhi: str, 
                                              age_range: str, geju_type: str) -> Dict[str, str]:
        """分析大运的机遇和挑战"""
        
        # 基于大运干支的机遇分析
        opportunities_map = {
            "甲": "创新突破的机遇，适合开拓新领域",
            "乙": "灵活适应的机遇，适合多元化发展", 
            "丙": "展现魅力的机遇，适合公众表现",
            "丁": "深化专精的机遇，适合技能提升",
            "戊": "稳固基础的机遇，适合长远规划",
            "己": "整合资源的机遇，适合平台建设",
            "庚": "果断决策的机遇，适合改革变化", 
            "辛": "精益求精的机遇，适合品质提升",
            "壬": "拓展视野的机遇，适合学习交流",
            "癸": "内在成长的机遇，适合修身养性"
        }
        
        challenges_map = {
            "甲": "过于固执的挑战，需要保持开放心态",
            "乙": "缺乏坚持的挑战，需要增强定力",
            "丙": "过度张扬的挑战，需要适度收敛",
            "丁": "过分挑剔的挑战，需要包容心态",
            "戊": "过于保守的挑战，需要适度创新",
            "己": "过度依赖的挑战，需要增强独立性",
            "庚": "过于严厉的挑战，需要保持温和",
            "辛": "过分计较的挑战，需要大度包容",
            "壬": "过于理想的挑战，需要脚踏实地",
            "癸": "过分内敛的挑战，需要主动表达"
        }
        
        # 基于年龄段的特殊建议
        age_specific_advice = {
            "20-29": "这个阶段要勇于尝试，不怕犯错，积累经验最重要",
            "30-39": "这个阶段要专注发展，建立专业优势，为未来奠定基础",
            "40-49": "这个阶段要承担责任，发挥影响力，帮助他人成长",
            "50-59": "这个阶段要传承智慧，享受成果，保持身心健康",
            "60-69": "这个阶段要安享生活，反思人生，准备下一个阶段"
        }
        
        opportunities = opportunities_map.get(dayun_gan, "寻找适合的发展机会")
        challenges = challenges_map.get(dayun_gan, "需要注意平衡发展")
        
        # 匹配年龄段建议
        age_advice = ""
        for age_desc, advice in age_specific_advice.items():
            if any(age in age_range for age in age_desc.split("-")):
                age_advice = advice
                break
        
        return {
            "关键机遇": opportunities,
            "主要挑战": challenges,
            "阶段建议": age_advice or "顺应自然规律，把握当下机会"
        }
    
    def _analyze_dayun_trend(self, dayun_gan: str, dayun_zhi: str, geju_type: str, step: int) -> Dict[str, str]:
        """分析未来大运趋势"""
        
        trend_descriptions = {
            1: f"第{step}步大运将是重要的转折期，需要提前做好准备",
            2: f"第{step}步大运将进入新的发展阶段，要有长远眼光",
            3: f"第{step}步大运将是成熟稳定期，可以享受之前的积累"
        }
        
        return {
            "趋势展望": trend_descriptions.get(step, "未来发展趋势")
        }
    
    def _is_beneficial_element(self, dayun_element: str, day_element: str, geju_type: str) -> bool:
        """判断大运五行对日主是否有利"""
        
        beneficial_relations = {
            "wood": ["water"],  # 水生木
            "fire": ["wood"],   # 木生火
            "earth": ["fire"],  # 火生土
            "metal": ["earth"], # 土生金
            "water": ["metal"]  # 金生水
        }
        
        return dayun_element in beneficial_relations.get(day_element, [])
    
    def _generate_energy_timeline(self, current_dayun: Dict[str, Any], future_dayuns: List[Dict[str, Any]], 
                                structured_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成生命能量趋势图数据"""
        
        timeline_data = {
            "chart_type": "energy_trend",
            "x_axis": "年龄",
            "y_axis": "生命能量指数",
            "data_points": [],
            "interactive_nodes": []
        }
        
        # 获取基础能量水平
        wuxing_stats = structured_result.get("五行统计", {})
        base_energy = self._calculate_base_energy(wuxing_stats)
        
        # 当前大运节点
        if current_dayun:
            current_age_range = current_dayun.get("age_range", "39-48")
            current_ages = self._parse_age_range(current_age_range)
            current_energy = self._calculate_dayun_energy(current_dayun, base_energy)
            
            timeline_data["data_points"].append({
                "age": current_ages[0],
                "energy": current_energy,
                "label": f"当前大运",
                "dayun": f"{current_dayun.get('gan', '')}${current_dayun.get('zhi', '')}"
            })
            
            timeline_data["interactive_nodes"].append({
                "age": current_ages[0],
                "title": f"当前大运 {current_dayun.get('gan', '')}{current_dayun.get('zhi', '')}",
                "energy_level": current_energy,
                "opportunities": current_dayun.get("关键机遇", ""),
                "challenges": current_dayun.get("主要挑战", ""),
                "balance_trend": current_dayun.get("平衡趋势", ""),
                "advice": current_dayun.get("阶段建议", ""),
                "color": self._get_energy_color(current_energy)
            })
        
        # 未来大运节点
        for i, future_dayun in enumerate(future_dayuns[:5]):  # 显示未来5步大运
            age_range = future_dayun.get("age_range", f"{49+i*10}-{58+i*10}")
            ages = self._parse_age_range(age_range)
            energy = self._calculate_dayun_energy(future_dayun, base_energy)
            
            timeline_data["data_points"].append({
                "age": ages[0],
                "energy": energy,
                "label": f"第{i+1}步大运",
                "dayun": f"{future_dayun.get('gan', '')}{future_dayun.get('zhi', '')}"
            })
            
            timeline_data["interactive_nodes"].append({
                "age": ages[0],
                "title": f"第{i+1}步大运 {future_dayun.get('gan', '')}{future_dayun.get('zhi', '')}",
                "energy_level": energy,
                "trend": future_dayun.get("趋势展望", ""),
                "key_focus": self._get_dayun_focus(future_dayun.get('gan', ''), ages[0]),
                "preparation": f"提前{10-i*2}年开始准备相关技能和资源",
                "color": self._get_energy_color(energy)
            })
        
        # 生成平滑的能量曲线
        timeline_data["smooth_curve"] = self._generate_smooth_curve(timeline_data["data_points"])
        
        return timeline_data
    
    def _calculate_base_energy(self, wuxing_stats: Dict[str, Any]) -> float:
        """计算基础能量水平"""
        # 基于五行分布计算基础能量指数
        total_energy = sum([
            wuxing_stats.get("wood", 0),
            wuxing_stats.get("fire", 0),
            wuxing_stats.get("earth", 0),
            wuxing_stats.get("metal", 0),
            wuxing_stats.get("water", 0)
        ])
        
        # 归一化到0-100区间
        base_energy = min(100, max(20, total_energy * 10))
        
        return base_energy
    
    def _parse_age_range(self, age_range: str) -> List[int]:
        """解析年龄区间"""
        try:
            ages = [int(x) for x in age_range.split("-")]
            return ages
        except:
            return [39, 48]  # 默认值
    
    def _calculate_dayun_energy(self, dayun: Dict[str, Any], base_energy: float) -> float:
        """计算大运期的能量水平"""
        # 基于大运干支的能量影响
        gan_energy_impact = {
            "甲": 10, "乙": 5, "丙": 15, "丁": 8,
            "戊": 3, "己": 0, "庚": 12, "辛": 7,
            "壬": 13, "癸": 6
        }
        
        zhi_energy_impact = {
            "子": 8, "丑": 2, "寅": 12, "卯": 10,
            "辰": 4, "巳": 14, "午": 16, "未": 6,
            "申": 11, "酉": 9, "戌": 5, "亥": 7
        }
        
        gan_impact = gan_energy_impact.get(dayun.get("gan", ""), 0)
        zhi_impact = zhi_energy_impact.get(dayun.get("zhi", ""), 0)
        
        # 计算调整后的能量水平
        adjusted_energy = base_energy + (gan_impact + zhi_impact) - 10
        
        return min(100, max(10, adjusted_energy))
    
    def _get_energy_color(self, energy_level: float) -> str:
        """根据能量水平获取颜色"""
        if energy_level >= 80:
            return "#ff4444"  # 高能量-红色
        elif energy_level >= 60:
            return "#ff8800"  # 中高能量-橙色
        elif energy_level >= 40:
            return "#44aa44"  # 中等能量-绿色
        else:
            return "#4488cc"  # 低能量-蓝色
    
    def _get_dayun_focus(self, dayun_gan: str, age: int) -> str:
        """获取大运的重点关注领域"""
        focus_map = {
            "甲": "创新创业，开拓新方向",
            "乙": "灵活适应，多元发展",
            "丙": "公众影响，魅力展现",
            "丁": "专业精进，技能提升",
            "戊": "稳固根基，长远规划",
            "己": "整合资源，平台建设",
            "庚": "改革决断，效率优化",
            "辛": "品质追求，精益求精",
            "壬": "视野拓展，智慧积累",
            "癸": "内在成长，修身养性"
        }
        
        base_focus = focus_map.get(dayun_gan, "全面发展")
        
        # 根据年龄段调整重点
        if age < 30:
            return f"{base_focus}，重点是学习和积累"
        elif age < 50:
            return f"{base_focus}，重点是发展和突破"
        else:
            return f"{base_focus}，重点是传承和享受"
    
    def _generate_smooth_curve(self, data_points: List[Dict]) -> List[Dict]:
        """生成平滑的能量曲线"""
        if len(data_points) < 2:
            return data_points
        
        smooth_curve = []
        for i in range(len(data_points) - 1):
            current = data_points[i]
            next_point = data_points[i + 1]
            
            # 在两个点之间插入中间点
            age_diff = next_point["age"] - current["age"]
            energy_diff = next_point["energy"] - current["energy"]
            
            for j in range(0, age_diff, 2):  # 每2岁一个点
                smooth_age = current["age"] + j
                smooth_energy = current["energy"] + (energy_diff * j / age_diff)
                smooth_curve.append({
                    "age": smooth_age,
                    "energy": smooth_energy
                })
        
        return smooth_curve
    
    def generate_final_report(self, enhanced_result: EnhancedInterpretationResult) -> Dict[str, Any]:
        """生成最终报告"""
        
        # 构建报告的各个部分
        report_sections = {}
        
        # 1. 用户基本信息
        report_sections["用户信息"] = enhanced_result.user_info
        
        # 2. 八字显示（使用新格式）
        report_sections["bazi"] = enhanced_result.bazi_display
        
        # 3. 大运信息（新增）
        report_sections["大运信息"] = enhanced_result.dayun_info
        
        # 4. 智能命局判定结果
        primary_types = enhanced_result.juju_detection.get("primary", [])
        report_sections["命局判定"] = {
            "主要类型": primary_types,
            "判定详情": enhanced_result.juju_detection.get("details", {}),
            "候选类型": enhanced_result.juju_detection.get("candidates", []),
            "plain_descriptions": enhanced_result.juju_detection.get("plain_descriptions", {})
        }
        
        # 5. 能量画像
        portrait = enhanced_result.energy_portrait
        report_sections["能量画像"] = {
            "核心意象": portrait.core_image,
            "详细描述": portrait.detailed_description,
            "生活体现": portrait.life_manifestation,
            "内心声音": portrait.inner_voice,
            "能量节奏": portrait.energy_rhythm
        }
        
        # 6. 问题深度分析
        question_analysis = enhanced_result.question_analysis
        if question_analysis.original_question:
            report_sections["问题分析"] = {
                "原始问题": question_analysis.original_question,
                "问题类别": question_analysis.question_category,
                "深层动机": question_analysis.deep_motivation,
                "重要性分析": question_analysis.why_important,
                "核心议题": question_analysis.core_issue,
                "重新框定": question_analysis.reframed_question
            }
        
        # 7. 启发式引导
        inspiration = enhanced_result.inspiration_guide
        report_sections["启发引导"] = {
            "重新框定的视角": inspiration.reframed_perspective,
            "深层反思问题": inspiration.deeper_questions,
            "多角度思考": inspiration.multiple_angles,
            "智慧洞察": inspiration.wisdom_insights,
            "意识提升": inspiration.consciousness_elevation
        }
        
        # 8. 个性化解决方案
        solution = enhanced_result.personalized_solution
        report_sections["个性化方案"] = {
            "优势模式": solution.strength_patterns,
            "温馨提醒": solution.blind_spots,
            "行动建议": solution.actionable_steps,
            "用药指导": solution.medicine_guidance,
            "时机建议": solution.timing_advice,
            "能量管理": solution.energy_management
        }
        
        # 9. 增强病药分析
        report_sections["增强病药"] = enhanced_result.enhanced_bingyao
        
        # 10. 大白话总结
        report_sections["大白话说明"] = enhanced_result.plain_language_summary
        
        # 11. 原始分析数据（供前端兼容）
        report_sections["五行统计"] = enhanced_result.bazi_display
        
        return report_sections


# 主要接口函数
def generate_enhanced_interpretation(structured_result: Dict[str, Any], 
                                   user_question: str = "",
                                   user_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """生成增强解读（主要接口）"""
    engine = EnhancedInterpretationEngine()
    
    # 执行增强分析
    enhanced_result = engine.comprehensive_enhanced_analysis(
        structured_result, user_question, user_info
    )
    
    # 生成最终报告
    final_report = engine.generate_final_report(enhanced_result)
    
    return final_report
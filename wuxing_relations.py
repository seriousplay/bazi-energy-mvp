"""
五行生克关系分析模块
Five Elements Energy Relationship Analysis Module
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class ElementType(Enum):
    """五行类型"""
    WOOD = "wood"    # 木
    FIRE = "fire"    # 火
    EARTH = "earth"  # 土
    METAL = "metal"  # 金
    WATER = "water"  # 水

class RelationType(Enum):
    """关系类型"""
    GENERATE = "generate"  # 相生
    OVERCOME = "overcome"  # 相克
    NEUTRAL = "neutral"    # 中性

@dataclass
class ElementRelation:
    """五行关系"""
    from_element: ElementType
    to_element: ElementType
    relation_type: RelationType
    strength: float  # 关系强度 0-1
    description: str

@dataclass
class BreakpointEnergy:
    """断点能量"""
    element: ElementType
    position: int  # 在循环中的位置
    break_type: str  # 断点类型：缺失/过弱/受阻
    impact_level: float  # 影响程度 0-1
    remedy_elements: List[ElementType]  # 补救五行

class WuxingRelationAnalyzer:
    """五行关系分析器"""
    
    def __init__(self):
        # 五行相生关系 (生成循环)
        self.generation_cycle = {
            ElementType.WOOD: ElementType.FIRE,   # 木生火
            ElementType.FIRE: ElementType.EARTH,  # 火生土
            ElementType.EARTH: ElementType.METAL, # 土生金
            ElementType.METAL: ElementType.WATER, # 金生水
            ElementType.WATER: ElementType.WOOD   # 水生木
        }
        
        # 五行相克关系 (克制循环)
        self.overcoming_cycle = {
            ElementType.WOOD: ElementType.EARTH,  # 木克土
            ElementType.FIRE: ElementType.METAL,  # 火克金
            ElementType.EARTH: ElementType.WATER, # 土克水
            ElementType.METAL: ElementType.WOOD,  # 金克木
            ElementType.WATER: ElementType.FIRE   # 水克火
        }
        
        # 五行中文名称映射
        self.element_names = {
            ElementType.WOOD: "木",
            ElementType.FIRE: "火", 
            ElementType.EARTH: "土",
            ElementType.METAL: "金",
            ElementType.WATER: "水"
        }
        
        # 十神与五行对应关系 (相对于日干)
        self.ten_god_elements = {
            "比劫": "self",     # 比肩劫财 - 同五行
            "印星": "generate_self",  # 正印偏印 - 生日干
            "伤官": "generated_by_self", # 食神伤官 - 日干所生
            "财星": "overcome_by_self",  # 正财偏财 - 日干所克
            "官杀": "overcome_self"     # 正官七杀 - 克日干
        }
    
    def analyze_element_relations(self, bazi_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析八字中的五行关系"""
        
        # 提取五行统计数据
        wuxing_stats = bazi_data.get("五行统计", {})
        
        # 获取各五行的能量值
        element_energies = {
            ElementType.WOOD: wuxing_stats.get("wood", 0),
            ElementType.FIRE: wuxing_stats.get("fire", 0),
            ElementType.EARTH: wuxing_stats.get("earth", 0),
            ElementType.METAL: wuxing_stats.get("metal", 0),
            ElementType.WATER: wuxing_stats.get("water", 0)
        }
        
        # 分析生克关系
        relations = self._analyze_generation_relations(element_energies)
        relations.extend(self._analyze_overcoming_relations(element_energies))
        
        # 检测断点能量
        breakpoints = self._detect_energy_breakpoints(element_energies)
        
        # 计算循环流畅度
        flow_analysis = self._analyze_energy_flow(element_energies)
        
        # 生成关系图数据
        relationship_graph = self._generate_relationship_graph(element_energies, relations)
        
        return {
            "element_energies": {k.value: v for k, v in element_energies.items()},
            "relations": [self._relation_to_dict(r) for r in relations],
            "breakpoints": [self._breakpoint_to_dict(b) for b in breakpoints],
            "flow_analysis": flow_analysis,
            "relationship_graph": relationship_graph,
            "summary": self._generate_summary(element_energies, breakpoints, flow_analysis)
        }
    
    def _analyze_generation_relations(self, energies: Dict[ElementType, float]) -> List[ElementRelation]:
        """分析相生关系"""
        relations = []
        
        for generator, generated in self.generation_cycle.items():
            generator_energy = energies[generator]
            generated_energy = energies[generated]
            
            # 计算生成关系强度
            if generator_energy > 0:
                # 生成强度基于生成者能量和被生者需求
                base_strength = min(generator_energy / 3.0, 1.0)  # 生成者提供能力
                need_factor = max(0.1, 1.0 - generated_energy / 2.0)  # 被生者需求程度
                strength = base_strength * need_factor
                
                description = f"{self.element_names[generator]}生{self.element_names[generated]}"
                if strength > 0.7:
                    description += " (强生)"
                elif strength > 0.4:
                    description += " (中生)"
                else:
                    description += " (弱生)"
                
                relations.append(ElementRelation(
                    from_element=generator,
                    to_element=generated,
                    relation_type=RelationType.GENERATE,
                    strength=strength,
                    description=description
                ))
        
        return relations
    
    def _analyze_overcoming_relations(self, energies: Dict[ElementType, float]) -> List[ElementRelation]:
        """分析相克关系"""
        relations = []
        
        for overcomer, overcomed in self.overcoming_cycle.items():
            overcomer_energy = energies[overcomer]
            overcomed_energy = energies[overcomed]
            
            # 计算相克关系强度
            if overcomer_energy > 0:
                # 克制强度基于克制者能量和被克者抵抗力
                attack_strength = min(overcomer_energy / 2.0, 1.0)  # 攻击强度
                resistance = max(0.1, overcomed_energy / 3.0)      # 抵抗能力
                strength = attack_strength * (1.0 - resistance * 0.5)
                strength = max(0, min(1.0, strength))
                
                description = f"{self.element_names[overcomer]}克{self.element_names[overcomed]}"
                if strength > 0.7:
                    description += " (强克)"
                elif strength > 0.4:
                    description += " (中克)"
                else:
                    description += " (弱克)"
                
                relations.append(ElementRelation(
                    from_element=overcomer,
                    to_element=overcomed,
                    relation_type=RelationType.OVERCOME,
                    strength=strength,
                    description=description
                ))
        
        return relations
    
    def _detect_energy_breakpoints(self, energies: Dict[ElementType, float]) -> List[BreakpointEnergy]:
        """检测断点能量"""
        breakpoints = []
        
        # 按照相生循环顺序检查
        cycle_order = [ElementType.WOOD, ElementType.FIRE, ElementType.EARTH, 
                      ElementType.METAL, ElementType.WATER]
        
        for i, element in enumerate(cycle_order):
            energy = energies[element]
            
            # 检测缺失或过弱的五行
            if energy < 0.5:  # 能量阈值
                break_type = "缺失" if energy == 0 else "过弱"
                
                # 确定补救五行 (生我和我生的)
                remedy_elements = []
                
                # 找到生我的五行
                for gen, target in self.generation_cycle.items():
                    if target == element:
                        remedy_elements.append(gen)
                
                # 影响程度计算
                impact = self._calculate_breakpoint_impact(element, energies)
                
                breakpoints.append(BreakpointEnergy(
                    element=element,
                    position=i,
                    break_type=break_type,
                    impact_level=impact,
                    remedy_elements=remedy_elements
                ))
        
        # 检测受阻的五行 (被强克的情况)
        for element, energy in energies.items():
            if energy > 0:
                # 检查是否受到强克制
                total_overcome_strength = 0
                for overcomer, target in self.overcoming_cycle.items():
                    if target == element:
                        overcomer_energy = energies[overcomer]
                        if overcomer_energy > energy * 1.5:  # 克制者比被克者强很多
                            total_overcome_strength += overcomer_energy
                
                if total_overcome_strength > energy * 2:  # 受到强烈克制
                    impact = min(1.0, total_overcome_strength / (energy + 1))
                    breakpoints.append(BreakpointEnergy(
                        element=element,
                        position=cycle_order.index(element),
                        break_type="受阻",
                        impact_level=impact,
                        remedy_elements=[self.generation_cycle.get(gen, element) 
                                       for gen, target in self.generation_cycle.items() 
                                       if target == element]
                    ))
        
        return breakpoints
    
    def _calculate_breakpoint_impact(self, element: ElementType, energies: Dict[ElementType, float]) -> float:
        """计算断点能量的影响程度"""
        impact = 0.0
        
        # 检查对下一个五行的影响
        next_element = self.generation_cycle.get(element)
        if next_element and energies[next_element] < 1.0:
            impact += 0.4  # 无法充分生助下一五行
        
        # 检查是否是关键五行 (整体平衡的重要性)
        total_energy = sum(energies.values())
        if total_energy > 0:
            expected_ratio = 1.0 / 5  # 理想情况下每个五行占20%
            actual_ratio = energies[element] / total_energy
            imbalance = abs(expected_ratio - actual_ratio) / expected_ratio
            impact += imbalance * 0.6
        
        return min(1.0, impact)
    
    def _analyze_energy_flow(self, energies: Dict[ElementType, float]) -> Dict[str, Any]:
        """分析能量流动情况"""
        
        # 计算整体循环流畅度
        total_flow_strength = 0.0
        flow_details = []
        
        cycle_order = [ElementType.WOOD, ElementType.FIRE, ElementType.EARTH, 
                      ElementType.METAL, ElementType.WATER]
        
        for i, element in enumerate(cycle_order):
            next_element = cycle_order[(i + 1) % 5]
            current_energy = energies[element]
            next_energy = energies[next_element]
            
            # 计算流动强度
            if current_energy > 0:
                flow_strength = min(current_energy / 2.0, 1.0) * (1.0 + next_energy / 3.0)
            else:
                flow_strength = 0.0
            
            total_flow_strength += flow_strength
            
            flow_details.append({
                "from": self.element_names[element],
                "to": self.element_names[next_element],
                "strength": flow_strength,
                "description": f"{self.element_names[element]}→{self.element_names[next_element]}"
            })
        
        average_flow = total_flow_strength / 5.0
        
        # 分析流动质量
        flow_quality = "流畅"
        if average_flow < 0.3:
            flow_quality = "阻滞"
        elif average_flow < 0.6:
            flow_quality = "一般"
        elif average_flow > 0.8:
            flow_quality = "顺畅"
        
        return {
            "overall_flow_strength": average_flow,
            "flow_quality": flow_quality,
            "flow_details": flow_details,
            "circulation_health": self._assess_circulation_health(energies)
        }
    
    def _assess_circulation_health(self, energies: Dict[ElementType, float]) -> str:
        """评估循环健康度"""
        total = sum(energies.values())
        if total == 0:
            return "无循环"
        
        # 计算标准差 (衡量平衡度)
        mean = total / 5
        variance = sum((energy - mean) ** 2 for energy in energies.values()) / 5
        std_dev = variance ** 0.5
        
        # 根据标准差判断健康度
        if std_dev < mean * 0.3:
            return "非常平衡"
        elif std_dev < mean * 0.6:
            return "相对平衡"
        elif std_dev < mean * 1.0:
            return "轻度失衡"
        else:
            return "严重失衡"
    
    def _generate_relationship_graph(self, energies: Dict[ElementType, float], 
                                   relations: List[ElementRelation]) -> Dict[str, Any]:
        """生成关系图数据"""
        
        # 节点数据 (五行)
        nodes = []
        for element, energy in energies.items():
            nodes.append({
                "id": element.value,
                "name": self.element_names[element],
                "energy": energy,
                "size": max(20, energy * 30),  # 节点大小反映能量
                "color": self._get_element_color(element)
            })
        
        # 边数据 (关系)
        edges = []
        for relation in relations:
            edge_style = "solid" if relation.relation_type == RelationType.GENERATE else "dashed"
            edge_color = "#4ade80" if relation.relation_type == RelationType.GENERATE else "#f87171"
            
            edges.append({
                "from": relation.from_element.value,
                "to": relation.to_element.value,
                "type": relation.relation_type.value,
                "strength": relation.strength,
                "style": edge_style,
                "color": edge_color,
                "width": max(1, relation.strength * 5),
                "description": relation.description
            })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "layout": "circular"  # 建议使用圆形布局显示五行循环
        }
    
    def _get_element_color(self, element: ElementType) -> str:
        """获取五行颜色"""
        colors = {
            ElementType.WOOD: "#22c55e",   # 绿色
            ElementType.FIRE: "#ef4444",   # 红色  
            ElementType.EARTH: "#eab308",  # 黄色
            ElementType.METAL: "#9ca3af",  # 银灰色
            ElementType.WATER: "#3b82f6"   # 蓝色
        }
        return colors.get(element, "#6b7280")
    
    def _generate_summary(self, energies: Dict[ElementType, float], 
                         breakpoints: List[BreakpointEnergy], 
                         flow_analysis: Dict[str, Any]) -> str:
        """生成五行关系分析总结"""
        
        # 找出最强和最弱的五行
        strongest = max(energies.items(), key=lambda x: x[1])
        weakest = min(energies.items(), key=lambda x: x[1])
        
        summary_parts = []
        summary_parts.append(f"五行能量分布：{self.element_names[strongest[0]]}最旺({strongest[1]:.1f})，{self.element_names[weakest[0]]}最弱({weakest[1]:.1f})")
        
        # 循环状况
        flow_quality = flow_analysis["flow_quality"]
        circulation_health = flow_analysis["circulation_health"]
        summary_parts.append(f"循环状况：{flow_quality}，整体{circulation_health}")
        
        # 断点分析
        if breakpoints:
            breakpoint_elements = [self.element_names[bp.element] for bp in breakpoints[:2]]
            summary_parts.append(f"主要断点：{', '.join(breakpoint_elements)}")
        else:
            summary_parts.append("无明显断点")
        
        # 建议
        if weakest[1] < 0.5:
            remedy = []
            for gen, target in self.generation_cycle.items():
                if target == weakest[0]:
                    remedy.append(self.element_names[gen])
            if remedy:
                summary_parts.append(f"建议补强：{', '.join(remedy)}生{self.element_names[weakest[0]]}")
        
        return "；".join(summary_parts)
    
    def _relation_to_dict(self, relation: ElementRelation) -> Dict[str, Any]:
        """关系对象转字典"""
        return {
            "from_element": relation.from_element.value,
            "to_element": relation.to_element.value,
            "relation_type": relation.relation_type.value,
            "strength": relation.strength,
            "description": relation.description
        }
    
    def _breakpoint_to_dict(self, breakpoint: BreakpointEnergy) -> Dict[str, Any]:
        """断点对象转字典"""
        return {
            "element": breakpoint.element.value,
            "element_name": self.element_names[breakpoint.element],
            "position": breakpoint.position,
            "break_type": breakpoint.break_type,
            "impact_level": breakpoint.impact_level,
            "remedy_elements": [elem.value for elem in breakpoint.remedy_elements],
            "remedy_names": [self.element_names[elem] for elem in breakpoint.remedy_elements]
        }


# 主要接口函数
def analyze_wuxing_relations(bazi_analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """分析八字中的五行生克关系"""
    analyzer = WuxingRelationAnalyzer()
    return analyzer.analyze_element_relations(bazi_analysis_result)
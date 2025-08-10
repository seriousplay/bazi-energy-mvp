"""
八字命局自动判定与提示词生成模块 (MVP)
- 输入：interpretation dict (来自规则引擎)，应包含至少：
    - "五行分数": dict of element -> float  (e.g., {"wood":2.3,...})
    - "十神表": dict mapping labels -> 十神中文名 (e.g., {"柱1_天干_甲":"比肩", ...})
    - "bazi_raw": {"stems": [...], "branches":[...]}
    - 可选: "llm_summary" or "日干"
- 输出：
    - detect_jugotype(...) -> dict with primary types, counts, confidences
    - build_prompt(jugo_type, question, context) -> string prompt feedable to LLM

Notes:
- 判定启发式规则基于"能量易学 第一级.pdf" 中的病/药、格局与藏干逻辑（已编码为可执行逻辑）。请专家复核阈值。
- 来源：能量易学 第一级.pdf
"""

from collections import Counter, defaultdict
from typing import Dict, Any, List, Tuple

# 十神分组，用于计数
TEN_GOD_GROUPS = {
    "peer": {"比肩", "劫财"},              # 比肩/劫财 -> 同类（扶助/并列）
    "yin": {"正印", "偏印"},             # 印
    "cai": {"正财", "偏财"},             # 财
    "guan": {"正官", "七杀"},            # 官杀（煞）
    "shang": {"伤官", "食神"},           # 伤食
}

# 为每个命局准备关键词（LLM 提示使用）
JUJU_KEYWORDS = {
    "比肩旺": ["自主", "意志", "竞争", "独立", "坚韧", "同类聚集", "自我驱动", "资源防守"],
    "印重": ["学习", "依赖", "安全感", "保护", "积累", "体系", "守成", "延迟行动"],
    "财旺": ["成果", "目标", "获取", "外向驱动", "物质追求", "输出能量", "外部认可"],
    "煞重": ["规则", "纪律", "克制", "承压", "责任感", "社会框架", "自我约束"],
    "伤官旺": ["创造", "表达", "突破", "张扬", "反叛", "情绪释放", "个性化"],
    "从局": ["顺势", "借力", "环境融合", "适应", "放下自我", "趋利避害"],
    "无根局": ["灵活", "多变", "漂泊", "无拘束", "瞬变", "游走", "自发性"],
    "专旺格": ["极端旺盛", "压制其他", "主导", "强势", "能量集中"],
    "化气格": ["单一能量", "纯粹", "极致", "集中", "专注", "极端化倾向"],
    "半化/半合局": ["倾向性", "未稳定", "受影响", "转向", "局部合作"],
    "虚透格": ["表面倾向", "缺支撑", "空泛", "虚象", "意念多行动少"],
}

# 命局类型的通俗解释 - 让人一看就明白
JUJU_PLAIN_DESCRIPTIONS = {
    "比肩旺": {
        "核心特点": "天生不服输，喜欢掌控主动权",
        "性格表现": "您是那种'我的事情我做主'的人，不喜欢被人指挥，更愿意自己决定",
        "典型行为": "创业、独立工作、坚持己见、不轻易妥协",
        "鲜明标志": "💪 遇到困难不退缩，越挫越勇"
    },
    "印重": {
        "核心特点": "安全感需求强，喜欢有人指导和支持",
        "性格表现": "您是那种'三思而后行'的人，喜欢先学习研究透彻了再行动",
        "典型行为": "看重文凭资质、听专家建议、重视长辈意见、追求稳定",
        "鲜明标志": "🎓 终身学习者，智慧型的人"
    },
    "财旺": {
        "核心特点": "目标导向，善于把想法变成现实",
        "性格表现": "您是那种'想到就要做到'的人，不喜欢空谈，追求实际成果",
        "典型行为": "制定计划、追求效率、重视收益、关注结果",
        "鲜明标志": "🎯 执行力强，很有生意头脑"
    },
    "煞重": {
        "核心特点": "责任心强，在压力下反而能发挥更好",
        "性格表现": "您是那种'答应了就一定要做到'的人，有很强的自律性",
        "典型行为": "承担重任、严格要求、遵守规则、顶住压力",
        "鲜明标志": "⚡ 关键时刻能挺身而出的人"
    },
    "伤官旺": {
        "核心特点": "创意十足，不喜欢被条条框框限制",
        "性格表现": "您是那种'我有我的想法'的人，喜欢用自己的方式表达",
        "典型行为": "追求个性、创新突破、表达自我、不走寻常路",
        "鲜明标志": "🎨 天生的艺术家和创新者"
    },
    "从财": {
        "核心特点": "善于借力打力，懂得与环境合作共赢", 
        "性格表现": "您是那种'识时务者为俊杰'的人，善于顺势而为",
        "典型行为": "团队合作、资源整合、抓住机遇、灵活应变",
        "鲜明标志": "🤝 很会做人做事，人缘好"
    },
    "从杀": {
        "核心特点": "在规则和约束中反而能找到自己的位置",
        "性格表现": "您是那种'在纪律中获得自由'的人，适合有挑战的环境",
        "典型行为": "服从权威、承担挑战、严格执行、追求卓越",
        "鲜明标志": "🏆 在严格环境中更能出成绩"
    },
    "化气格": {
        "核心特点": "专注力强，容易在某个领域深度发展",
        "性格表现": "您是那种'专一专精'的人，一旦认定方向就会全力投入",
        "典型行为": "深度专研、专业精进、执着坚持、追求极致",
        "鲜明标志": "🔬 专家型人才，某方面特别突出"
    },
    "专旺格": {
        "核心特点": "某方面能力特别突出，但需要平衡发展",
        "性格表现": "您是那种'特色鲜明'的人，在某些方面很强但可能偏科",
        "典型行为": "发挥强项、展现个性、主导局面、影响他人",
        "鲜明标志": "⭐ 个性很强，容易成为焦点"
    },
    "无根局": {
        "核心特点": "灵活性强，但需要找到稳定的支撑",
        "性格表现": "您是那种'随机应变'的人，适应能力强但有时缺乏坚持",
        "典型行为": "随遇而安、适应环境、多才多艺、变化灵活",
        "鲜明标志": "🌊 像水一样灵活，但需要找到容器"
    },
    "虚透格": {
        "核心特点": "想法很多，但需要加强行动力",
        "性格表现": "您是那种'理想主义者'，有很多想法但执行上可能欠缺",
        "典型行为": "头脑灵活、点子多、计划性强、但执行偏弱",
        "鲜明标志": "💭 思维活跃，需要更多实际行动"
    }
}

# 判定阈值（可调）
THRESH = {
    "group_count_major": 2,        # 单一十神组出现 >=2 次，认为该组显著
    "group_count_dominate": 3,     # 出现 >=3，认为非常显著（可能从局）
    "day_elem_weak_ratio": 0.8,    # 日主元素分数 < avg * ratio -> 认为弱
    "dominant_elem_ratio": 0.6,    # 某元素分数 / total >= threshold -> 专旺/化气候选
    "dominant_elem_extreme": 0.8,  # >=0.8 -> 化气格（极端）
}

# mapping from juju name to human label (optional)
JUJU_LABELS = {
    "peer": "比肩旺",
    "yin": "印重",
    "cai": "财旺",
    "guan": "煞重",
    "shang": "伤官旺",
}


def _count_ten_gods(ten_dict: Dict[str, str]) -> Counter:
    """
    ten_dict: mapping like {"柱1_天干_甲":"比肩", ...}
    returns Counter of ten-god Chinese names
    """
    cnt = Counter()
    for k, v in (ten_dict or {}).items():
        if not v:
            continue
        cnt[v] += 1
    return cnt


def _group_counts_from_ten(counter: Counter) -> Dict[str, int]:
    groups = {}
    for gname, members in TEN_GOD_GROUPS.items():
        groups[gname] = sum(counter.get(x, 0) for x in members)
    return groups


def detect_jugotype(interp: Dict[str, Any]) -> Dict[str, Any]:
    """
    自动判定命局类型（启发式）
    Input: interp dict from bazi engine (must contain "十神表" and "五行分数")
    Output: dict containing:
      - primary: list of primary detected types (strings)
      - details: raw counts and heuristics used
    """
    ten_table = interp.get("十神表") or interp.get("ten_gods") or {}
    scores = interp.get("五行分数") or interp.get("five_elements_scores") or {}
    stems = interp.get("bazi_raw", {}).get("stems", [])
    branches = interp.get("bazi_raw", {}).get("branches", [])

    ten_counter = _count_ten_gods(ten_table)
    group_counts = _group_counts_from_ten(ten_counter)

    # compute simple five-element totals and day element
    total_score = sum(scores.get(e, 0.0) for e in scores) or 1.0
    # day_gan: try to pick 日干 if present
    day_gan = None
    daily = None
    if "bazi_raw" in interp:
        stems_list = interp["bazi_raw"].get("stems", [])
        if len(stems_list) >= 3:
            day_gan = stems_list[2]
    # day element by mapping if available in interp
    # fallback: try interpret '日干' key
    if not day_gan:
        day_gan = interp.get("日干") or interp.get("day_gan")

    # Attempt to derive day element string (wood/fire/earth/metal/water)
    # The caller should map tian_gan -> element before calling if needed.
    # Here we try to read if interp includes 'day_element'
    day_elem = interp.get("day_element")
    avg = (total_score / 5.0) if total_score else 0.0

    results = {
        "primary": [],
        "candidates": [],
        "details": {
            "ten_counter": dict(ten_counter),
            "group_counts": group_counts,
            "scores": scores,
            "total_score": total_score,
            "avg_elem_score": avg,
            "day_gan": day_gan,
            "day_elem": day_elem,
        }
    }

    # 1) direct group detections (比肩/印/财/煞/伤)
    for grp_key, label in JUJU_LABELS.items():
        cnt = group_counts.get(grp_key, 0)
        if cnt >= THRESH["group_count_major"]:
            results["primary"].append(label)
            results["candidates"].append({"type": label, "count": cnt, "reason": "group_major"})
        elif cnt > 0:
            results["candidates"].append({"type": label, "count": cnt, "reason": "group_minor"})

    # 2) 从局检测：若某组数量非常大且日主相对弱 -> 从局（归于相应类，比如从财/从杀/从印/从儿）
    for grp_key, members in TEN_GOD_GROUPS.items():
        cnt = group_counts.get(grp_key, 0)
        # group dominates strongly -> candidate for 从局
        if cnt >= THRESH["group_count_dominate"]:
            # check day element weakness
            day_elem_score = None
            if day_elem and day_elem in scores:
                day_elem_score = scores.get(day_elem, 0.0)
            else:
                # fallback: if day_gan provided but not mapped to element, skip this check
                day_elem_score = None
            weak_flag = False
            if day_elem_score is not None:
                weak_flag = day_elem_score < (avg * THRESH["day_elem_weak_ratio"])
            # if day elem unknown, be conservative and require higher cnt
            if weak_flag or cnt >= (THRESH["group_count_dominate"] + 1):
                # determine which from-jv type
                from_label = None
                if grp_key == "cai":
                    from_label = "从财"
                elif grp_key == "guan":
                    from_label = "从杀"
                elif grp_key == "yin":
                    from_label = "从印"
                elif grp_key == "shang":
                    from_label = "从儿"  # 从食伤
                else:
                    from_label = f"从_{grp_key}"
                results["primary"].append(from_label)
                results["candidates"].append({"type": from_label, "count": cnt, "reason": "from_dominant"})

    # 3) 无根局检测：日主在盘中无根（五行分数低且无比肩/印）
    day_elem_score = None
    if day_elem and day_elem in scores:
        day_elem_score = scores.get(day_elem)
    # condition: day_elem_score low AND counts of peer+yin both small
    peer_yin_count = group_counts.get("peer", 0) + group_counts.get("yin", 0)
    if day_elem_score is not None:
        if day_elem_score < (avg * THRESH["day_elem_weak_ratio"]) and peer_yin_count <= 1:
            results["primary"].append("无根局")
            results["candidates"].append({"type": "无根局", "day_elem_score": day_elem_score, "peer_yin": peer_yin_count})

    # 4) 专旺 / 化气 / 半化 等基于五行偏势的判断
    # find dominant element
    if scores:
        dominant_elem, dominant_val = max(scores.items(), key=lambda kv: kv[1])
        dominant_ratio = dominant_val / total_score if total_score else 0.0
        if dominant_ratio >= THRESH["dominant_elem_extreme"]:
            results["primary"].append("化气格")
            results["candidates"].append({"type": "化气格", "dominant": dominant_elem, "ratio": dominant_ratio})
        elif dominant_ratio >= THRESH["dominant_elem_ratio"]:
            results["primary"].append("专旺格")
            results["candidates"].append({"type": "专旺格", "dominant": dominant_elem, "ratio": dominant_ratio})
        else:
            # 半化/半合判定 - heuristic:
            # If any element has two occurrences in branches (i.e., appears in 2+ 藏干 or多天干), treat as 半化倾向
            branch_elems = []
            # try to infer elements present from stems/branches dictionary if provided
            # interp may include mapping; caller can augment
            # we conservatively check: if any element's value > avg*1.2, consider 半化/倾向
            for e, val in scores.items():
                if val > avg * 1.2:
                    results["candidates"].append({"type": "半化/半合局", "element": e, "value": val})
    # 5) 虚透格（透干无根） heuristic:
    # if stems have a clear '透' (i.e., a天干的某五行分数显著，但 day_elem 无根) -> 虚透格
    # simple heuristic: if dominant_val > avg*1.3 but day_elem weak and peer_yin_count==0
    if scores:
        dominant_elem, dominant_val = max(scores.items(), key=lambda kv: kv[1])
        dominant_ratio = dominant_val / total_score
        if dominant_ratio > 0.5 and ("无根局" in results["primary"] or peer_yin_count == 0):
            results["candidates"].append({"type": "虚透格", "dominant": dominant_elem, "ratio": dominant_ratio})

    # deduplicate primary
    results["primary"] = list(dict.fromkeys(results["primary"]))
    
    # 添加通俗解释
    results["plain_descriptions"] = {}
    for juju_type in results["primary"]:
        if juju_type in JUJU_PLAIN_DESCRIPTIONS:
            results["plain_descriptions"][juju_type] = JUJU_PLAIN_DESCRIPTIONS[juju_type]
    
    return results


def build_prompt(jugo_type: str, question: str = "", extra_context: str = "", juju_keywords: Dict[str, List[str]] = None) -> str:
    """
    根据命局类型生成 LLM 提示词（中文）。
    juju_keywords: optional mapping override; otherwise use JUJU_KEYWORDS
    """
    keywords = (juju_keywords or JUJU_KEYWORDS).get(jugo_type, [])
    kw_line = "，".join(keywords)
    prompt = f"""你是一位擅长结合八字命理与意识能量学的分析师。
命局类型：{jugo_type}
问题：{question or '（未提供）'}
请按下列要求生成回答：
1) 用生动、贴近觉知的语言描述该命局的意识能量特征（3-5句），结合关键词：{kw_line}。
2) 针对该问题，说明该命局在决策时的优势（1-2句）与潜在挑战（1-2句）。
3) 给出一条简明、可执行且鼓舞人心的行动建议（1句，尽量具体）。
4) 在末尾括注一行"判定依据"，简单写出触发该判定的主要线索（例如："依据：盘中伤官3次，日主弱，属于伤官旺"）。
注意：避免使用医学或法律断言，仅提供能量/意识层面的建议。
{extra_context or ''}"""
    return prompt


# --------------------
# 简单示例 / 单元测试样例（可用 pytest 运行）
# --------------------
if __name__ == "__main__":
    # 例子：模拟规则引擎输出
    interp_example = {
        "十神表": {
            "柱1_天干_甲": "比肩",
            "柱1_地支_寅_主": "比肩",
            "柱2_天干_乙": "劫财",
            "柱3_天干_丙": "食神",
            "柱4_天干_丁": "伤官",
        },
        "五行分数": {"wood": 3.0, "fire": 1.0, "earth": 0.5, "metal": 0.2, "water": 0.3},
        "bazi_raw": {"stems": ["甲", "乙", "丙", "丁"], "branches": ["子","丑","寅","巳"]},
        "day_element": "wood",
    }
    det = detect_jugotype(interp_example)
    print("detect:", det)
    print("prompt example:\n", build_prompt("比肩旺", "我适合创业吗？"))
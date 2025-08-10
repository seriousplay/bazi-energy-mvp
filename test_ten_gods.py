import pytest
from bazi_engine_d1d2 import determine_ten_god, interpret_bazi

class TestTenGods:
    """测试十神判定逻辑"""
    
    def test_same_element_same_yin_yang(self):
        """测试同五行同阴阳 - 比肩"""
        assert determine_ten_god("甲", "甲") == "比肩"
        assert determine_ten_god("乙", "乙") == "比肩"
        assert determine_ten_god("丙", "丙") == "比肩"
        
    def test_same_element_diff_yin_yang(self):
        """测试同五行不同阴阳 - 劫财"""
        assert determine_ten_god("甲", "乙") == "劫财"
        assert determine_ten_god("乙", "甲") == "劫财"
        assert determine_ten_god("丙", "丁") == "劫财"
        
    def test_zheng_yin(self):
        """测试正印 - 异性相生"""
        assert determine_ten_god("甲", "癸") == "正印"  # 水生木
        assert determine_ten_god("丙", "乙") == "正印"  # 木生火
        assert determine_ten_god("戊", "丁") == "正印"  # 火生土
        
    def test_pian_yin(self):
        """测试偏印 - 同性相生"""
        assert determine_ten_god("甲", "壬") == "偏印"  # 水生木
        assert determine_ten_god("丙", "甲") == "偏印"  # 木生火
        assert determine_ten_god("戊", "丙") == "偏印"  # 火生土
        
    def test_zheng_guan(self):
        """测试正官 - 异性相克"""
        assert determine_ten_god("甲", "辛") == "正官"  # 金克木
        assert determine_ten_god("丙", "癸") == "正官"  # 水克火
        assert determine_ten_god("戊", "乙") == "正官"  # 木克土
        
    def test_qi_sha(self):
        """测试七杀 - 同性相克"""
        assert determine_ten_god("甲", "庚") == "七杀"  # 金克木
        assert determine_ten_god("丙", "壬") == "七杀"  # 水克火
        assert determine_ten_god("戊", "甲") == "七杀"  # 木克土
        
    def test_zheng_cai(self):
        """测试正财 - 异性被克"""
        assert determine_ten_god("甲", "己") == "正财"  # 木克土
        assert determine_ten_god("丙", "辛") == "正财"  # 火克金
        assert determine_ten_god("戊", "癸") == "正财"  # 土克水
        
    def test_pian_cai(self):
        """测试偏财 - 同性被克"""
        assert determine_ten_god("甲", "戊") == "偏财"  # 木克土
        assert determine_ten_god("丙", "庚") == "偏财"  # 火克金
        assert determine_ten_god("戊", "壬") == "偏财"  # 土克水
        
    def test_shi_shen(self):
        """测试食神 - 同性我生"""
        assert determine_ten_god("甲", "丙") == "食神"  # 木生火
        assert determine_ten_god("丙", "戊") == "食神"  # 火生土
        assert determine_ten_god("戊", "庚") == "食神"  # 土生金
        
    def test_shang_guan(self):
        """测试伤官 - 异性我生"""
        assert determine_ten_god("甲", "丁") == "伤官"  # 木生火
        assert determine_ten_god("丙", "己") == "伤官"  # 火生土
        assert determine_ten_god("戊", "辛") == "伤官"  # 土生金

class TestBaziInterpretation:
    """测试八字解读功能"""
    
    def test_valid_bazi_input(self):
        """测试有效的八字输入"""
        result = interpret_bazi("甲子 乙丑 丙寅 丁巳")
        
        assert "八字信息" in result
        assert "日主分析" in result
        assert "十神关系" in result
        assert "五行统计" in result
        assert "能量分析" in result
        assert "基础解读" in result
        
        # 检查具体内容
        assert result["日主分析"]["日干"] == "丙"
        assert result["日主分析"]["五行"] == "fire"
        assert result["八字信息"]["年柱"] == "甲子"
        
    def test_invalid_bazi_format(self):
        """测试无效的八字格式"""
        with pytest.raises(ValueError, match="八字格式错误"):
            interpret_bazi("甲子 乙丑 丙寅")  # 只有三柱
            
        with pytest.raises(ValueError, match="八字格式错误"):
            interpret_bazi("甲子 乙丑 丙寅 丁巳 戊午")  # 五柱
            
    def test_invalid_gan_zhi(self):
        """测试无效的天干地支"""
        with pytest.raises(ValueError, match="无效的天干"):
            interpret_bazi("甲子 乙丑 X寅 丁巳")  # 无效天干
            
        with pytest.raises(ValueError, match="无效的地支"):
            interpret_bazi("甲子 乙丑 丙Y 丁巳")  # 无效地支
            
    def test_question_specific_interpretation(self):
        """测试针对特定问题的解读"""
        result = interpret_bazi("甲子 己卯 丙寅 戊戌", "我适合创业吗？")
        
        interpretation = result["基础解读"]
        # 这个八字中有财星（月干己土，时干戊土），应该包含创业相关的建议
        assert "创业" in interpretation or "财" in interpretation
        
    def test_element_counting(self):
        """测试五行统计功能"""
        result = interpret_bazi("甲子 乙丑 丙寅 丁巳")
        element_count = result["五行统计"]
        
        # 验证五行统计是否合理
        assert all(elem in element_count for elem in ["wood", "fire", "earth", "metal", "water"])
        assert all(count >= 0 for count in element_count.values())
        
    def test_ten_gods_analysis(self):
        """测试十神关系分析"""
        result = interpret_bazi("甲子 乙丑 丙寅 丁巳")
        ten_gods = result["十神关系"]
        
        assert "年干" in ten_gods
        assert "月干" in ten_gods  
        assert "时干" in ten_gods
        
        # 验证十神关系的准确性
        assert ten_gods["年干"] == determine_ten_god("丙", "甲")
        assert ten_gods["月干"] == determine_ten_god("丙", "乙")
        assert ten_gods["时干"] == determine_ten_god("丙", "丁")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

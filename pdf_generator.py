"""
PDF Generator for Bazi Analysis Reports
八字分析报告PDF生成器
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfutils
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from typing import Dict, Any, List
from datetime import datetime
import io

class BaziPDFGenerator:
    """八字分析PDF生成器"""
    
    def __init__(self):
        self.setup_fonts()
        self.setup_styles()
    
    def setup_fonts(self):
        """设置中文字体"""
        try:
            # 尝试使用系统中文字体
            font_paths = [
                "/System/Library/Fonts/Helvetica.ttc",  # macOS基础字体
                "/System/Library/Fonts/Arial.ttf",  # macOS备用
                "C:\\Windows\\Fonts\\arial.ttf",  # Windows
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            ]
            
            self.has_chinese_font = False
            # 先使用基础字体，避免中文编码问题
            try:
                pdfmetrics.registerFont(TTFont('CustomFont', font_paths[0] if os.path.exists(font_paths[0]) else None))
                self.has_chinese_font = True
            except:
                # 如果都失败，使用默认字体
                self.has_chinese_font = False
                
        except Exception as e:
            self.has_chinese_font = False
            print(f"Font setup warning: {e}")
    
    def safe_text(self, text: str) -> str:
        """安全处理文本，避免编码问题 - 简化版本，移除所有非ASCII字符"""
        if not text:
            return ""
        
        # 简单粗暴的方式：只保留ASCII字符，移除其他所有字符
        try:
            # 尝试编码到latin-1，如果失败则过滤
            return text.encode('latin-1', 'ignore').decode('latin-1')
        except Exception:
            # 备选方案：只保留ASCII字符
            return ''.join(char for char in text if ord(char) < 128)
    
    def setup_styles(self):
        """设置样式"""
        styles = getSampleStyleSheet()
        
        # 使用安全字体
        font_name = 'CustomFont' if self.has_chinese_font else 'Helvetica'
        
        # 标题样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=font_name,
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # 居中
            textColor=colors.HexColor('#2E86AB')
        )
        
        # 章节标题
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontName=font_name,
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#A23B72')
        )
        
        # 正文样式
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=12,
            spaceAfter=6,
            leftIndent=0,
            rightIndent=0
        )
        
        # 强调样式
        self.emphasis_style = ParagraphStyle(
            'CustomEmphasis',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=colors.HexColor('#F18F01'),
            leftIndent=20
        )
    
    def create_bazi_table(self, bazi_data: Dict[str, str]) -> Table:
        """创建八字表格"""
        data = [
            ['Year', 'Month', 'Day', 'Hour'],
            [
                bazi_data['year'], 
                bazi_data['month'], 
                bazi_data['day'], 
                bazi_data['hour']
            ]
        ]
        
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F4FD')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC'))
        ]))
        
        return table
    
    def create_personal_info_table(self, personal_info: Dict[str, Any]) -> Table:
        """创建个人信息表格（传统格式）"""
        # 性别转换：男->乾，女->坤
        gender_map = {'male': '乾 (Male)', 'female': '坤 (Female)', '男': '乾 (Male)', '女': '坤 (Female)'}
        gender_display = gender_map.get(personal_info.get('gender', ''), personal_info.get('gender', ''))
        
        data = [
            ['Name', 'Birth Date', 'Gender', 'Location', 'Current Age'],
            [
                personal_info.get('name', ''),
                f"{personal_info.get('year', '')}年{personal_info.get('month', '')}月{personal_info.get('day', '')}日{personal_info.get('hour', '')}时",
                gender_display,
                personal_info.get('location', ''),
                f"{personal_info.get('current_age', '')} years old"
            ]
        ]
        
        table = Table(data, colWidths=[1.2*inch, 2*inch, 1*inch, 1.2*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F4FD')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        return table
    
    def create_wuxing_table(self, wuxing_data: Dict[str, Any]) -> Table:
        """创建五行统计表格"""
        elements = ['wood', 'fire', 'earth', 'metal', 'water']
        element_names = {'wood': 'Wood', 'fire': 'Fire', 'earth': 'Earth', 'metal': 'Metal', 'water': 'Water'}
        
        data = [['Element', 'Wood', 'Fire', 'Earth', 'Metal', 'Water']]
        scores = ['Score']
        
        for element in elements:
            score = wuxing_data.get(element, 0)
            scores.append(f"{score:.1f}")
        
        data.append(scores)
        
        # 添加最旺最弱行
        strongest = wuxing_data.get('最旺', '')
        weakest = wuxing_data.get('最弱', '')
        status_row = ['Status']
        
        for element in elements:
            if element == strongest:
                status_row.append('Strongest')
            elif element == weakest:
                status_row.append('Weakest')
            else:
                status_row.append('-')
        
        data.append(status_row)
        
        table = Table(data, colWidths=[1*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F4FD')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#FFF2E8'))
        ]))
        
        return table
    
    def create_bingyao_table(self, bingyao_data: List[Dict[str, Any]]) -> Table:
        """创建病药分级表格"""
        data = [['Level', 'Element', 'Present', 'Strength', 'Consciousness']]
        
        for item in bingyao_data:
            data.append([
                item.get('level', ''),
                item.get('element_cn', ''),
                item.get('has', ''),
                item.get('prosperity', ''),
                item.get('consciousness', '')
            ])
        
        table = Table(data, colWidths=[0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F4FD')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        return table
    
    def sanitize_data(self, data):
        """递归处理数据，将所有中文字符转为安全字符"""
        if isinstance(data, dict):
            return {key: self.sanitize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_data(item) for item in data]
        elif isinstance(data, str):
            return self.safe_text(data)
        else:
            return data
    
    def generate_report(
        self, 
        structured_result: Dict[str, Any], 
        interpretation: Dict[str, str],
        output_path: str = None
    ) -> bytes:
        """生成完整的分析报告PDF"""
        
        # 预处理所有数据，确保没有中文字符
        structured_result = self.sanitize_data(structured_result)
        interpretation = self.sanitize_data(interpretation)
        
        # 创建PDF文档
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=72, 
            leftMargin=72,
            topMargin=72, 
            bottomMargin=18
        )
        
        # 构建内容
        story = []
        
        # 标题
        title = Paragraph("Bazi Energy Analysis Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # 生成时间
        generate_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        time_para = Paragraph(f"Generated: {generate_time}", self.body_style)
        story.append(time_para)
        story.append(Spacer(1, 20))
        
        # 个人基本信息表格（传统格式）
        if structured_result.get('个人信息'):
            story.append(Paragraph("Personal Information", self.heading_style))
            personal_info_table = self.create_personal_info_table(structured_result['个人信息'])
            story.append(personal_info_table)
            story.append(Spacer(1, 20))
        
        # 八字基本信息
        story.append(Paragraph("Bazi Chart Information", self.heading_style))
        bazi_table = self.create_bazi_table(structured_result['bazi'])
        story.append(bazi_table)
        story.append(Spacer(1, 15))
        
        # 用户问题
        if structured_result.get('问题'):
            story.append(Paragraph("Question", self.heading_style))
            question_text = structured_result['问题']
            question_para = Paragraph(f'"{question_text}"', self.body_style)
            story.append(question_para)
            story.append(Spacer(1, 15))
        
        # 能量画像
        story.append(Paragraph("Energy Portrait", self.heading_style))
        portrait_text = interpretation.get('energy_portrait', '')
        portrait_para = Paragraph(portrait_text, self.body_style)
        story.append(portrait_para)
        story.append(Spacer(1, 15))
        
        # 五行统计
        story.append(Paragraph("Five Elements Analysis", self.heading_style))
        wuxing_table = self.create_wuxing_table(structured_result['五行统计'])
        story.append(wuxing_table)
        story.append(Spacer(1, 15))
        
        # 格局分析
        story.append(Paragraph("Pattern Analysis", self.heading_style))
        geju = structured_result['定格局']
        geju_content = f"""
        <b>Pattern Type:</b> {geju['格局类型']}<br/>
        <b>Strength:</b> {geju['强弱']}<br/>
        <b>Root Status:</b> {geju['根']}<br/>
        <b>Support/Suppress:</b> {geju['扶抑关系']}
        """
        story.append(Paragraph(geju_content, self.body_style))
        story.append(Spacer(1, 15))
        
        # 寒燥分析
        story.append(Paragraph("Cold/Hot Analysis", self.heading_style))
        hanzao = structured_result['定寒燥']
        medicine_order = ' > '.join(hanzao['调候药效顺序']) if hanzao['调候药效顺序'] else 'None'
        hanzao_content = f"""
        <b>Type:</b> {hanzao['类型']}<br/>
        <b>Reason:</b> {hanzao['原因']}<br/>
        <b>Regulation Need:</b> {hanzao['需要调候']}<br/>
        <b>Medicine Order:</b> {medicine_order}
        """
        story.append(Paragraph(hanzao_content, self.body_style))
        story.append(Spacer(1, 15))
        
        # 病药分级
        story.append(Paragraph("Medicine Classification", self.heading_style))
        bingyao_table = self.create_bingyao_table(structured_result['定病药']['分级'])
        story.append(bingyao_table)
        story.append(Spacer(1, 15))
        
        # 大运分析
        story.append(Paragraph("Luck Period Analysis", self.heading_style))
        dayun = structured_result['看大运']
        current_dayun = dayun['当前大运']
        dayun_content = f"""
        <b>Current Period:</b> {current_dayun['age_range']} years<br/>
        <b>Period Stems:</b> {current_dayun['gan']}{current_dayun['zhi']}<br/>
        <b>Influence:</b> {current_dayun['influence']}
        """
        story.append(Paragraph(dayun_content, self.body_style))
        story.append(Spacer(1, 15))
        
        # 问题回答
        if interpretation.get('question_answer'):
            story.append(Paragraph("Targeted Suggestions", self.heading_style))
            # 处理换行和格式
            answer_text = interpretation['question_answer'].replace('\n', '<br/>')
            answer_para = Paragraph(answer_text, self.body_style)
            story.append(answer_para)
            story.append(Spacer(1, 15))
        
        # 调候建议
        if interpretation.get('practice_suggestions'):
            story.append(Paragraph("Practice Suggestions", self.heading_style))
            suggestions_text = interpretation['practice_suggestions'].replace('\n', '<br/>')
            suggestions_para = Paragraph(suggestions_text, self.body_style)
            story.append(suggestions_para)
            story.append(Spacer(1, 15))
        
        # 专家分析（如果有）
        if interpretation.get('expert_analysis'):
            story.append(PageBreak())
            story.append(Paragraph("Expert Analysis Details", self.heading_style))
            expert_text = interpretation['expert_analysis'].replace('\n', '<br/>')
            expert_para = Paragraph(expert_text, self.body_style)
            story.append(expert_para)
            story.append(Spacer(1, 15))
        
        # 免责声明
        story.append(Spacer(1, 30))
        disclaimer_text = interpretation.get('disclaimer', '')
        disclaimer_para = Paragraph(disclaimer_text, self.emphasis_style)
        story.append(disclaimer_para)
        
        # 构建PDF
        doc.build(story)
        
        # 获取PDF数据
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # 如果指定了输出路径，保存文件
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(pdf_data)
        
        return pdf_data

def generate_bazi_pdf(
    structured_result: Dict[str, Any], 
    interpretation: Dict[str, str],
    output_path: str = None
) -> bytes:
    """生成八字分析PDF报告"""
    generator = BaziPDFGenerator()
    return generator.generate_report(structured_result, interpretation, output_path)
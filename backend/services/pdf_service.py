import os
import json
from typing import List, Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PDFService:
    """PDF生成服务"""
    
    def __init__(self):
        self.setup_fonts()
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_fonts(self):
        """设置中文字体"""
        try:
            # 尝试注册中文字体
            font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'SimHei.ttf')
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('SimHei', font_path))
                self.chinese_font = 'SimHei'
            else:
                # 如果没有中文字体文件，使用默认字体
                self.chinese_font = 'Helvetica'
                logger.warning("未找到中文字体文件，使用默认字体")
        except Exception as e:
            self.chinese_font = 'Helvetica'
            logger.warning(f"字体设置失败: {e}")
    
    def setup_custom_styles(self):
        """设置自定义样式"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontName=self.chinese_font,
            fontSize=18,
            spaceAfter=30,
            alignment=1  # 居中
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontName=self.chinese_font,
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontName=self.chinese_font,
            fontSize=12,
            spaceAfter=6
        )
        
        self.question_style = ParagraphStyle(
            'QuestionStyle',
            parent=self.styles['Normal'],
            fontName=self.chinese_font,
            fontSize=12,
            spaceAfter=10,
            leftIndent=20
        )
    
    def generate_exercise_pdf(self, exercise_data: Dict[str, Any], 
                            output_path: str, include_answers: bool = False) -> str:
        """生成练习题PDF"""
        
        try:
            # 创建PDF文档
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # 构建PDF内容
            story = []
            
            # 标题
            title = f"{exercise_data.get('subject', '练习')} - {exercise_data.get('title', '练习题目')}"
            story.append(Paragraph(title, self.title_style))
            story.append(Spacer(1, 12))
            
            # 基本信息
            info_data = [
                ['题目数量:', f"{exercise_data.get('question_count', 0)}题"],
                ['题目类型:', self._get_type_display(exercise_data.get('question_type', ''))],
                ['难度等级:', self._get_difficulty_display(exercise_data.get('difficulty_level', 1))],
                ['生成时间:', datetime.now().strftime('%Y-%m-%d %H:%M')]
            ]
            
            info_table = Table(info_data, colWidths=[2*inch, 3*inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), self.chinese_font),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey)
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 20))
            
            # 题目内容
            questions = exercise_data.get('generated_content', {}).get('questions', [])
            
            for i, question in enumerate(questions, 1):
                # 题目标题
                story.append(Paragraph(f"第{i}题:", self.heading_style))
                
                # 题目内容
                content = question.get('content', '')
                story.append(Paragraph(content, self.question_style))
                
                # 选择题选项
                if question.get('type') == 'choice' and question.get('options'):
                    for option in question['options']:
                        story.append(Paragraph(f"　　{option}", self.normal_style))
                
                # 如果包含答案
                if include_answers:
                    story.append(Spacer(1, 6))
                    answer = question.get('answer', '暂无答案')
                    story.append(Paragraph(f"<b>答案:</b> {answer}", self.normal_style))
                    
                    # 知识点
                    knowledge_point = question.get('knowledge_point', '')
                    if knowledge_point:
                        story.append(Paragraph(f"<b>知识点:</b> {knowledge_point}", self.normal_style))
                
                story.append(Spacer(1, 15))
            
            # 如果没有答案，添加答题区域
            if not include_answers:
                story.append(Paragraph("答题区域", self.heading_style))
                story.append(Spacer(1, 10))
                
                for i in range(len(questions)):
                    story.append(Paragraph(f"第{i+1}题答案: ________________________", self.normal_style))
                    story.append(Spacer(1, 8))
            
            # 生成PDF
            doc.build(story)
            
            logger.info(f"PDF生成成功: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"PDF生成失败: {e}")
            raise Exception(f"PDF生成失败: {str(e)}")
    
    def generate_answer_pdf(self, exercise_data: Dict[str, Any], 
                          analysis_data: Dict[str, Any], output_path: str) -> str:
        """生成答案解析PDF"""
        
        try:
            # 创建PDF文档
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            story = []
            
            # 标题
            title = f"{exercise_data.get('subject', '练习')} - 答案解析"
            story.append(Paragraph(title, self.title_style))
            story.append(Spacer(1, 12))
            
            # 解析内容
            analyses = analysis_data.get('analyses', [])
            questions = exercise_data.get('generated_content', {}).get('questions', [])
            
            for i, (question, analysis) in enumerate(zip(questions, analyses), 1):
                # 题目
                story.append(Paragraph(f"第{i}题:", self.heading_style))
                story.append(Paragraph(question.get('content', ''), self.question_style))
                
                # 选择题选项
                if question.get('options'):
                    for option in question['options']:
                        story.append(Paragraph(f"　　{option}", self.normal_style))
                
                story.append(Spacer(1, 10))
                
                # 答案
                answer = analysis.get('answer', '暂无答案')
                story.append(Paragraph(f"<b>标准答案:</b> {answer}", self.normal_style))
                
                # 解题步骤
                steps = analysis.get('steps', [])
                if steps:
                    story.append(Paragraph("<b>解题步骤:</b>", self.normal_style))
                    for j, step in enumerate(steps, 1):
                        story.append(Paragraph(f"{j}. {step}", self.normal_style))
                
                # 知识点
                knowledge_points = analysis.get('knowledge_points', [])
                if knowledge_points:
                    story.append(Paragraph(f"<b>涉及知识点:</b> {', '.join(knowledge_points)}", self.normal_style))
                
                # 易错点
                mistakes = analysis.get('common_mistakes', [])
                if mistakes:
                    story.append(Paragraph("<b>易错点提醒:</b>", self.normal_style))
                    for mistake in mistakes:
                        story.append(Paragraph(f"• {mistake}", self.normal_style))
                
                # 解题技巧
                tips = analysis.get('tips', '')
                if tips:
                    story.append(Paragraph(f"<b>解题技巧:</b> {tips}", self.normal_style))
                
                story.append(Spacer(1, 20))
            
            # 生成PDF
            doc.build(story)
            
            logger.info(f"答案解析PDF生成成功: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"答案解析PDF生成失败: {e}")
            raise Exception(f"答案解析PDF生成失败: {str(e)}")
    
    def _get_type_display(self, question_type: str) -> str:
        """获取题目类型显示名称"""
        type_map = {
            'choice': '选择题',
            'fill': '填空题',
            'solve': '解答题',
            'mixed': '混合题型'
        }
        return type_map.get(question_type, question_type)
    
    def _get_difficulty_display(self, difficulty_level: int) -> str:
        """获取难度等级显示名称"""
        difficulty_map = {
            1: '基础',
            2: '简单',
            3: '中等',
            4: '困难',
            5: '挑战'
        }
        return difficulty_map.get(difficulty_level, '中等')


# PDF服务管理器
class PDFServiceManager:
    """PDF服务管理器"""
    
    @staticmethod
    def ensure_pdf_directory():
        """确保PDF输出目录存在"""
        pdf_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        return pdf_dir
    
    @staticmethod
    def get_pdf_path(exercise_id: int, pdf_type: str = 'exercise') -> str:
        """获取PDF文件路径"""
        pdf_dir = PDFServiceManager.ensure_pdf_directory()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{pdf_type}_{exercise_id}_{timestamp}.pdf"
        return os.path.join(pdf_dir, filename)
    
    @staticmethod
    def cleanup_old_pdfs(days: int = 7):
        """清理旧的PDF文件"""
        try:
            pdf_dir = PDFServiceManager.ensure_pdf_directory()
            current_time = datetime.now()
            
            for filename in os.listdir(pdf_dir):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(pdf_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    
                    if (current_time - file_time).days > days:
                        os.remove(file_path)
                        logger.info(f"已删除过期PDF文件: {filename}")
                        
        except Exception as e:
            logger.error(f"清理PDF文件失败: {e}")
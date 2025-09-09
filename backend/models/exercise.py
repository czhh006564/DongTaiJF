# 练习题目和错题记录相关数据模型
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class ErrorRecord(Base):
    __tablename__ = "error_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 错题信息
    subject = Column(String(50), nullable=False)  # 学科
    grade = Column(String(20), nullable=False)    # 年级
    chapter = Column(String(100))                 # 章节
    knowledge_point = Column(String(200), nullable=False)  # 知识点
    
    # 题目内容
    question_text = Column(Text, nullable=False)  # 题目文本
    question_image = Column(String(255))          # 题目图片URL
    correct_answer = Column(Text, nullable=False) # 正确答案
    student_answer = Column(Text, nullable=False) # 学生答案
    
    # 分析信息
    error_type = Column(String(100))              # 错误类型
    difficulty_level = Column(Integer, default=1) # 难度等级 1-5
    ai_analysis = Column(Text)                    # AI分析结果
    
    # 状态信息
    is_resolved = Column(Boolean, default=False)  # 是否已解决
    practice_count = Column(Integer, default=0)   # 练习次数
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<ErrorRecord(id={self.id}, user_id={self.user_id}, knowledge_point='{self.knowledge_point}')>"

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 练习基本信息
    title = Column(String(200), nullable=False)   # 练习标题
    subject = Column(String(50), nullable=False)  # 学科
    grade = Column(String(20), nullable=False)    # 年级
    knowledge_points = Column(JSON, nullable=False)  # 涉及的知识点列表
    
    # 题目配置
    question_types = Column(JSON, nullable=False) # 题型配置 ["choice", "fill", "solve"]
    question_count = Column(Integer, nullable=False)  # 题目数量
    difficulty_level = Column(Integer, default=2) # 整体难度等级
    
    # 生成信息
    ai_model_used = Column(String(100))           # 使用的AI模型
    generation_prompt = Column(Text)              # 生成提示词
    
    # 文件信息
    pdf_file_path = Column(String(255))           # 题目PDF路径
    answer_file_path = Column(String(255))        # 答案PDF路径
    analysis_file_path = Column(String(255))      # 分析PDF路径
    
    # 状态信息
    status = Column(String(20), default="generated")  # generated, downloaded, completed
    is_completed = Column(Boolean, default=False)
    completion_score = Column(Float)              # 完成得分
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<Exercise(id={self.id}, title='{self.title}', user_id={self.user_id})>"

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    
    # 题目信息
    question_number = Column(Integer, nullable=False)  # 题目序号
    question_type = Column(String(20), nullable=False) # choice, fill, solve, judge
    question_text = Column(Text, nullable=False)       # 题目内容
    question_image = Column(String(255))               # 题目图片
    
    # 选择题选项
    options = Column(JSON)  # 选择题选项 {"A": "选项A", "B": "选项B", ...}
    
    # 答案信息
    correct_answer = Column(Text, nullable=False)      # 正确答案
    answer_explanation = Column(Text)                  # 答案解析
    knowledge_point = Column(String(200), nullable=False)  # 对应知识点
    
    # 难度和分值
    difficulty_level = Column(Integer, default=2)      # 难度等级
    points = Column(Float, default=1.0)                # 分值
    
    # 学生作答
    student_answer = Column(Text)                      # 学生答案
    is_correct = Column(Boolean)                       # 是否正确
    answer_time = Column(Integer)                      # 答题用时(秒)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    answered_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<Question(id={self.id}, exercise_id={self.exercise_id}, type='{self.question_type}')>"

class LearningReport(Base):
    __tablename__ = "learning_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 报告基本信息
    report_type = Column(String(20), nullable=False)  # daily, weekly, monthly
    title = Column(String(200), nullable=False)
    subject = Column(String(50))
    
    # 时间范围
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # 报告内容
    summary = Column(Text)                            # 总结
    knowledge_mastery = Column(JSON)                  # 知识点掌握情况
    error_analysis = Column(JSON)                     # 错题分析
    progress_data = Column(JSON)                      # 进度数据
    suggestions = Column(Text)                        # 学习建议
    
    # 统计数据
    total_exercises = Column(Integer, default=0)      # 总练习数
    total_questions = Column(Integer, default=0)      # 总题目数
    correct_count = Column(Integer, default=0)        # 正确题目数
    accuracy_rate = Column(Float, default=0.0)        # 正确率
    
    # 生成信息
    ai_model_used = Column(String(100))               # 使用的AI模型
    generation_time = Column(Float)                   # 生成耗时
    
    # 文件信息
    pdf_file_path = Column(String(255))               # 报告PDF路径
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<LearningReport(id={self.id}, user_id={self.user_id}, type='{self.report_type}')>"
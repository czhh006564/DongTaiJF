from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    student = "student"
    parent = "parent"
    teacher = "teacher"
    institution = "institution"
    super_admin = "super_admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    real_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default=UserRole.student)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    error_records = relationship("ErrorRecord", back_populates="user")
    exercises = relationship("Exercise", back_populates="user")
    game_data = relationship("UserGameData", back_populates="user", uselist=False)
    learning_reports = relationship("LearningReport", back_populates="user")

class AIModelConfig(Base):
    __tablename__ = "ai_model_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)  # tongyi, deepseek, chatgpt
    display_name = Column(String(100), nullable=False)  # 显示名称
    api_endpoint = Column(String(500), nullable=False)
    api_key = Column(Text, nullable=False)  # 加密存储
    model_params = Column(JSON, nullable=True)  # 模型参数配置
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    max_tokens = Column(Integer, default=2000)
    temperature = Column(Float, default=0.7)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AICallLog(Base):
    __tablename__ = "ai_call_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_name = Column(String(100), nullable=False)
    function_type = Column(String(100), nullable=False)  # generate_exercise, analyze_error, etc.
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    response_time = Column(Float, nullable=False)  # 响应时间（秒）
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")

class ErrorRecord(Base):
    __tablename__ = "error_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=False)  # 学科
    knowledge_point = Column(String(200), nullable=False)  # 知识点
    question_type = Column(String(50), nullable=False)  # 题目类型
    difficulty_level = Column(Integer, default=1)  # 难度等级 1-5
    error_count = Column(Integer, default=1)  # 错误次数
    last_error_time = Column(DateTime(timezone=True), server_default=func.now())
    is_resolved = Column(Boolean, default=False)  # 是否已解决
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="error_records")

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    subject = Column(String(100), nullable=False)
    question_type = Column(String(50), nullable=False)  # choice, fill, solve, mixed
    question_count = Column(Integer, nullable=False)
    difficulty_level = Column(Integer, default=1)
    generated_content = Column(JSON, nullable=False)  # 生成的题目内容
    pdf_path = Column(String(500), nullable=True)  # PDF文件路径
    answer_content = Column(JSON, nullable=True)  # 答案和解析
    completion_status = Column(String(20), default="pending")  # pending, completed, reviewed
    score = Column(Float, nullable=True)  # 得分
    completion_time = Column(Integer, nullable=True)  # 完成时间（秒）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="exercises")

class UserGameData(Base):
    __tablename__ = "user_game_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    total_points = Column(Integer, default=0)  # 总积分
    current_level = Column(Integer, default=1)  # 当前等级
    experience_points = Column(Integer, default=0)  # 经验值
    consecutive_days = Column(Integer, default=0)  # 连续学习天数
    total_exercises = Column(Integer, default=0)  # 总练习数
    correct_answers = Column(Integer, default=0)  # 正确答案数
    last_activity_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="game_data")
    badges = relationship("UserBadge", back_populates="user_game_data")

class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    icon = Column(String(100), nullable=False)  # 图标
    condition_type = Column(String(50), nullable=False)  # consecutive_days, total_exercises, accuracy_rate
    condition_value = Column(Integer, nullable=False)  # 达成条件的数值
    points_reward = Column(Integer, default=0)  # 获得积分奖励
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserBadge(Base):
    __tablename__ = "user_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_game_data_id = Column(Integer, ForeignKey("user_game_data.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user_game_data = relationship("UserGameData", back_populates="badges")
    badge = relationship("Badge")

class LearningReport(Base):
    __tablename__ = "learning_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_type = Column(String(50), nullable=False)  # daily, weekly, monthly
    report_period = Column(String(100), nullable=False)  # 报告周期，如 "2024-01-01 to 2024-01-07"
    knowledge_analysis = Column(JSON, nullable=False)  # 知识点分析
    progress_data = Column(JSON, nullable=False)  # 进度数据
    suggestions = Column(JSON, nullable=False)  # AI生成的建议
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="learning_reports")

class SystemConfig(Base):
    __tablename__ = "system_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(Text, nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
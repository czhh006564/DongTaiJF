# 游戏化系统相关数据模型
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, Float
from sqlalchemy.sql import func
from .database import Base

class UserGameData(Base):
    __tablename__ = "user_game_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # 积分系统
    total_points = Column(Integer, default=0)         # 总积分
    available_points = Column(Integer, default=0)     # 可用积分
    used_points = Column(Integer, default=0)          # 已使用积分
    
    # 等级系统
    current_level = Column(Integer, default=1)        # 当前等级
    level_progress = Column(Float, default=0.0)       # 等级进度 (0-1)
    next_level_points = Column(Integer, default=100)  # 升级所需积分
    
    # 连续学习
    current_streak = Column(Integer, default=0)       # 当前连续天数
    longest_streak = Column(Integer, default=0)       # 最长连续天数
    last_activity_date = Column(DateTime(timezone=True))  # 最后活动日期
    
    # 统计数据
    total_exercises = Column(Integer, default=0)      # 总练习次数
    total_questions = Column(Integer, default=0)      # 总答题数
    correct_answers = Column(Integer, default=0)      # 正确答题数
    total_study_time = Column(Integer, default=0)     # 总学习时间(分钟)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserGameData(user_id={self.user_id}, level={self.current_level}, points={self.total_points})>"

class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(255))                        # 徽章图标URL
    category = Column(String(50), default="general")  # 徽章分类
    
    # 获得条件
    condition_type = Column(String(50), nullable=False)  # streak, points, exercises, accuracy
    condition_value = Column(Integer, nullable=False)    # 条件数值
    condition_description = Column(Text)                 # 条件描述
    
    # 奖励
    points_reward = Column(Integer, default=0)        # 积分奖励
    
    # 稀有度
    rarity = Column(String(20), default="common")     # common, rare, epic, legendary
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Badge(id={self.id}, name='{self.name}', rarity='{self.rarity}')>"

class UserBadge(Base):
    __tablename__ = "user_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    
    # 获得信息
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    is_displayed = Column(Boolean, default=True)      # 是否在个人资料中显示
    
    def __repr__(self):
        return f"<UserBadge(user_id={self.user_id}, badge_id={self.badge_id})>"

class DailyTask(Base):
    __tablename__ = "daily_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(255))                        # 任务图标
    
    # 任务配置
    task_type = Column(String(50), nullable=False)    # exercise, streak, time, accuracy
    target_value = Column(Integer, nullable=False)    # 目标数值
    
    # 奖励
    points_reward = Column(Integer, default=10)       # 积分奖励
    
    # 状态
    is_active = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<DailyTask(id={self.id}, name='{self.name}', points={self.points_reward})>"

class UserDailyTask(Base):
    __tablename__ = "user_daily_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("daily_tasks.id"), nullable=False)
    
    # 任务状态
    task_date = Column(DateTime(timezone=True), nullable=False)  # 任务日期
    current_progress = Column(Integer, default=0)     # 当前进度
    target_progress = Column(Integer, nullable=False) # 目标进度
    is_completed = Column(Boolean, default=False)     # 是否完成
    completed_at = Column(DateTime(timezone=True))    # 完成时间
    
    # 奖励
    points_earned = Column(Integer, default=0)        # 获得积分
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserDailyTask(user_id={self.user_id}, task_id={self.task_id}, completed={self.is_completed})>"

class PointsTransaction(Base):
    __tablename__ = "points_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 交易信息
    transaction_type = Column(String(20), nullable=False)  # earn, spend, bonus, penalty
    points = Column(Integer, nullable=False)               # 积分数量 (正数为获得，负数为消费)
    description = Column(String(200), nullable=False)      # 交易描述
    
    # 关联信息
    related_type = Column(String(50))                      # exercise, badge, task, admin
    related_id = Column(Integer)                           # 关联对象ID
    
    # 余额信息
    balance_before = Column(Integer, nullable=False)       # 交易前余额
    balance_after = Column(Integer, nullable=False)        # 交易后余额
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<PointsTransaction(user_id={self.user_id}, type='{self.transaction_type}', points={self.points})>"
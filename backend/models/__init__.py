# 模型初始化文件
from .database import Base, engine, get_db
from .user import User, UserRole, RolePermission
from .config import AIModelConfig, SystemConfig, SystemLog, AuditLog
from .exercise import ErrorRecord, Exercise, Question, LearningReport
from .gamification import UserGameData, Badge, UserBadge, DailyTask, UserDailyTask, PointsTransaction

# 导出所有模型
__all__ = [
    "Base",
    "engine", 
    "get_db",
    "User",
    "UserRole",
    "RolePermission",
    "AIModelConfig",
    "SystemConfig", 
    "SystemLog",
    "AuditLog",
    "ErrorRecord",
    "Exercise",
    "Question",
    "LearningReport",
    "UserGameData",
    "Badge",
    "UserBadge", 
    "DailyTask",
    "UserDailyTask",
    "PointsTransaction"
]
# 用户相关数据模型
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
from .database import Base
import enum

class UserRole(enum.Enum):
    STUDENT = "student"          # 学生
    PARENT = "parent"            # 家长
    TEACHER = "teacher"          # 老师
    INSTITUTION = "institution"  # 机构
    SUPER_ADMIN = "super_admin"  # 超级管理员

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # 用户信息
    real_name = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    avatar = Column(String(255))  # 头像URL
    
    # 学生特有信息
    grade = Column(String(20))    # 年级
    school = Column(String(100))  # 学校
    class_name = Column(String(50))  # 班级
    
    # 状态信息
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"

class RolePermission(Base):
    __tablename__ = "roles_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(UserRole), nullable=False)
    permission = Column(String(100), nullable=False)  # 权限标识
    description = Column(Text)  # 权限描述
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<RolePermission(role='{self.role.value}', permission='{self.permission}')>"
# 系统配置相关数据模型
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from .database import Base

class AIModelConfig(Base):
    __tablename__ = "ai_model_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)  # 模型名称 (如: tongyi-qwen, deepseek, gpt-4)
    model_display_name = Column(String(100), nullable=False)  # 显示名称
    api_endpoint = Column(String(255), nullable=False)  # API端点
    api_key = Column(Text, nullable=False)  # API密钥 (加密存储)
    
    # 模型配置参数
    max_tokens = Column(Integer, default=2000)
    temperature = Column(String(10), default="0.7")
    model_params = Column(JSON)  # 其他模型参数
    
    # 状态信息
    is_active = Column(Boolean, default=False)  # 是否启用
    is_default = Column(Boolean, default=False)  # 是否为默认模型
    
    # 使用统计
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime(timezone=True))
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<AIModelConfig(id={self.id}, model_name='{self.model_name}', is_default={self.is_default})>"

class SystemConfig(Base):
    __tablename__ = "system_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(Text, nullable=False)
    config_type = Column(String(20), default="string")  # string, integer, boolean, json
    description = Column(Text)
    category = Column(String(50), default="general")  # 配置分类
    
    # 权限控制
    is_public = Column(Boolean, default=False)  # 是否为公开配置
    requires_restart = Column(Boolean, default=False)  # 是否需要重启系统
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<SystemConfig(key='{self.config_key}', category='{self.category}')>"

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)  # INFO, WARNING, ERROR, DEBUG
    message = Column(Text, nullable=False)
    module = Column(String(100))  # 模块名称
    function = Column(String(100))  # 函数名称
    
    # 用户信息
    user_id = Column(Integer)
    user_role = Column(String(20))
    
    # 请求信息
    ip_address = Column(String(45))
    user_agent = Column(Text)
    request_id = Column(String(100))
    
    # 额外数据
    extra_data = Column(JSON)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.level}', module='{self.module}')>"

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)  # 操作类型
    resource = Column(String(100), nullable=False)  # 操作资源
    resource_id = Column(String(100))  # 资源ID
    
    # 用户信息
    user_id = Column(Integer, nullable=False)
    user_role = Column(String(20), nullable=False)
    username = Column(String(50), nullable=False)
    
    # 操作详情
    old_values = Column(JSON)  # 操作前的值
    new_values = Column(JSON)  # 操作后的值
    description = Column(Text)  # 操作描述
    
    # 请求信息
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # 结果信息
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', user='{self.username}')>"
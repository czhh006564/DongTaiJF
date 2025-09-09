# 超级管理员相关路由
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from models.database import get_db
from models.user import User, UserRole
from routes.auth import get_current_user

router = APIRouter()

# Pydantic模型
class AIModelConfig(BaseModel):
    model_name: str
    api_key: str
    api_endpoint: str
    is_active: bool = True

class SystemConfig(BaseModel):
    key: str
    value: str
    description: Optional[str] = None

class SystemStats(BaseModel):
    total_users: int
    active_users: int
    total_exercises: int
    ai_requests_today: int

# 权限检查装饰器
def require_super_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return current_user

# 获取系统统计信息
@router.get("/stats", response_model=SystemStats)
async def get_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """
    获取系统统计信息
    """
    # TODO: 从数据库查询真实统计数据
    return SystemStats(
        total_users=100,
        active_users=85,
        total_exercises=500,
        ai_requests_today=1200
    )

# AI模型配置管理
@router.get("/ai-models")
async def get_ai_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """
    获取AI模型配置列表
    """
    # TODO: 从数据库查询
    return [
        {
            "id": 1,
            "model_name": "通义千问",
            "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            "is_active": True,
            "is_default": True
        },
        {
            "id": 2,
            "model_name": "DeepSeek",
            "api_endpoint": "https://api.deepseek.com/v1/chat/completions",
            "is_active": False,
            "is_default": False
        }
    ]

@router.post("/ai-models")
async def create_ai_model_config(
    config: AIModelConfig,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """
    创建AI模型配置
    """
    # TODO: 保存到数据库，加密API密钥
    return {
        "id": 3,
        "model_name": config.model_name,
        "api_endpoint": config.api_endpoint,
        "is_active": config.is_active,
        "message": "AI模型配置创建成功"
    }

@router.put("/ai-models/{model_id}")
async def update_ai_model_config(
    model_id: int,
    config: AIModelConfig,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """
    更新AI模型配置
    """
    # TODO: 更新数据库记录
    return {"message": "AI模型配置更新成功"}

# 系统配置管理
@router.get("/system-config")
async def get_system_config(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """
    获取系统配置
    """
    return [
        {"key": "max_daily_requests", "value": "1000", "description": "每日最大AI请求数"},
        {"key": "default_ai_model", "value": "tongyi", "description": "默认AI模型"},
        {"key": "enable_registration", "value": "true", "description": "是否允许用户注册"}
    ]

@router.post("/system-config")
async def update_system_config(
    configs: List[SystemConfig],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """
    更新系统配置
    """
    # TODO: 批量更新系统配置
    return {"message": f"成功更新{len(configs)}项系统配置"}

# 用户管理
@router.get("/users")
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[UserRole] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """
    获取所有用户列表
    """
    # TODO: 从数据库查询
    return [
        {
            "id": 1,
            "username": "student1",
            "email": "student1@example.com",
            "role": "student",
            "is_active": True,
            "created_at": "2024-01-01T10:00:00"
        }
    ]

# 系统日志
@router.get("/logs")
async def get_system_logs(
    skip: int = 0,
    limit: int = 100,
    level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """
    获取系统日志
    """
    return [
        {
            "id": 1,
            "level": "INFO",
            "message": "用户登录成功",
            "timestamp": "2024-01-01T10:00:00",
            "user_id": 1
        }
    ]
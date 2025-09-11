from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import json

from ..database.database import get_db
from ..database.models import User, AIModelConfig, Exercise, ErrorRecord
from .auth import get_current_user
from ..utils.security import encrypt_api_key, decrypt_api_key
from ..services.ai_service import AIService

router = APIRouter(prefix="/admin", tags=["超级管理员"])

# 请求模型
class AIModelRequest(BaseModel):
    display_name: str
    model_name: str
    api_endpoint: str
    api_key: str
    max_tokens: Optional[int] = 2000
    temperature: Optional[float] = 0.7
    is_active: bool = True
    is_default: bool = False

class AIModelUpdate(BaseModel):
    display_name: Optional[str] = None
    model_name: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None

# 响应模型
class AIModelResponse(BaseModel):
    id: int
    display_name: str
    model_name: str
    api_endpoint: str
    max_tokens: int
    temperature: float
    is_active: bool
    is_default: bool
    usage_count: int
    last_used: Optional[datetime]
    created_at: datetime

def check_admin_permission(current_user: User = Depends(get_current_user)):
    """检查超级管理员权限"""
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要超级管理员权限"
        )
    return current_user

@router.get("/ai-models")
async def get_ai_models(
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """获取所有AI模型配置"""
    
    models = db.query(AIModelConfig).all()
    
    return {
        "models": [
            {
                "id": model.id,
                "display_name": model.display_name,
                "model_name": model.model_name,
                "api_endpoint": model.api_endpoint,
                "max_tokens": model.max_tokens,
                "temperature": model.temperature,
                "is_active": model.is_active,
                "is_default": model.is_default,
                "usage_count": model.usage_count,
                "last_used": model.last_used,
                "created_at": model.created_at
            }
            for model in models
        ]
    }

@router.post("/ai-models")
async def create_ai_model(
    model_data: AIModelRequest,
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """创建新的AI模型配置"""
    
    # 检查模型名称是否已存在
    existing_model = db.query(AIModelConfig).filter(
        AIModelConfig.model_name == model_data.model_name
    ).first()
    
    if existing_model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="模型名称已存在"
        )
    
    # 如果设置为默认模型，先取消其他默认模型
    if model_data.is_default:
        db.query(AIModelConfig).filter(AIModelConfig.is_default == True).update(
            {"is_default": False}
        )
    
    # 加密API密钥
    encrypted_key = encrypt_api_key(model_data.api_key)
    
    # 创建新模型配置
    new_model = AIModelConfig(
        display_name=model_data.display_name,
        model_name=model_data.model_name,
        api_endpoint=model_data.api_endpoint,
        encrypted_api_key=encrypted_key,
        max_tokens=model_data.max_tokens,
        temperature=model_data.temperature,
        is_active=model_data.is_active,
        is_default=model_data.is_default,
        usage_count=0
    )
    
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    
    return {
        "success": True,
        "message": "AI模型配置创建成功",
        "model_id": new_model.id
    }

@router.put("/ai-models/{model_id}")
async def update_ai_model(
    model_id: int,
    model_data: AIModelUpdate,
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """更新AI模型配置"""
    
    model = db.query(AIModelConfig).filter(AIModelConfig.id == model_id).first()
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模型配置不存在"
        )
    
    # 如果设置为默认模型，先取消其他默认模型
    if model_data.is_default:
        db.query(AIModelConfig).filter(
            AIModelConfig.is_default == True,
            AIModelConfig.id != model_id
        ).update({"is_default": False})
    
    # 更新字段
    update_data = model_data.dict(exclude_unset=True)
    
    # 处理API密钥加密
    if "api_key" in update_data and update_data["api_key"]:
        update_data["encrypted_api_key"] = encrypt_api_key(update_data["api_key"])
        del update_data["api_key"]
    
    for field, value in update_data.items():
        setattr(model, field, value)
    
    db.commit()
    
    return {
        "success": True,
        "message": "AI模型配置更新成功"
    }

@router.patch("/ai-models/{model_id}/toggle")
async def toggle_model_status(
    model_id: int,
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """切换模型启用/停用状态"""
    
    model = db.query(AIModelConfig).filter(AIModelConfig.id == model_id).first()
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模型配置不存在"
        )
    
    # 切换状态
    model.is_active = not model.is_active
    
    # 如果停用的是默认模型，需要取消默认设置
    if not model.is_active and model.is_default:
        model.is_default = False
    
    db.commit()
    
    return {
        "success": True,
        "message": f"模型已{'启用' if model.is_active else '停用'}",
        "is_active": model.is_active
    }

@router.patch("/ai-models/{model_id}/set-default")
async def set_default_model(
    model_id: int,
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """设置默认模型"""
    
    model = db.query(AIModelConfig).filter(AIModelConfig.id == model_id).first()
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模型配置不存在"
        )
    
    if not model.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能将活跃模型设为默认"
        )
    
    # 取消其他默认模型
    db.query(AIModelConfig).filter(AIModelConfig.is_default == True).update(
        {"is_default": False}
    )
    
    # 设置当前模型为默认
    model.is_default = True
    db.commit()
    
    return {
        "success": True,
        "message": "默认模型设置成功"
    }

@router.post("/ai-models/{model_id}/test")
async def test_model(
    model_id: int,
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """测试AI模型连接"""
    
    model = db.query(AIModelConfig).filter(AIModelConfig.id == model_id).first()
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模型配置不存在"
        )
    
    if not model.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能测试活跃模型"
        )
    
    try:
        # 使用AI服务测试连接
        start_time = datetime.now()
        
        async with AIService(db) as ai_service:
            # 发送测试消息
            result = await ai_service.test_model_connection(model_id)
        
        end_time = datetime.now()
        response_time = int((end_time - start_time).total_seconds() * 1000)
        
        if result['success']:
            return {
                "success": True,
                "message": "模型测试成功",
                "response_time": response_time
            }
        else:
            return {
                "success": False,
                "error": result.get('error', '测试失败'),
                "response_time": response_time
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_time": 0
        }

@router.delete("/ai-models/{model_id}")
async def delete_ai_model(
    model_id: int,
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """删除AI模型配置"""
    
    model = db.query(AIModelConfig).filter(AIModelConfig.id == model_id).first()
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模型配置不存在"
        )
    
    # 检查是否为默认模型
    if model.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除默认模型，请先设置其他模型为默认"
        )
    
    db.delete(model)
    db.commit()
    
    return {
        "success": True,
        "message": "AI模型配置删除成功"
    }

@router.get("/ai-stats")
async def get_ai_stats(
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """获取AI使用统计"""
    
    # 计算今日统计
    today = datetime.now().date()
    daily_usage = db.query(func.sum(AIModelConfig.usage_count)).filter(
        func.date(AIModelConfig.last_used) == today
    ).scalar() or 0
    
    # 计算本月统计
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_usage = db.query(func.sum(AIModelConfig.usage_count)).filter(
        AIModelConfig.last_used >= month_start
    ).scalar() or 0
    
    # 计算总使用次数
    total_usage = db.query(func.sum(AIModelConfig.usage_count)).scalar() or 0
    
    # 活跃模型数量
    active_models = db.query(AIModelConfig).filter(AIModelConfig.is_active == True).count()
    
    # 模拟成功率和响应时间（实际项目中应该从日志或监控系统获取）
    success_rate = 95.5
    avg_response_time = 1200
    
    return {
        "daily": {"calls": daily_usage},
        "monthly": {"calls": monthly_usage},
        "total_usage": total_usage,
        "active_models": active_models,
        "success_rate": success_rate,
        "avg_response_time": avg_response_time
    }

@router.get("/users")
async def get_all_users(
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """获取所有用户列表"""
    
    users = db.query(User).offset(skip).limit(limit).all()
    total = db.query(User).count()
    
    return {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "real_name": user.real_name,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "last_login": user.last_login
            }
            for user in users
        ],
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.patch("/users/{user_id}/toggle")
async def toggle_user_status(
    user_id: int,
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """切换用户启用/停用状态"""
    
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能停用自己的账号"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    user.is_active = not user.is_active
    db.commit()
    
    return {
        "success": True,
        "message": f"用户已{'启用' if user.is_active else '停用'}",
        "is_active": user.is_active
    }

@router.get("/system-stats")
async def get_system_stats(
    current_user: User = Depends(check_admin_permission),
    db: Session = Depends(get_db)
):
    """获取系统统计信息"""
    
    # 用户统计
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    # 按角色统计用户
    role_stats = {}
    for role in ['student', 'parent', 'teacher', 'institution', 'super_admin']:
        count = db.query(User).filter(User.role == role).count()
        role_stats[role] = count
    
    # 练习统计
    total_exercises = db.query(Exercise).count()
    completed_exercises = db.query(Exercise).filter(
        Exercise.completion_status == 'completed'
    ).count()
    
    # 错题统计
    total_errors = db.query(ErrorRecord).count()
    
    # 今日新增用户
    today = datetime.now().date()
    today_users = db.query(User).filter(
        func.date(User.created_at) == today
    ).count()
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "today_new": today_users,
            "by_role": role_stats
        },
        "exercises": {
            "total": total_exercises,
            "completed": completed_exercises,
            "completion_rate": round(completed_exercises / total_exercises * 100, 1) if total_exercises > 0 else 0
        },
        "errors": {
            "total": total_errors
        }
    }
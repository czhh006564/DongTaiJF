# 路由模块初始化文件
from .auth import router as auth_router
from .user import router as user_router
from .ai import router as ai_router
from .exercise import router as exercise_router
from .admin import router as admin_router

__all__ = [
    "auth_router",
    "user_router", 
    "ai_router",
    "exercise_router",
    "admin_router"
]
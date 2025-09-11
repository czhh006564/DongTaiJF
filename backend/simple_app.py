# 简化版应用启动文件
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
import asyncio
import random

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 创建FastAPI应用
app = FastAPI(
    title="精准动态教辅系统",
    description="AI驱动的个性化教育辅助平台",
    version="2.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基础路由
@app.get("/")
async def root():
    return {"message": "精准动态教辅系统 API", "version": "2.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "系统运行正常"}

# 简单的认证路由
@app.post("/auth/login")
async def login(request_data: dict = None):
    # 获取用户名，用于确定角色
    username = request_data.get("username", "student1") if request_data else "student1"
    
    # 根据用户名确定角色和相关信息
    role = "student"  # 默认角色
    real_name = "测试用户"
    user_id = 1
    
    if "teacher" in username.lower() or username.lower().startswith("t"):
        role = "teacher"
        real_name = "测试教师"
        user_id = 2
    elif "parent" in username.lower() or username.lower().startswith("p"):
        role = "parent"
        real_name = "测试家长"
        user_id = 3
    elif "admin" in username.lower() or username.lower().startswith("a"):
        role = "super_admin"
        real_name = "系统管理员"
        user_id = 4
    elif "institution" in username.lower() or username.lower().startswith("i"):
        role = "institution"
        real_name = "测试机构"
        user_id = 5
    else:
        role = "student"
        real_name = "测试学生"
        user_id = 1
    
    return {
        "success": True,
        "access_token": "test_token",
        "token_type": "bearer",
        "user_info": {
            "id": user_id,
            "username": username,
            "real_name": real_name,
            "role": role,
            "email": f"{username}@test.com",
            "is_active": True
        },
        "message": "登录成功"
    }

# AI模型管理相关路由
@app.get("/api/admin/ai-models")
async def get_ai_models():
    # 模拟返回AI模型列表
    return {
        "models": [
            {
                "id": 1,
                "display_name": "通义千问-Turbo",
                "model_name": "qwen-turbo",
                "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
                "usage_count": 1250,
                "last_used": "2024-01-15T10:30:00",
                "is_active": True,
                "is_default": True,
                "max_tokens": 2000,
                "temperature": 0.7
            }
        ]
    }

@app.get("/api/admin/ai-stats")
async def get_ai_stats():
    # 模拟返回AI统计数据
    return {
        "daily": {"calls": 156},
        "monthly": {"calls": 4520},
        "success_rate": 98.5,
        "avg_response_time": 850
    }

@app.post("/api/admin/ai-models/test-connection")
async def test_ai_connection(request_data: dict):
    import time
    import random
    
    # 模拟连通测试
    provider = request_data.get("provider")
    model_name = request_data.get("model_name")
    api_endpoint = request_data.get("api_endpoint")
    api_key = request_data.get("api_key")
    
    # 基本验证
    if not all([provider, model_name, api_endpoint, api_key]):
        return {
            "success": False,
            "error": "缺少必要参数"
        }
    
    # 模拟网络延迟
    await asyncio.sleep(random.uniform(0.5, 2.0))
    
    # 模拟测试结果（90%成功率）
    if random.random() < 0.9:
        response_time = random.randint(200, 1500)
        return {
            "success": True,
            "response_time": response_time,
            "test_response": f"模型 {model_name} 连接正常",
            "message": "连通测试成功"
        }
    else:
        error_messages = [
            "API密钥无效",
            "网络连接超时",
            "模型服务暂不可用",
            "请求频率过高"
        ]
        return {
            "success": False,
            "error": random.choice(error_messages)
        }

@app.post("/api/admin/ai-models")
async def create_ai_model(request_data: dict):
    # 模拟创建AI模型配置
    return {
        "success": True,
        "message": "AI模型配置创建成功",
        "model_id": random.randint(100, 999)
    }

@app.put("/api/admin/ai-models/{model_id}")
async def update_ai_model(model_id: int, request_data: dict):
    # 模拟更新AI模型配置
    return {
        "success": True,
        "message": "AI模型配置更新成功"
    }

@app.patch("/api/admin/ai-models/{model_id}/toggle")
async def toggle_model_status(model_id: int):
    # 模拟切换模型状态
    return {
        "success": True,
        "message": "模型状态切换成功"
    }

@app.patch("/api/admin/ai-models/{model_id}/set-default")
async def set_default_model(model_id: int):
    # 模拟设置默认模型
    return {
        "success": True,
        "message": "默认模型设置成功"
    }

@app.post("/api/admin/ai-models/{model_id}/test")
async def test_model_by_id(model_id: int):
    # 模拟测试指定模型
    await asyncio.sleep(random.uniform(0.5, 1.5))
    
    if random.random() < 0.9:
        response_time = random.randint(200, 1200)
        return {
            "success": True,
            "response_time": response_time,
            "message": "模型测试成功"
        }
    else:
        return {
            "success": False,
            "error": "模型连接失败"
        }

if __name__ == "__main__":
    uvicorn.run("simple_app:app", host="0.0.0.0", port=8000, reload=True)
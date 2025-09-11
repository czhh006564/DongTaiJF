# 简化版应用启动文件
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

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

if __name__ == "__main__":
    uvicorn.run("simple_app:app", host="0.0.0.0", port=8000, reload=True)
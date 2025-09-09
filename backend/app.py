# 精准动态教辅 - 主应用入口
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入路由
from routes.auth import router as auth_router
from routes.ai import router as ai_router
from routes.user import router as user_router
from routes.exercise import router as exercise_router
from routes.admin import router as admin_router

# 导入数据库
from models.database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="精准动态教辅系统",
    description="基于AI的个性化教育辅助平台",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],  # Vue.js开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册路由
app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
app.include_router(user_router, prefix="/api/user", tags=["用户管理"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI功能"])
app.include_router(exercise_router, prefix="/api/exercise", tags=["练习题目"])
app.include_router(admin_router, prefix="/api/admin", tags=["超级管理员"])

@app.get("/")
async def root():
    return {"message": "精准动态教辅系统API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "系统运行正常"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
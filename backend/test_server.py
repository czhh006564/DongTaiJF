#!/usr/bin/env python3
# 最简单的测试服务器
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="测试服务器")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "测试服务器运行正常"}

@app.get("/api/ai/test-connection")
async def test_connection():
    print("收到连通性测试请求")
    return {
        "status": "success",
        "message": "AI模型连通正常",
        "model": "qwen-vl-max"
    }

@app.post("/api/photo-correction")
async def photo_correction():
    print("收到拍照批阅请求")
    return {
        "success": True,
        "results": [
            {
                "image_id": 1,
                "corrections": [
                    {
                        "question": "测试题目：2+3=?",
                        "student_answer": "5",
                        "correct_answer": "5",
                        "is_correct": True,
                        "explanation": "答案正确！",
                        "knowledge_points": ["加法运算"]
                    }
                ]
            }
        ]
    }

if __name__ == "__main__":
    print("启动测试服务器...")
    print("访问地址: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
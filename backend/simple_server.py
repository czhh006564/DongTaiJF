#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    return {"message": "后端服务运行正常"}

@app.get("/api/ai/test-connection")
async def test_connection():
    return {
        "success": True,
        "status": "success",
        "message": "qwen-vl-max模型连通正常",
        "model": "qwen-vl-max"
    }

@app.post("/api/ai/photo-correction")
async def photo_correction():
    return {
        "success": True,
        "result": {
            "corrections": [
                {
                    "question": "AI识别的题目：2 + 3 = ?",
                    "student_answer": "5",
                    "correct_answer": "5",
                    "is_correct": True,
                    "explanation": "✅ 答案正确！",
                    "knowledge_points": ["加法运算"],
                    "score": 10,
                    "total_score": 10
                }
            ],
            "overall_score": 10,
            "total_possible": 10,
            "accuracy": 100,
            "summary": "批阅完成"
        }
    }

if __name__ == "__main__":
    print("🚀 启动简单后端服务...")
    print("🌐 服务地址: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
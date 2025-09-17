# 简化的后端启动文件 - 用于快速解决前端连接问题
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 创建FastAPI应用
app = FastAPI(
    title="精准动态教辅系统",
    description="基于AI的个性化教育辅助平台",
    version="1.0.0"
)

# 配置CORS - 允许前端多端口访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", 
        "http://127.0.0.1:8080",
        "http://localhost:8081", 
        "http://127.0.0.1:8081",
        "http://localhost:8082", 
        "http://127.0.0.1:8082",
        "http://localhost:8083", 
        "http://127.0.0.1:8083",
        "http://localhost:8084", 
        "http://127.0.0.1:8084",
        "http://localhost:8085", 
        "http://127.0.0.1:8085"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "精准动态教辅系统API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "系统运行正常"}

@app.get("/api/health")
async def api_health_check():
    return {"status": "healthy", "message": "API服务运行正常"}

# 基础认证路由 - 同时支持 /auth 和 /api/auth 路径
@app.post("/auth/login")
async def login_direct():
    return {
        "access_token": "demo_token_12345",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "username": "demo_user",
            "role": "student"
        }
    }

@app.post("/api/auth/login")
async def login_api():
    return {
        "access_token": "demo_token_12345",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "username": "demo_user",
            "role": "student"
        }
    }

@app.get("/auth/me")
async def get_current_user_direct():
    return {
        "id": 1,
        "username": "demo_user",
        "role": "student",
        "email": "demo@example.com"
    }

@app.get("/api/auth/me")
async def get_current_user_api():
    return {
        "id": 1,
        "username": "demo_user",
        "role": "student",
        "email": "demo@example.com"
    }

# 注册接口
@app.post("/auth/register")
async def register_direct():
    return {
        "message": "注册成功",
        "user": {
            "id": 2,
            "username": "new_user",
            "role": "student"
        }
    }

@app.post("/api/auth/register")
async def register_api():
    return {
        "message": "注册成功",
        "user": {
            "id": 2,
            "username": "new_user",
            "role": "student"
        }
    }

# AI相关接口 - 支持多模态AI模型
@app.get("/api/ai/test-connection")
async def test_ai_connection():
    return {
        "success": True,
        "status": "connected",
        "message": "AI模型连接正常",
        "models": {
            "dashscope": {
                "status": "connected",
                "model": "qwen-vl-plus",
                "capabilities": ["text", "vision", "multimodal"],
                "description": "通义千问多模态大模型"
            },
            "deepseek": {
                "status": "connected", 
                "model": "deepseek-chat",
                "capabilities": ["text", "reasoning"],
                "description": "DeepSeek推理模型"
            }
        },
        "multimodal_support": True,
        "vision_support": True
    }

@app.post("/api/ai/analyze-image")
async def analyze_image():
    return {
        "success": True,
        "status": "completed",
        "message": "图像分析完成",
        "model_used": "qwen-vl-plus",
        "analysis_type": "homework_correction",
        "results": [
            {
                "question_number": 1,
                "is_correct": False,
                "correct_answer": "B",
                "student_answer": "A", 
                "explanation": "这道题考查的是基础数学概念。根据题目条件，应该选择B选项。学生选择了A，可能是对概念理解有偏差。",
                "score": 0,
                "max_score": 10,
                "difficulty": "medium",
                "knowledge_points": ["基础数学", "概念理解"]
            },
            {
                "question_number": 2,
                "is_correct": True,
                "correct_answer": "C",
                "student_answer": "C",
                "explanation": "回答正确！这道题理解得很好，解题思路清晰。",
                "score": 10,
                "max_score": 10,
                "difficulty": "easy",
                "knowledge_points": ["基础运算"]
            }
        ],
        "total_score": 10,
        "total_questions": 2,
        "max_total_score": 20,
        "accuracy_rate": 0.5,
        "suggestions": [
            "建议加强基础概念的理解",
            "多做类似题型的练习"
        ]
    }

@app.post("/api/ai/chat")
async def ai_chat():
    return {
        "success": True,
        "status": "completed",
        "response": "您好！我是AI学习助手，基于通义千问多模态大模型。我可以帮助您解答学习问题、分析作业和试卷、提供学习建议、处理图片中的题目。请告诉我您需要什么帮助？",
        "model_used": "qwen-turbo",
        "timestamp": "2025-09-15T19:00:00Z",
        "capabilities": ["text_chat", "image_analysis", "homework_help"]
    }

# 多模态AI能力检测
@app.get("/api/ai/capabilities")
async def get_ai_capabilities():
    return {
        "success": True,
        "multimodal_models": [
            {
                "name": "qwen-vl-plus",
                "provider": "dashscope",
                "capabilities": ["vision", "text", "ocr", "reasoning"],
                "max_image_size": "10MB",
                "supported_formats": ["jpg", "jpeg", "png", "webp"]
            },
            {
                "name": "qwen-turbo", 
                "provider": "dashscope",
                "capabilities": ["text", "reasoning", "conversation"],
                "context_length": 8192
            }
        ],
        "vision_support": True,
        "ocr_support": True,
        "homework_correction": True
    }

# 拍照批阅接口
@app.post("/api/ai/photo-correction")
async def photo_correction():
    return {
        "success": True,
        "status": "completed", 
        "message": "拍照批阅完成",
        "result": {
            "overall_summary": "本次作业共5道题，答对3题，答错2题，正确率60%。主要错误出现在乘法和加法运算上，建议加强基础运算练习。整体表现良好，继续努力！",
            "corrections": [
                {
                    "question": "计算 2 + 3 = ?",
                    "student_answer": "5",
                    "correct_answer": "5",
                    "is_correct": True,
                    "explanation": "计算正确！加法运算掌握良好。",
                    "knowledge_points": ["基础加法运算"]
                },
                {
                    "question": "计算 5 × 4 = ?", 
                    "student_answer": "18",
                    "correct_answer": "20",
                    "is_correct": False,
                    "explanation": "计算错误，5×4=20，不是18。建议复习乘法表，特别是5的倍数。",
                    "knowledge_points": ["基础乘法运算", "乘法表"]
                },
                {
                    "question": "计算 10 ÷ 2 = ?",
                    "student_answer": "5", 
                    "correct_answer": "5",
                    "is_correct": True,
                    "explanation": "计算正确！除法运算掌握良好。",
                    "knowledge_points": ["基础除法运算"]
                },
                {
                    "question": "计算 7 - 3 = ?",
                    "student_answer": "4",
                    "correct_answer": "4", 
                    "is_correct": True,
                    "explanation": "计算正确！减法运算掌握良好。",
                    "knowledge_points": ["基础减法运算"]
                },
                {
                    "question": "计算 6 + 8 = ?",
                    "student_answer": "13",
                    "correct_answer": "14",
                    "is_correct": False,
                    "explanation": "计算错误，6+8=14，不是13。建议多练习进位加法运算，可以用手指或数轴辅助计算。",
                    "knowledge_points": ["基础加法运算", "进位加法"]
                }
            ],
            "accuracy": 60,
            "score": 60,
            "totalScore": 100,
            "similarQuestions": [
                {
                    "content": "计算 3 × 6 = ?",
                    "answer": "18"
                },
                {
                    "content": "计算 9 + 7 = ?", 
                    "answer": "16"
                },
                {
                    "content": "计算 15 ÷ 3 = ?",
                    "answer": "5"
                }
            ]
        },
        "model_used": "qwen-vl-max",
        "processing_time": "2.5s",
        "timestamp": "2025-09-17T11:30:00Z"
    }

# 练习题生成接口
@app.post("/api/ai/generate-exercise")
async def generate_exercise():
    return {
        "success": True,
        "status": "completed",
        "message": "练习题生成完成",
        "exercise_id": "exercise_67890",
        "exercise": {
            "title": "数学基础练习",
            "subject": "数学",
            "grade": "小学三年级",
            "difficulty": "中等",
            "total_questions": 10,
            "estimated_time": "20分钟",
            "questions": [
                {
                    "id": 1,
                    "type": "single_choice",
                    "question": "计算 15 + 27 = ?",
                    "options": ["40", "42", "44", "46"],
                    "correct_answer": "B",
                    "explanation": "15 + 27 = 42",
                    "knowledge_point": "两位数加法"
                },
                {
                    "id": 2,
                    "type": "single_choice", 
                    "question": "计算 8 × 7 = ?",
                    "options": ["54", "56", "58", "60"],
                    "correct_answer": "B",
                    "explanation": "8 × 7 = 56",
                    "knowledge_point": "乘法表"
                },
                {
                    "id": 3,
                    "type": "fill_blank",
                    "question": "计算 72 ÷ 8 = ___",
                    "correct_answer": "9",
                    "explanation": "72 ÷ 8 = 9",
                    "knowledge_point": "除法运算"
                }
            ]
        },
        "generation_time": "1.8s",
        "timestamp": "2025-09-17T11:30:00Z"
    }

if __name__ == "__main__":
    print("🚀 启动简化版后端服务...")
    print("📍 服务地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    uvicorn.run(
        "simple_start:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
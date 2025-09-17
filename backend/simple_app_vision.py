# 精准动态教辅系统 - 统一后端服务
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
import httpx
import json
import dashscope
from http import HTTPStatus
from pydantic import BaseModel
from typing import List, Dict, Union, Any

# 加载环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- 配置 ---
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 从环境变量获取API Key配置
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
if not DASHSCOPE_API_KEY:
    print("⚠️ WARNING: DASHSCOPE_API_KEY not found in environment variables")
    print("Please set it in your .env file")
    DASHSCOPE_API_KEY = "your-api-key-not-set"

dashscope.api_key = DASHSCOPE_API_KEY

# 文本生成模型配置
TEXT_AI_CONFIG = {
    "provider": "tongyi",
    "api_key": DASHSCOPE_API_KEY,
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
    "model_name": "qwen-plus",
}

print("🚀 精准动态教辅统一后端服务正在启动...")
print(f"🔑 Dashscope API Key: ...{DASHSCOPE_API_KEY[-4:]}")
print(f"🧠 视觉模型: qwen-vl-max")
print(f"📝 文本模型: {TEXT_AI_CONFIG['model_name']}")

# --- FastAPI 应用设置 ---
app = FastAPI(
    title="精准动态教辅统一后端服务",
    description="统一处理用户认证、AI文本生成和AI视觉识别",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic 模型定义 ---
class PhotoCorrectionRequest(BaseModel):
    image: str
    type: str  # 保持与前端的 'type' 字段一致
    config: Dict[str, Any]

# --- API 端点 ---
@app.get("/")
async def root():
    return {"message": "精准动态教辅统一后端服务", "version": "3.0.0", "vision_model": "qwen-vl-max", "text_model": TEXT_AI_CONFIG['model_name']}

# 登录接口 (保留)
@app.post("/auth/login")
async def login(request_data: dict = None):
    username = request_data.get("username", "student1") if request_data else "student1"
    role, real_name, user_id = "student", "测试学生", 1
    if "teacher" in username.lower() or username.lower().startswith("t"):
        role, real_name, user_id = "teacher", "测试教师", 2
    elif "parent" in username.lower() or username.lower().startswith("p"):
        role, real_name, user_id = "parent", "测试家长", 3
    elif "admin" in username.lower() or username.lower().startswith("a"):
        role, real_name, user_id = "super_admin", "系统管理员", 4
    elif "institution" in username.lower() or username.lower().startswith("i"):
        role, real_name, user_id = "institution", "测试机构", 5
    
    print(f"👤 用户 '{username}' 登录成功，分配角色: {role}")
    return {
        "success": True, "access_token": "unified_backend_test_token", "token_type": "bearer",
        "user_info": {"id": user_id, "username": username, "real_name": real_name, "role": role, "email": f"{username}@test.com", "is_active": True},
        "message": "登录成功"
    }

# AI连通性测试 (新, 使用Dashscope SDK)
@app.get("/api/ai/test-connection")
async def test_connection():
    try:
        print("--- 正在测试 qwen-vl-max 连通性 (SDK) ---")
        messages = [{'role': 'user', 'content': [{'text': "你好，请回复'连接正常'以确认连接。"}]}]
        response = dashscope.MultiModalConversation.call(model='qwen-vl-max', messages=messages)
        if response.status_code == HTTPStatus.OK:
            print("✅ 连通性测试成功")
            return {"success": True, "status": "success", "message": "qwen-vl-max 模型连通正常 (SDK)"}
        else:
            print(f"❌ 连通性测试失败: {response.code} - {response.message}")
            raise HTTPException(status_code=500, detail=f"API返回错误: {response.code} - {response.message}")
    except Exception as e:
        print(f"❌ 连通性测试异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"连接测试时发生异常: {str(e)}")

# AI拍照批阅 (新, 使用Dashscope SDK)
@app.post("/api/ai/photo-correction")
async def photo_correction(request: PhotoCorrectionRequest):
    try:
        print(f"📸 收到批阅请求, 类型: {request.type}, 配置: {request.config}, 图片数据长度: {len(request.image)}")
        image_data = request.image
        prompt = "你是一位经验丰富的AI辅导老师..." # 省略详细prompt
        if request.type == "homework":
            prompt = """你是一位经验丰富的AI辅导老师，请仔细分析这张作业图片，进行智能批阅。返回结果必须严格遵循以下JSON格式：{"corrections": [{"question": "...", "student_answer": "...", "correct_answer": "...", "is_correct": false, "explanation": "...", "knowledge_points": ["..."]}], "overall_summary": "..."}"""
        else:
            prompt = """你是一位顶级的解题专家，请分析这张图片中的题目，并提供一个清晰、详尽的解答。返回结果必须严格遵循以下JSON格式：{"question_analysis": {"question": "...", "solution_steps": ["..."], "final_answer": "...", "knowledge_points_summary": "..."}}"""

        messages = [{"role": "user", "content": [{"image": image_data}, {"text": prompt}]}]
        
        print("📡 正在通过 Dashscope SDK 调用 qwen-vl-max API...")
        response = dashscope.MultiModalConversation.call(model='qwen-vl-max', messages=messages)
        
        if response.status_code == HTTPStatus.OK:
            print("✅ API 调用成功")
            ai_response_text = response.output.choices[0].message.content[0]['text']
            print(f"🤖 AI 原始回复: {ai_response_text[:300]}...")
            try:
                json_str = ai_response_text.split("```json")[1].split("```")[0].strip() if "```json" in ai_response_text else ai_response_text
                correction_result = json.loads(json_str)
                return {"success": True, "result": correction_result}
            except (json.JSONDecodeError, IndexError) as e:
                print(f"❌ AI响应JSON解析失败: {e}")
                return {"success": False, "result": {"error_summary": "AI响应不是有效的JSON格式。", "raw_response": ai_response_text}}
        else:
            error_msg = f"Dashscope API 调用失败: {response.code} - {response.message}"
            print(f"❌ {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_msg = f"服务器内部错误: {str(e)}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

# 文本生成接口 (保留)
async def call_tongyi_text_api(prompt: str):
    headers = {"Authorization": f"Bearer {TEXT_AI_CONFIG['api_key']}", "Content-Type": "application/json"}
    payload = {"model": TEXT_AI_CONFIG['model_name'], "input": {"messages": [{"role": "user", "content": prompt}]}, "parameters": {"result_format": "message"}}
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(TEXT_AI_CONFIG['api_endpoint'], headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            content = result["output"]["choices"][0]["message"]["content"]
            return {"success": True, "content": content}
        else:
            return {"success": False, "error": f"API Error: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/ai/generate-exercise")
async def generate_exercise(request_data: dict):
    try:
        subject, grade, q_type, q_count = request_data.get("subject", "数学"), request_data.get("grade", "一年级"), request_data.get("question_type", "选择题"), request_data.get("question_count", 5)
        prompt = f"请为{grade}学生生成{q_count}道{subject}{q_type}。请严格按照JSON格式返回..." # 省略详细prompt
        ai_result = await call_tongyi_text_api(prompt)
        if ai_result["success"]:
            ai_content = ai_result["content"].strip()
            json_str = ai_content.split("```json")[1].split("```")[0].strip() if "```json" in ai_content else ai_content
            ai_questions = json.loads(json_str)
            return {"success": True, "questions": ai_questions.get("questions", []), "ai_powered": True}
        else:
            raise Exception(ai_result["error"])
    except Exception as e:
        print(f"❌ AI题目生成失败，使用备用题目: {e}")
        return {"success": True, "questions": [{"content": "备用题：1+1=?", "answer": "2"}], "ai_powered": False}

if __name__ == "__main__":
    uvicorn.run("simple_app_vision:app", host="0.0.0.0", port=8000, reload=True)
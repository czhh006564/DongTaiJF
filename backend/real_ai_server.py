#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实的AI拍照批阅后端服务 - 使用Dashscope SDK
"""

import uvicorn
import json
import dashscope
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Union, Any

# --- 配置 ---
# 用户提供的API Key
DASHSCOPE_API_KEY = "sk-b98893a9f7274f64b3b3060771097aba"
dashscope.api_key = DASHSCOPE_API_KEY

# --- FastAPI 应用设置 ---
app = FastAPI(title="AI拍照批阅服务 (Dashscope SDK)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic 模型定义 ---
class PhotoCorrectionRequest(BaseModel):
    image: str  # base64编码的图片数据 (例如: "data:image/jpeg;base64,iVBORw0KGgo...")
    correction_type: str   # 批阅类型：homework 或 question

# --- API 端点 ---
@app.get("/")
async def root():
    return {"message": "AI拍照批阅服务运行正常", "model": "qwen-vl-max", "sdk": "dashscope"}

@app.get("/api/ai/test-connection")
async def test_connection():
    """使用Dashscope SDK测试AI模型连通性"""
    try:
        print("--- 正在测试 qwen-vl-max 连通性 (SDK) ---")
        messages = [{'role': 'user', 'content': [{'text': "你好，请回复'连接正常'以确认连接。"}]}]
        
        response = dashscope.MultiModalConversation.call(
            model='qwen-vl-max',
            messages=messages
        )

        if response.status_code == HTTPStatus.OK:
            print("✅ 连通性测试成功")
            return {
                "success": True,
                "status": "success",
                "message": "qwen-vl-max 模型连通正常 (SDK)",
                "model": "qwen-vl-max"
            }
        else:
            print(f"❌ 连通性测试失败: {response.code} - {response.message}")
            raise HTTPException(
                status_code=500, 
                detail=f"API返回错误: {response.code} - {response.message}"
            )
            
    except Exception as e:
        print(f"❌ 连通性测试异常: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"连接测试时发生异常: {str(e)}"
        )

@app.post("/api/ai/photo-correction")
async def photo_correction(request: PhotoCorrectionRequest):
    """使用Dashscope SDK进行AI拍照批阅"""
    try:
        print(f"📸 收到批阅请求, 类型: {request.correction_type}, 图片数据长度: {len(request.image)}")

        # Dashscope SDK可以直接处理带有 "data:image/jpeg;base64," 前缀的base64字符串
        # 无需手动去除
        image_data = request.image
        
        # 构建批阅提示词
        if request.correction_type == "homework":
            prompt = """你是一位经验丰富的AI辅导老师，请仔细分析这张作业图片，进行智能批阅。

你的任务是：
1.  **识别题目与答案**：准确识别图片中的每一道题目和学生写的答案。
2.  **判断对错**：清晰地判断每道题的正确性。
3.  **提供详尽解析**：对于错误的题目，必须提供详细的解题步骤、正确答案和易错点分析。对于正确的题目，给予鼓励。
4.  **总结知识点**：归纳本次作业考察的核心知识点。

返回结果必须严格遵循以下JSON格式，不要添加任何额外的解释或说明文字：
{
  "corrections": [
    {
      "question": "这里是识别出的题目内容",
      "student_answer": "这里是识别出的学生答案", 
      "correct_answer": "这里是该题的正确答案",
      "is_correct": false,
      "explanation": "这里是对错题的详细解析，或对正确题目的鼓励",
      "knowledge_points": ["知识点一", "知识点二"]
    }
  ],
  "overall_summary": "这里是对本次作业的总体评价和学习建议。"
}"""
        else: # request.correction_type == "question"
            prompt = """你是一位顶级的解题专家，请分析这张图片中的题目，并提供一个清晰、详尽的解答。

你的任务是：
1.  **识别题目**：准确识别图片中的问题。
2.  **分步解答**：提供完整、清晰的解题步骤。
3.  **给出最终答案**：明确展示最终的正确答案。
4.  **讲解核心知识点**：解释这道题所考察的关键概念和知识点。

返回结果必须严格遵循以下JSON格式，不要添加任何额外的解释或说明文字：
{
  "question_analysis": {
    "question": "这里是识别出的题目内容",
    "solution_steps": [
      "第一步：...",
      "第二步：...",
      "第三步：..."
    ],
    "final_answer": "这里是最终的正确答案",
    "knowledge_points_summary": "这里是对相关知识点的详细讲解。"
  }
}"""

        messages = [
            {
                "role": "user",
                "content": [
                    {"image": image_data},
                    {"text": prompt}
                ]
            }
        ]
        
        print("📡 正在通过 Dashscope SDK 调用 qwen-vl-max API...")
        response = dashscope.MultiModalConversation.call(
            model='qwen-vl-max',
            messages=messages
        )
        
        if response.status_code == HTTPStatus.OK:
            print("✅ API 调用成功")
            # 提取模型返回的文本内容
            ai_response_text = response.output.choices[0].message.content[0]['text']
            print(f"🤖 AI 原始回复: \n{ai_response_text}")
            
            # 尝试解析AI返回的JSON字符串
            try:
                # AI返回的文本可能被包裹在```json ... ```中，需要提取出来
                if "```json" in ai_response_text:
                    json_str = ai_response_text.split("```json")[1].split("```")[0].strip()
                else:
                    json_str = ai_response_text
                
                correction_result = json.loads(json_str)
                
                return {
                    "success": True,
                    "result": correction_result
                }
            except (json.JSONDecodeError, IndexError) as e:
                print(f"❌ AI响应JSON解析失败: {e}")
                print(f"   将返回原始文本作为应急方案。")
                # 如果解析失败，返回一个包含原始文本的应急结构
                fallback_result = {
                    "error_summary": "AI响应不是有效的JSON格式，已返回原始文本。",
                    "raw_response": ai_response_text
                }
                return {
                    "success": False, # 标记为半成功或失败，让前端知道这不是期望的格式
                    "result": fallback_result
                }

        else:
            error_msg = f"Dashscope API 调用失败: {response.code} - {response.message}"
            print(f"❌ {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)
            
    except Exception as e:
        error_msg = f"服务器内部错误: {str(e)}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    print("🚀 启动AI拍照批阅服务 (使用 Dashscope SDK)...")
    print(f"🔑 Dashscope API Key: ...{DASHSCOPE_API_KEY[-4:]}")
    print("🧠 使用模型: qwen-vl-max")
    print("🌐 服务地址: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
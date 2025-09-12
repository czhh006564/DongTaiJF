# 调试版后端 - 检查拍照批阅流程
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
import asyncio
import random
import httpx
import json

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 默认AI配置 - 通义千问视觉模型
DEFAULT_AI_CONFIG = {
    "provider": "tongyi",
    "api_key": "sk-b98893a9f7274f64b3b3060771097aba",
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    "model_name": "qwen-vl-max",
    "enabled": True
}

print(f"🤖 默认AI配置已加载: {DEFAULT_AI_CONFIG['provider']} - {DEFAULT_AI_CONFIG['model_name']}")

# 创建FastAPI应用
app = FastAPI(
    title="精准动态教辅系统 - 调试版",
    description="AI驱动的个性化教育辅助平台 - 调试拍照批阅",
    version="2.1.1"
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
    return {"message": "精准动态教辅系统 API - 调试版", "version": "2.1.1", "vision_model": DEFAULT_AI_CONFIG['model_name']}

# 简单的认证路由
@app.post("/auth/login")
async def login(request_data: dict = None):
    username = request_data.get("username", "student1") if request_data else "student1"
    return {
        "success": True,
        "access_token": "test_token",
        "token_type": "bearer",
        "user_info": {
            "id": 1,
            "username": username,
            "real_name": "测试学生",
            "role": "student",
            "email": f"{username}@test.com",
            "is_active": True
        },
        "message": "登录成功"
    }

# AI连通性测试接口
@app.get("/api/ai/test-connection")
async def test_ai_connection():
    """
    测试AI模型连通性
    """
    try:
        print(f"
🔍 ===== 开始AI连通性测试 =====")
        print(f"🤖 测试模型: {DEFAULT_AI_CONFIG['model_name']}")
        print(f"🔑 API Key: {DEFAULT_AI_CONFIG['api_key'][:20]}...")
        
        headers = {
            "Authorization": f"Bearer {DEFAULT_AI_CONFIG['api_key']}",
            "Content-Type": "application/json",
            "X-DashScope-SSE": "disable"
        }
        
        # 简单的文本测试请求
        payload = {
            "model": "qwen-plus",  # 使用文本模型进行连通性测试
            "input": {
                "messages": [
                    {
                        "role": "user", 
                        "content": "你好，请回复'连接正常'"
                    }
                ]
            },
            "parameters": {
                "result_format": "message",
                "max_tokens": 50
            }
        }
        
        print(f"📡 发送连通性测试请求...")
        
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0)
        ) as client:
            response = await client.post(
                "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
                headers=headers,
                json=payload
            )
            
            print(f"📡 连通性测试响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ AI连通性测试成功")
                print(f"📋 测试响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                
                return {
                    "success": True, 
                    "message": "qwen-vl-max模型连通正常",
                    "model": DEFAULT_AI_CONFIG['model_name'],
                    "status": "connected"
                }
            else:
                error_text = response.text
                print(f"❌ AI连通性测试失败: {response.status_code}")
                print(f"❌ 错误详情: {error_text}")
                return {
                    "success": False, 
                    "message": f"AI模型连通失败: {response.status_code} - {error_text}",
                    "status": "disconnected"
                }
                
    except Exception as e:
        print(f"❌ AI连通性测试异常: {str(e)}")
        import traceback
        print(f"❌ 异常堆栈: {traceback.format_exc()}")
        return {
            "success": False, 
            "message": f"连通性测试异常: {str(e)}",
            "status": "error"
        }

# 调用通义千问视觉API
async def call_tongyi_vision_api(prompt: str, image_url: str):
    """
    调用通义千问视觉API - 支持图像输入 (qwen-vl-max)
    """
    try:
        print(f"🔍 开始调用视觉API")
        print(f"📝 提示词长度: {len(prompt)}")
        print(f"🖼️ 图片数据长度: {len(image_url)}")
        print(f"🖼️ 图片数据类型: {type(image_url)}")
        print(f"🖼️ 图片数据开头: {str(image_url)[:50]}...")
        
        headers = {
            "Authorization": f"Bearer {DEFAULT_AI_CONFIG['api_key']}",
            "Content-Type": "application/json",
            "X-DashScope-SSE": "disable"
        }
        
        # 构建多模态消息
        content = [
            {
                "text": prompt
            },
            {
                "image": image_url
            }
        ]
        
        payload = {
            "model": DEFAULT_AI_CONFIG['model_name'],
            "input": {
                "messages": [
                    {
                        "role": "user", 
                        "content": content
                    }
                ]
            },
            "parameters": {
                "result_format": "message",
                "max_tokens": 2000,
                "temperature": 0.7
            }
        }
        
        print(f"🤖 调用通义千问视觉API: {DEFAULT_AI_CONFIG['api_endpoint']}")
        print(f"📝 使用模型: {DEFAULT_AI_CONFIG['model_name']}")
        print(f"🔑 API Key: {DEFAULT_AI_CONFIG['api_key'][:20]}...")
        
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(120.0, connect=15.0),
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
        ) as client:
            print(f"📡 发送请求到API...")
            response = await client.post(
                DEFAULT_AI_CONFIG['api_endpoint'],
                headers=headers,
                json=payload
            )
            
            print(f"📡 API响应状态码: {response.status_code}")
            print(f"📡 API响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📋 API响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
                
                if result.get("output") and result["output"].get("choices"):
                    content = result["output"]["choices"][0]["message"]["content"]
                    print(f"✅ 通义千问视觉API调用成功，生成内容长度: {len(content)}")
                    print(f"📝 生成内容预览: {content[:200]}...")
                    return {"success": True, "content": content}
                else:
                    print(f"❌ 通义千问视觉API返回格式异常: {result}")
                    return {"success": False, "error": "API返回格式异常"}
            else:
                error_text = response.text
                print(f"❌ 通义千问视觉API调用失败: {response.status_code}")
                print(f"❌ 错误详情: {error_text}")
                return {"success": False, "error": f"API调用失败: {response.status_code} - {error_text}"}
                
    except Exception as e:
        print(f"❌ 通义千问视觉API调用异常: {str(e)}")
        import traceback
        print(f"❌ 异常堆栈: {traceback.format_exc()}")
        return {"success": False, "error": str(e)}

# AI拍照批阅接口 - 调试版
@app.post("/api/ai/photo-correction")
async def photo_correction(request_data: dict):
    """
    AI拍照批阅功能 - 调试版
    """
    try:
        print(f"\n🔍 ===== 开始拍照批阅调试 =====")
        print(f"📥 收到请求数据: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
        
        image_data = request_data.get("image")
        correction_type = request_data.get("type", "homework")
        config = request_data.get("config", {})
        
        print(f"🔍 图片数据状态: {'存在' if image_data else '不存在'}")
        if image_data:
            print(f"🔍 图片数据类型: {type(image_data)}")
            print(f"🔍 图片数据长度: {len(image_data)}")
            print(f"🔍 图片数据开头: {str(image_data)[:100]}...")
        
        print(f"🔍 批阅类型: {correction_type}")
        print(f"🔍 配置信息: {config}")
        
        if not image_data:
            print(f"❌ 缺少图片数据")
            return {"success": False, "message": "缺少图片数据"}
        
        # 构建AI提示词
        subject = config.get("subject", "数学")
        grade = config.get("grade", "1年级")
        need_explanation = config.get("needExplanation", True)
        need_similar = config.get("needSimilarQuestions", False)
        
        print(f"🎯 批阅参数: {subject} {grade}, 需要解析: {need_explanation}, 需要相似题: {need_similar}")
        
        if correction_type == "homework":
            prompt = f"""请作为一名专业的{grade}{subject}老师，对学生上传的作业图片进行批阅。

批阅要求：
1. 仔细识别图片中的所有题目和学生答案
2. 判断每道题的正确性
3. 对错误的题目给出正确答案
4. 提供详细的解题步骤和解析
5. 分析错误原因并给出学习建议

请按照以下JSON格式返回结果：
{{
    "accuracy": 85,
    "score": 85,
    "totalScore": 100,
    "questions": [
        {{
            "content": "题目内容",
            "studentAnswer": "学生的答案",
            "correctAnswer": "正确答案",
            "isCorrect": true,
            "explanation": "详细解析",
            "errorAnalysis": "错误分析",
            "suggestion": "学习建议",
            "knowledgePoint": "考查的知识点"
        }}
    ],
    "similarQuestions": [
        {{
            "content": "相似题目内容",
            "answer": "答案"
        }}
    ],
    "overallComment": "总体评价和建议"
}}

请仔细观察图片内容，识别其中的题目和答案，然后按照上述格式返回批阅结果。"""
        else:
            prompt = f"""请作为一名专业的{grade}{subject}老师，对学生上传的题目图片进行解答。

解答要求：
1. 仔细识别图片中的题目内容
2. 提供详细的解答步骤
3. 给出最终答案

请按照以下JSON格式返回结果：
{{
    "questions": [
        {{
            "content": "题目内容",
            "solution": "详细解答过程",
            "answer": "最终答案",
            "explanation": "解题思路和方法",
            "keyPoints": "关键知识点"
        }}
    ]
}}

请仔细观察图片内容，识别其中的题目，然后按照上述格式返回解答结果。"""
        
        print(f"📝 构建的提示词长度: {len(prompt)}")
        print(f"📝 提示词内容: {prompt[:200]}...")
        
        # 检查图片数据格式
        if not str(image_data).startswith('data:image'):
            print(f"❌ 图片数据格式不正确，不是data:image格式")
            return {"success": False, "message": "图片数据格式不正确"}
        
        print(f"🖼️ 开始调用qwen-vl-max模型...")
        
        # 调用通义千问视觉API
        ai_result = await call_tongyi_vision_api(prompt, image_data)
        
        print(f"🤖 AI调用结果: {ai_result}")
        
        if ai_result["success"]:
            print(f"✅ AI调用成功，开始解析返回内容...")
            try:
                ai_content = ai_result["content"].strip()
                print(f"📝 AI返回内容: {ai_content}")
                
                # 尝试提取JSON部分
                if "```json" in ai_content:
                    json_start = ai_content.find("```json") + 7
                    json_end = ai_content.find("```", json_start)
                    ai_content = ai_content[json_start:json_end].strip()
                    print(f"📝 提取的JSON内容: {ai_content}")
                elif "{" in ai_content:
                    json_start = ai_content.find("{")
                    json_end = ai_content.rfind("}") + 1
                    ai_content = ai_content[json_start:json_end]
                    print(f"📝 提取的JSON内容: {ai_content}")
                
                result = json.loads(ai_content)
                print(f"✅ JSON解析成功: {result}")
                return {"success": True, "result": result}
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"❌ 原始内容: {ai_result['content']}")
                return {"success": False, "message": f"AI返回内容解析失败: {str(e)}"}
        else:
            print(f"❌ AI调用失败: {ai_result['error']}")
            return {"success": False, "message": f"AI调用失败: {ai_result['error']}"}
            
    except Exception as e:
        print(f"❌ 拍照批阅接口异常: {str(e)}")
        import traceback
        print(f"❌ 异常堆栈: {traceback.format_exc()}")
        return {"success": False, "message": f"批阅失败: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run("debug_app:app", host="0.0.0.0", port=8000, reload=True)
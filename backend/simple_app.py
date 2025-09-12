# 简化版应用启动文件
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

# 默认AI配置 - 通义千问
DEFAULT_AI_CONFIG = {
    "provider": "tongyi",
    "api_key": "sk-b98893a9f7274f64b3b3060771097aba",
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
    "model_name": "qwen-plus",
    "enabled": True
}

print(f"🤖 默认AI配置已加载: {DEFAULT_AI_CONFIG['provider']} - {DEFAULT_AI_CONFIG['model_name']}")

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

# 测试通义千问API连接
@app.post("/api/test-tongyi")
async def test_tongyi_connection():
    """
    测试通义千问API连接
    """
    try:
        test_prompt = "请回答：1+1等于多少？"
        result = await call_tongyi_api(test_prompt)
        
        if result["success"]:
            return {
                "success": True,
                "message": "通义千问API连接正常",
                "response": result["content"][:100] + "..." if len(result["content"]) > 100 else result["content"]
            }
        else:
            return {
                "success": False,
                "message": "通义千问API连接失败",
                "error": result["error"]
            }
    except Exception as e:
        return {
            "success": False,
            "message": "测试过程中发生异常",
            "error": str(e)
        }

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

# 调用通义千问API生成题目
async def call_tongyi_api(prompt: str):
    """
    调用通义千问API - 修正版本
    """
    try:
        # 通义千问API的正确请求头格式
        headers = {
            "Authorization": f"Bearer {DEFAULT_AI_CONFIG['api_key']}",
            "Content-Type": "application/json",
            "X-DashScope-SSE": "disable"
        }
        
        # 通义千问API的正确请求体格式
        payload = {
            "model": DEFAULT_AI_CONFIG['model_name'],
            "input": {
                "messages": [
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
            },
            "parameters": {
                "result_format": "message",
                "incremental_output": False,
                "max_tokens": 2000,
                "temperature": 0.7
            }
        }
        
        print(f"🤖 调用通义千问API: {DEFAULT_AI_CONFIG['api_endpoint']}")
        print(f"🔑 使用API Key: {DEFAULT_AI_CONFIG['api_key'][:20]}...")
        print(f"📝 请求模型: {DEFAULT_AI_CONFIG['model_name']}")
        
        # 增加超时时间和重试机制
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(60.0, connect=10.0),
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
        ) as client:
            response = await client.post(
                DEFAULT_AI_CONFIG['api_endpoint'],
                headers=headers,
                json=payload
            )
            
            print(f"📡 API响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📋 API响应内容: {result}")
                
                if result.get("output") and result["output"].get("choices"):
                    content = result["output"]["choices"][0]["message"]["content"]
                    print(f"✅ 通义千问API调用成功，生成内容长度: {len(content)}")
                    return {"success": True, "content": content}
                else:
                    print(f"❌ 通义千问API返回格式异常: {result}")
                    return {"success": False, "error": "API返回格式异常"}
            else:
                error_text = response.text
                print(f"❌ 通义千问API调用失败: {response.status_code}")
                print(f"❌ 错误详情: {error_text}")
                return {"success": False, "error": f"API调用失败: {response.status_code} - {error_text}"}
                
    except httpx.TimeoutException as e:
        print(f"❌ 通义千问API调用超时: {str(e)}")
        return {"success": False, "error": f"API调用超时: {str(e)}"}
    except httpx.ConnectError as e:
        print(f"❌ 通义千问API连接错误: {str(e)}")
        return {"success": False, "error": f"API连接错误: {str(e)}"}
    except Exception as e:
        print(f"❌ 通义千问API调用异常: {str(e)}")
        return {"success": False, "error": str(e)}

# AI题目生成端点
@app.post("/api/ai/generate-exercise")
async def generate_exercise(request_data: dict):
    """
    AI题目生成接口
    """
    try:
        # 获取请求参数
        subject = request_data.get("subject", "数学")
        grade = request_data.get("grade", "1年级")
        question_type = request_data.get("question_type", "choice")
        question_count = request_data.get("question_count", 5)
        knowledge_points = request_data.get("knowledge_points", [])
        difficulty_level = request_data.get("difficulty_level", 1)
        
        print(f"🎯 收到题目生成请求: {subject} {grade} {question_type} 共{question_count}题")
        
        # 根据题型构建不同的AI提示词
        type_descriptions = {
            'choice': '选择题',
            'fill': '填空题', 
            'solve': '解答题',
            'mixed': '混合题型（包含选择题、填空题、解答题）'
        }
        
        type_name = type_descriptions.get(question_type, '选择题')
        
        if question_type == 'choice':
            prompt = f"""请为{grade}学生生成{question_count}道{subject}选择题。

要求：
1. 题目难度适合{grade}学生
2. 每道题包含4个选项（A、B、C、D）
3. 题目内容要准确、有教育意义
4. 请严格按照以下JSON格式返回：

{{
  "questions": [
    {{
      "content": "题目内容",
      "options": ["选项A内容", "选项B内容", "选项C内容", "选项D内容"],
      "answer": "正确答案（A/B/C/D）",
      "explanation": "题目解析"
    }}
  ]
}}

请直接返回JSON格式，不要包含其他文字说明。"""

        elif question_type == 'fill':
            prompt = f"""请为{grade}学生生成{question_count}道{subject}填空题。

要求：
1. 题目难度适合{grade}学生
2. 题目中用"____"表示需要填空的地方
3. 题目内容要准确、有教育意义
4. 请严格按照以下JSON格式返回：

{{
  "questions": [
    {{
      "content": "题目内容（用____表示填空）",
      "answer": "正确答案",
      "explanation": "题目解析"
    }}
  ]
}}

请直接返回JSON格式，不要包含其他文字说明。"""

        elif question_type == 'solve':
            prompt = f"""请为{grade}学生生成{question_count}道{subject}解答题。

要求：
1. 题目难度适合{grade}学生
2. 题目需要学生写出详细解答过程
3. 题目内容要准确、有教育意义
4. 请严格按照以下JSON格式返回：

{{
  "questions": [
    {{
      "content": "题目内容",
      "answer": "标准答案或解答要点",
      "explanation": "详细解答过程"
    }}
  ]
}}

请直接返回JSON格式，不要包含其他文字说明。"""

        else:  # mixed
            prompt = f"""请为{grade}学生生成{question_count}道{subject}混合题型。

要求：
1. 题目难度适合{grade}学生
2. 包含选择题、填空题、解答题等不同类型
3. 选择题包含4个选项（A、B、C、D）
4. 填空题用"____"表示填空位置
5. 解答题需要详细解答过程
6. 请严格按照以下JSON格式返回：

{{
  "questions": [
    {{
      "type": "choice|fill|solve",
      "content": "题目内容",
      "options": ["选项A", "选项B", "选项C", "选项D"],
      "answer": "正确答案",
      "explanation": "题目解析"
    }}
  ]
}}

注意：选择题必须有options字段，填空题和解答题不需要options字段。
请直接返回JSON格式，不要包含其他文字说明。"""

        # 尝试调用AI API
        ai_result = await call_tongyi_api(prompt)
        
        if ai_result["success"]:
            try:
                # 解析AI返回的JSON
                ai_content = ai_result["content"].strip()
                
                # 尝试提取JSON部分
                if "```json" in ai_content:
                    json_start = ai_content.find("```json") + 7
                    json_end = ai_content.find("```", json_start)
                    ai_content = ai_content[json_start:json_end].strip()
                elif "{" in ai_content:
                    json_start = ai_content.find("{")
                    json_end = ai_content.rfind("}") + 1
                    ai_content = ai_content[json_start:json_end]
                
                ai_questions = json.loads(ai_content)
                
                if "questions" in ai_questions and ai_questions["questions"]:
                    questions = []
                    for q in ai_questions["questions"][:question_count]:
                        # 根据题型处理不同的返回格式
                        question_data = {
                            "content": q.get("content", "AI生成的题目"),
                            "answer": q.get("answer", "A"),
                            "explanation": q.get("explanation", "AI生成的解析"),
                            "knowledge_point": f"{grade}{subject}",
                            "difficulty": difficulty_level
                        }
                        
                        # 处理混合题型中的type字段
                        if question_type == 'mixed' and 'type' in q:
                            question_data['type'] = q['type']
                        else:
                            question_data['type'] = question_type
                        
                        # 只有选择题才需要options字段
                        if question_data['type'] == 'choice' or (question_type == 'choice'):
                            question_data["options"] = q.get("options", ["选项A", "选项B", "选项C", "选项D"])
                        
                        questions.append(question_data)
                    
                    print(f"✅ AI成功生成 {len(questions)} 道{subject}题目")
                    
                    return {
                        "success": True,
                        "questions": questions,
                        "total_count": len(questions),
                        "subject": subject,
                        "grade": grade,
                        "message": f"AI成功生成{len(questions)}道{subject}题目",
                        "ai_powered": True
                    }
                else:
                    raise ValueError("AI返回的JSON格式不正确")
                    
            except json.JSONDecodeError as e:
                print(f"❌ AI返回内容JSON解析失败: {e}")
                print(f"AI返回内容: {ai_result['content']}")
                raise Exception("AI返回内容格式错误")
        else:
            raise Exception(f"AI调用失败: {ai_result['error']}")
            
    except Exception as e:
        print(f"❌ AI题目生成失败，使用备用题目: {str(e)}")
        
        # AI失败时使用备用题目
        try:
            questions = []
            
            # 根据题型生成不同类型的备用题目
            if subject == "数学":
                if question_type == 'choice':
                    math_questions = [
                        {
                            "type": "choice",
                            "content": "计算：5 + 3 = ?",
                            "options": ["6", "7", "8", "9"],
                            "answer": "8",
                            "explanation": "这是一道基础加法运算题：5 + 3 = 8。",
                            "knowledge_point": f"{grade}数学基础运算",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "choice",
                            "content": "计算：10 - 4 = ?",
                            "options": ["5", "6", "7", "8"],
                            "answer": "6",
                            "explanation": "这是一道基础减法运算题：10 - 4 = 6。",
                            "knowledge_point": f"{grade}数学基础运算",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "choice",
                            "content": "计算：3 × 4 = ?",
                            "options": ["10", "11", "12", "13"],
                            "answer": "12",
                            "explanation": "这是一道基础乘法运算题：3 × 4 = 12。",
                            "knowledge_point": f"{grade}数学乘法运算",
                            "difficulty": difficulty_level
                        }
                    ]
                elif question_type == 'fill':
                    math_questions = [
                        {
                            "type": "fill",
                            "content": "5 + 3 = ____",
                            "answer": "8",
                            "explanation": "这是一道基础加法运算题：5 + 3 = 8。",
                            "knowledge_point": f"{grade}数学基础运算",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "fill",
                            "content": "10 - ____ = 6",
                            "answer": "4",
                            "explanation": "这是一道基础减法运算题：10 - 4 = 6。",
                            "knowledge_point": f"{grade}数学基础运算",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "fill",
                            "content": "3 × 4 = ____",
                            "answer": "12",
                            "explanation": "这是一道基础乘法运算题：3 × 4 = 12。",
                            "knowledge_point": f"{grade}数学乘法运算",
                            "difficulty": difficulty_level
                        }
                    ]
                elif question_type == 'solve':
                    math_questions = [
                        {
                            "type": "solve",
                            "content": "小明有5个苹果，妈妈又给了他3个苹果，请问小明现在一共有多少个苹果？",
                            "answer": "8个苹果",
                            "explanation": "解：小明原有5个苹果，妈妈又给了3个苹果，所以总数为：5 + 3 = 8个苹果。",
                            "knowledge_point": f"{grade}数学应用题",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "solve",
                            "content": "一个长方形的长是6厘米，宽是4厘米，求这个长方形的面积。",
                            "answer": "24平方厘米",
                            "explanation": "解：长方形面积 = 长 × 宽 = 6 × 4 = 24平方厘米。",
                            "knowledge_point": f"{grade}数学几何",
                            "difficulty": difficulty_level
                        }
                    ]
                else:  # mixed
                    math_questions = [
                        {
                            "type": "choice",
                            "content": "计算：5 + 3 = ?",
                            "options": ["6", "7", "8", "9"],
                            "answer": "8",
                            "explanation": "这是一道基础加法运算题：5 + 3 = 8。",
                            "knowledge_point": f"{grade}数学基础运算",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "fill",
                            "content": "10 - ____ = 6",
                            "answer": "4",
                            "explanation": "这是一道基础减法运算题：10 - 4 = 6。",
                            "knowledge_point": f"{grade}数学基础运算",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "solve",
                            "content": "小明有5个苹果，妈妈又给了他3个苹果，请问小明现在一共有多少个苹果？",
                            "answer": "8个苹果",
                            "explanation": "解：小明原有5个苹果，妈妈又给了3个苹果，所以总数为：5 + 3 = 8个苹果。",
                            "knowledge_point": f"{grade}数学应用题",
                            "difficulty": difficulty_level
                        }
                    ]
                questions = math_questions[:question_count]
                
            elif subject == "语文":
                if question_type == 'choice':
                    chinese_questions = [
                        {
                            "type": "choice",
                            "content": "下列词语中，哪个是形容词？",
                            "options": ["跑步", "美丽", "吃饭", "睡觉"],
                            "answer": "美丽",
                            "explanation": "形容词是用来描述事物性质、状态的词语，'美丽'描述外观，是形容词。",
                            "knowledge_point": f"{grade}语文词性识别",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "choice",
                            "content": "\"春眠不觉晓\"的下一句是？",
                            "options": ["处处闻啼鸟", "夜来风雨声", "花落知多少", "红掌拨清波"],
                            "answer": "处处闻啼鸟",
                            "explanation": "这是孟浩然《春晓》中的诗句，表达了春天早晨的美好景象。",
                            "knowledge_point": f"{grade}语文古诗词",
                            "difficulty": difficulty_level
                        }
                    ]
                elif question_type == 'fill':
                    chinese_questions = [
                        {
                            "type": "fill",
                            "content": "春眠不觉晓，____闻啼鸟。",
                            "answer": "处处",
                            "explanation": "这是孟浩然《春晓》中的诗句：春眠不觉晓，处处闻啼鸟。",
                            "knowledge_point": f"{grade}语文古诗词",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "fill",
                            "content": "____是用来描述事物性质、状态的词语。",
                            "answer": "形容词",
                            "explanation": "形容词是用来描述事物性质、状态的词语。",
                            "knowledge_point": f"{grade}语文词性识别",
                            "difficulty": difficulty_level
                        }
                    ]
                elif question_type == 'solve':
                    chinese_questions = [
                        {
                            "type": "solve",
                            "content": "请背诵孟浩然的《春晓》全诗，并说明这首诗表达了什么意思？",
                            "answer": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。这首诗表达了诗人对春天美好景象的喜爱和对时光流逝的感慨。",
                            "explanation": "《春晓》描写了春天早晨的美好景象，表达了诗人对春天的喜爱之情。",
                            "knowledge_point": f"{grade}语文古诗词",
                            "difficulty": difficulty_level
                        }
                    ]
                else:  # mixed
                    chinese_questions = [
                        {
                            "type": "choice",
                            "content": "下列词语中，哪个是形容词？",
                            "options": ["跑步", "美丽", "吃饭", "睡觉"],
                            "answer": "美丽",
                            "explanation": "形容词是用来描述事物性质、状态的词语，'美丽'描述外观，是形容词。",
                            "knowledge_point": f"{grade}语文词性识别",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "fill",
                            "content": "春眠不觉晓，____闻啼鸟。",
                            "answer": "处处",
                            "explanation": "这是孟浩然《春晓》中的诗句：春眠不觉晓，处处闻啼鸟。",
                            "knowledge_point": f"{grade}语文古诗词",
                            "difficulty": difficulty_level
                        }
                    ]
                questions = chinese_questions[:question_count]
                
            elif subject == "英语":
                if question_type == 'choice':
                    english_questions = [
                        {
                            "type": "choice",
                            "content": "\"Hello\" 的中文意思是？",
                            "options": ["再见", "你好", "谢谢", "对不起"],
                            "answer": "你好",
                            "explanation": "'Hello'是英语中最常用的问候语，意思是'你好'。",
                            "knowledge_point": f"{grade}英语基础词汇",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "choice",
                            "content": "下列哪个是颜色单词？",
                            "options": ["cat", "red", "run", "book"],
                            "answer": "red",
                            "explanation": "'red'表示红色，是颜色类单词。",
                            "knowledge_point": f"{grade}英语颜色词汇",
                            "difficulty": difficulty_level
                        }
                    ]
                elif question_type == 'fill':
                    english_questions = [
                        {
                            "type": "fill",
                            "content": "\"____\" 的中文意思是'你好'。",
                            "answer": "Hello",
                            "explanation": "'Hello'是英语中最常用的问候语，意思是'你好'。",
                            "knowledge_point": f"{grade}英语基础词汇",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "fill",
                            "content": "苹果的英文单词是 ____。",
                            "answer": "apple",
                            "explanation": "'apple'是水果类单词，中文意思是苹果。",
                            "knowledge_point": f"{grade}英语水果词汇",
                            "difficulty": difficulty_level
                        }
                    ]
                elif question_type == 'solve':
                    english_questions = [
                        {
                            "type": "solve",
                            "content": "请用英语介绍你自己，包括姓名、年龄和爱好。（至少3句话）",
                            "answer": "My name is... I am ... years old. I like...",
                            "explanation": "英语自我介绍的基本句型：My name is + 姓名，I am + 年龄 + years old，I like + 爱好。",
                            "knowledge_point": f"{grade}英语口语表达",
                            "difficulty": difficulty_level
                        }
                    ]
                else:  # mixed
                    english_questions = [
                        {
                            "type": "choice",
                            "content": "\"Hello\" 的中文意思是？",
                            "options": ["再见", "你好", "谢谢", "对不起"],
                            "answer": "你好",
                            "explanation": "'Hello'是英语中最常用的问候语，意思是'你好'。",
                            "knowledge_point": f"{grade}英语基础词汇",
                            "difficulty": difficulty_level
                        },
                        {
                            "type": "fill",
                            "content": "苹果的英文单词是 ____。",
                            "answer": "apple",
                            "explanation": "'apple'是水果类单词，中文意思是苹果。",
                            "knowledge_point": f"{grade}英语水果词汇",
                            "difficulty": difficulty_level
                        }
                    ]
                questions = english_questions[:question_count]
            
            # 确保生成足够数量的题目
            while len(questions) < question_count:
                questions.extend(questions[:question_count - len(questions)])
            
            questions = questions[:question_count]
            
            print(f"✅ 使用备用题目生成 {len(questions)} 道{subject}题目")
            
            return {
                "success": True,
                "questions": questions,
                "total_count": len(questions),
                "subject": subject,
                "grade": grade,
                "message": f"使用备用题目生成{len(questions)}道{subject}题目",
                "ai_powered": False
            }
            
        except Exception as fallback_error:
            print(f"❌ 备用题目生成也失败: {str(fallback_error)}")
            return {
                "success": False,
                "error": str(fallback_error),
                "message": "题目生成失败，请稍后重试"
            }

if __name__ == "__main__":
    uvicorn.run("simple_app:app", host="0.0.0.0", port=8000, reload=True)
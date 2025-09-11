import json
import time
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from database.models import AIModelConfig, AICallLog, User
import logging

logger = logging.getLogger(__name__)

class AIService:
    """AI服务类，支持多种AI模型"""
    
    def __init__(self, db: Session):
        self.db = db
        self.session = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    def get_default_model(self) -> Optional[AIModelConfig]:
        """获取默认AI模型配置"""
        return self.db.query(AIModelConfig).filter(
            AIModelConfig.is_default == True,
            AIModelConfig.is_active == True
        ).first()
    
    def get_model_by_name(self, model_name: str) -> Optional[AIModelConfig]:
        """根据名称获取AI模型配置"""
        return self.db.query(AIModelConfig).filter(
            AIModelConfig.model_name == model_name,
            AIModelConfig.is_active == True
        ).first()
    
    async def call_tongyi_api(self, model_config: AIModelConfig, messages: List[Dict], 
                             function_type: str, user_id: int) -> Dict[str, Any]:
        """调用通义千问API"""
        start_time = time.time()
        
        try:
            # 解密API密钥
            api_key = decrypt_api_key(model_config.api_key)
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": "qwen-turbo",  # 或其他通义千问模型
                "input": {
                    "messages": messages
                },
                "parameters": {
                    "max_tokens": model_config.max_tokens,
                    "temperature": model_config.temperature,
                    **model_config.model_params if model_config.model_params else {}
                }
            }
            
            async with self.session.post(
                model_config.api_endpoint,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    result = await response.json()
                    
                    # 记录调用日志
                    await self._log_api_call(
                        user_id=user_id,
                        model_name=model_config.model_name,
                        function_type=function_type,
                        prompt_tokens=result.get('usage', {}).get('input_tokens', 0),
                        completion_tokens=result.get('usage', {}).get('output_tokens', 0),
                        total_tokens=result.get('usage', {}).get('total_tokens', 0),
                        response_time=response_time,
                        success=True
                    )
                    
                    return {
                        'success': True,
                        'content': result['output']['text'],
                        'usage': result.get('usage', {}),
                        'response_time': response_time
                    }
                else:
                    error_text = await response.text()
                    await self._log_api_call(
                        user_id=user_id,
                        model_name=model_config.model_name,
                        function_type=function_type,
                        response_time=response_time,
                        success=False,
                        error_message=f"HTTP {response.status}: {error_text}"
                    )
                    
                    return {
                        'success': False,
                        'error': f"API调用失败: HTTP {response.status}",
                        'details': error_text
                    }
                    
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = str(e)
            
            await self._log_api_call(
                user_id=user_id,
                model_name=model_config.model_name,
                function_type=function_type,
                response_time=response_time,
                success=False,
                error_message=error_msg
            )
            
            logger.error(f"通义千问API调用异常: {error_msg}")
            return {
                'success': False,
                'error': f"API调用异常: {error_msg}"
            }
    
    async def call_deepseek_api(self, model_config: AIModelConfig, messages: List[Dict], 
                               function_type: str, user_id: int) -> Dict[str, Any]:
        """调用DeepSeek API"""
        start_time = time.time()
        
        try:
            # 解密API密钥
            api_key = decrypt_api_key(model_config.api_key)
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": messages,
                "max_tokens": model_config.max_tokens,
                "temperature": model_config.temperature,
                **model_config.model_params if model_config.model_params else {}
            }
            
            async with self.session.post(
                model_config.api_endpoint,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    result = await response.json()
                    
                    # 记录调用日志
                    await self._log_api_call(
                        user_id=user_id,
                        model_name=model_config.model_name,
                        function_type=function_type,
                        prompt_tokens=result.get('usage', {}).get('prompt_tokens', 0),
                        completion_tokens=result.get('usage', {}).get('completion_tokens', 0),
                        total_tokens=result.get('usage', {}).get('total_tokens', 0),
                        response_time=response_time,
                        success=True
                    )
                    
                    return {
                        'success': True,
                        'content': result['choices'][0]['message']['content'],
                        'usage': result.get('usage', {}),
                        'response_time': response_time
                    }
                else:
                    error_text = await response.text()
                    await self._log_api_call(
                        user_id=user_id,
                        model_name=model_config.model_name,
                        function_type=function_type,
                        response_time=response_time,
                        success=False,
                        error_message=f"HTTP {response.status}: {error_text}"
                    )
                    
                    return {
                        'success': False,
                        'error': f"API调用失败: HTTP {response.status}",
                        'details': error_text
                    }
                    
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = str(e)
            
            await self._log_api_call(
                user_id=user_id,
                model_name=model_config.model_name,
                function_type=function_type,
                response_time=response_time,
                success=False,
                error_message=error_msg
            )
            
            logger.error(f"DeepSeek API调用异常: {error_msg}")
            return {
                'success': False,
                'error': f"API调用异常: {error_msg}"
            }
    
    async def call_ai_model(self, messages: List[Dict], function_type: str, 
                           user_id: int, model_name: Optional[str] = None) -> Dict[str, Any]:
        """统一的AI模型调用接口"""
        
        # 获取模型配置
        if model_name:
            model_config = self.get_model_by_name(model_name)
        else:
            model_config = self.get_default_model()
        
        if not model_config:
            return {
                'success': False,
                'error': '未找到可用的AI模型配置'
            }
        
        # 根据模型类型调用相应的API
        if model_config.model_name == 'tongyi':
            return await self.call_tongyi_api(model_config, messages, function_type, user_id)
        elif model_config.model_name == 'deepseek':
            return await self.call_deepseek_api(model_config, messages, function_type, user_id)
        else:
            return {
                'success': False,
                'error': f'不支持的模型类型: {model_config.model_name}'
            }
    
    async def generate_exercise_questions(self, user_id: int, subject: str, 
                                        knowledge_points: List[str], question_type: str, 
                                        question_count: int, difficulty_level: int = 1) -> Dict[str, Any]:
        """生成练习题目"""
        
        # 构建提示词
        prompt = self._build_exercise_prompt(
            subject, knowledge_points, question_type, question_count, difficulty_level
        )
        
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的教育AI助手，擅长根据学生的学习情况生成个性化的练习题目。请严格按照要求的格式输出题目。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        return await self.call_ai_model(messages, "generate_exercise", user_id)
    
    async def generate_answer_analysis(self, user_id: int, questions: List[Dict]) -> Dict[str, Any]:
        """生成答案解析"""
        
        prompt = self._build_analysis_prompt(questions)
        
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的教育AI助手，擅长为题目提供详细的答案解析和解题思路。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        return await self.call_ai_model(messages, "generate_analysis", user_id)
    
    async def analyze_error_patterns(self, user_id: int, error_records: List[Dict]) -> Dict[str, Any]:
        """分析错题模式"""
        
        prompt = self._build_error_analysis_prompt(error_records)
        
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的教育数据分析师，擅长分析学生的错题模式并提供学习建议。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        return await self.call_ai_model(messages, "analyze_errors", user_id)
    
    def _build_exercise_prompt(self, subject: str, knowledge_points: List[str], 
                              question_type: str, question_count: int, difficulty_level: int) -> str:
        """构建题目生成提示词"""
        
        type_map = {
            'choice': '选择题',
            'fill': '填空题',
            'solve': '解答题',
            'mixed': '混合题型'
        }
        
        difficulty_map = {
            1: '基础',
            2: '简单',
            3: '中等',
            4: '困难',
            5: '挑战'
        }
        
        prompt = f"""
请为{subject}学科生成{question_count}道{type_map.get(question_type, question_type)}，难度等级为{difficulty_map.get(difficulty_level, '中等')}。

涉及知识点：{', '.join(knowledge_points)}

要求：
1. 题目要有针对性，符合指定的知识点
2. 难度适中，符合指定的难度等级
3. 题目表述清晰，无歧义
4. 如果是选择题，提供4个选项（A、B、C、D）
5. 如果是填空题，用下划线表示空白处
6. 如果是解答题，要求有明确的解题步骤

请按照以下JSON格式输出：
{{
    "questions": [
        {{
            "id": 1,
            "type": "{question_type}",
            "content": "题目内容",
            "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],  // 仅选择题需要
            "answer": "正确答案",
            "knowledge_point": "主要知识点",
            "difficulty": {difficulty_level}
        }}
    ]
}}
"""
        return prompt
    
    def _build_analysis_prompt(self, questions: List[Dict]) -> str:
        """构建答案解析提示词"""
        
        questions_text = ""
        for i, q in enumerate(questions, 1):
            questions_text += f"\n{i}. {q.get('content', '')}"
            if q.get('options'):
                for option in q['options']:
                    questions_text += f"\n   {option}"
        
        prompt = f"""
请为以下题目提供详细的答案解析：

{questions_text}

对每道题目，请提供：
1. 标准答案
2. 详细的解题步骤
3. 涉及的知识点说明
4. 易错点提醒
5. 解题技巧

请按照以下JSON格式输出：
{{
    "analyses": [
        {{
            "question_id": 1,
            "answer": "标准答案",
            "steps": ["步骤1", "步骤2", "步骤3"],
            "knowledge_points": ["知识点1", "知识点2"],
            "common_mistakes": ["易错点1", "易错点2"],
            "tips": "解题技巧"
        }}
    ]
}}
"""
        return prompt
    
    def _build_error_analysis_prompt(self, error_records: List[Dict]) -> str:
        """构建错题分析提示词"""
        
        records_text = ""
        for record in error_records:
            records_text += f"\n- {record.get('subject', '')}: {record.get('knowledge_point', '')} (错误{record.get('error_count', 1)}次)"
        
        prompt = f"""
请分析以下学生的错题记录，识别学习模式和薄弱环节：

错题记录：{records_text}

请提供：
1. 薄弱知识点分析
2. 错题模式识别
3. 学习建议
4. 重点练习方向

请按照以下JSON格式输出：
{{
    "weak_points": ["薄弱知识点1", "薄弱知识点2"],
    "error_patterns": ["错题模式1", "错题模式2"],
    "suggestions": ["建议1", "建议2", "建议3"],
    "focus_areas": ["重点练习方向1", "重点练习方向2"]
}}
"""
        return prompt
    
    async def _log_api_call(self, user_id: int, model_name: str, function_type: str,
                           response_time: float, success: bool, prompt_tokens: int = 0,
                           completion_tokens: int = 0, total_tokens: int = 0,
                           error_message: str = None):
        """记录API调用日志"""
        
        log_entry = AICallLog(
            user_id=user_id,
            model_name=model_name,
            function_type=function_type,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            response_time=response_time,
            success=success,
            error_message=error_message
        )
        
        self.db.add(log_entry)
        self.db.commit()


# AI服务管理类
class AIServiceManager:
    """AI服务管理器"""
    
    @staticmethod
    def initialize_default_models(db: Session):
        """初始化默认AI模型配置"""
        
        # 检查是否已有配置
        existing_config = db.query(AIModelConfig).first()
        if existing_config:
            return
        
        # 创建通义千问默认配置
        tongyi_config = AIModelConfig(
            model_name="tongyi",
            display_name="通义千问",
            api_endpoint="https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            api_key=encrypt_api_key("your-tongyi-api-key"),  # 需要用户配置
            model_params={
                "result_format": "text"
            },
            is_active=False,  # 默认不激活，需要用户配置API密钥后激活
            is_default=True,
            max_tokens=2000,
            temperature=0.7
        )
        
        # 创建DeepSeek配置
        deepseek_config = AIModelConfig(
            model_name="deepseek",
            display_name="DeepSeek",
            api_endpoint="https://api.deepseek.com/v1/chat/completions",
            api_key=encrypt_api_key("your-deepseek-api-key"),  # 需要用户配置
            model_params={},
            is_active=False,
            is_default=False,
            max_tokens=2000,
            temperature=0.7
        )
        
        db.add(tongyi_config)
        db.add(deepseek_config)
        db.commit()
        
        logger.info("默认AI模型配置已初始化")
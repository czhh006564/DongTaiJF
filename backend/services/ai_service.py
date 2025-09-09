# AI服务层
import requests
import json
import os
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from ..models import AIModelConfig, ErrorRecord

class AIService:
    def __init__(self, db: Session):
        self.db = db
        self.default_model = self._get_default_model()
    
    def _get_default_model(self) -> Optional[AIModelConfig]:
        """获取默认AI模型配置"""
        return self.db.query(AIModelConfig).filter(
            AIModelConfig.is_default == True,
            AIModelConfig.is_active == True
        ).first()
    
    def _get_model_by_name(self, model_name: str) -> Optional[AIModelConfig]:
        """根据名称获取AI模型配置"""
        return self.db.query(AIModelConfig).filter(
            AIModelConfig.model_name == model_name,
            AIModelConfig.is_active == True
        ).first()
    
    async def call_ai_model(
        self, 
        prompt: str, 
        model_name: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Dict:
        """调用AI模型"""
        try:
            # 选择模型
            if model_name:
                model_config = self._get_model_by_name(model_name)
            else:
                model_config = self.default_model
            
            if not model_config:
                raise Exception("没有可用的AI模型配置")
            
            # 准备请求参数
            headers = {
                "Authorization": f"Bearer {model_config.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model_config.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens or model_config.max_tokens,
                "temperature": float(temperature or model_config.temperature)
            }
            
            # 发送请求
            response = requests.post(
                model_config.api_endpoint,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 更新使用统计
                model_config.usage_count += 1
                self.db.commit()
                
                return {
                    "success": True,
                    "content": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                    "model_used": model_config.model_name
                }
            else:
                return {
                    "success": False,
                    "error": f"API调用失败: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"AI模型调用异常: {str(e)}"
            }
    
    async def batch_homework(
        self, 
        user_id: int,
        image_path: str,
        subject: str,
        grade: str
    ) -> Dict:
        """AI批阅作业"""
        try:
            # 构建批阅提示词
            prompt = f"""
            请作为一名{grade}{subject}老师，批阅这份作业。
            
            要求：
            1. 识别题目内容和学生答案
            2. 判断每道题的对错
            3. 对错题进行分析，指出错误原因
            4. 识别涉及的知识点
            5. 给出改进建议
            
            请以JSON格式返回结果：
            {{
                "total_questions": 题目总数,
                "correct_count": 正确题目数,
                "accuracy_rate": 正确率,
                "questions": [
                    {{
                        "question_number": 题目序号,
                        "question_text": "题目内容",
                        "student_answer": "学生答案",
                        "correct_answer": "正确答案",
                        "is_correct": true/false,
                        "knowledge_point": "涉及知识点",
                        "error_analysis": "错误分析（如果错误）",
                        "suggestion": "改进建议"
                    }}
                ]
            }}
            """
            
            # 调用AI模型
            result = await self.call_ai_model(prompt)
            
            if result["success"]:
                # 解析结果并保存错题记录
                try:
                    ai_result = json.loads(result["content"])
                    
                    # 保存错题记录
                    for question in ai_result.get("questions", []):
                        if not question.get("is_correct", True):
                            error_record = ErrorRecord(
                                user_id=user_id,
                                subject=subject,
                                grade=grade,
                                knowledge_point=question.get("knowledge_point", ""),
                                question_text=question.get("question_text", ""),
                                correct_answer=question.get("correct_answer", ""),
                                student_answer=question.get("student_answer", ""),
                                error_type="作业错题",
                                ai_analysis=question.get("error_analysis", "")
                            )
                            self.db.add(error_record)
                    
                    self.db.commit()
                    
                    return {
                        "success": True,
                        "result": ai_result,
                        "message": "作业批阅完成"
                    }
                    
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": "AI返回结果格式错误"
                    }
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": f"作业批阅失败: {str(e)}"
            }
    
    async def generate_questions(
        self,
        user_id: int,
        subject: str,
        grade: str,
        knowledge_points: List[str],
        question_types: List[str],
        question_count: int = 10,
        difficulty_level: int = 2
    ) -> Dict:
        """生成动态练习题目"""
        try:
            # 构建题目生成提示词
            prompt = f"""
            请为{grade}学生生成{subject}练习题目。
            
            要求：
            - 涉及知识点：{', '.join(knowledge_points)}
            - 题型：{', '.join(question_types)}
            - 题目数量：{question_count}道
            - 难度等级：{difficulty_level}/5
            
            题型说明：
            - choice: 选择题（提供4个选项A、B、C、D）
            - fill: 填空题
            - solve: 解答题
            - judge: 判断题
            
            请以JSON格式返回：
            {{
                "title": "练习标题",
                "total_questions": {question_count},
                "questions": [
                    {{
                        "question_number": 1,
                        "question_type": "题型",
                        "question_text": "题目内容",
                        "options": {{"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"}}, // 仅选择题需要
                        "correct_answer": "正确答案",
                        "explanation": "答案解析",
                        "knowledge_point": "对应知识点",
                        "difficulty": 难度等级,
                        "points": 分值
                    }}
                ]
            }}
            """
            
            # 调用AI模型
            result = await self.call_ai_model(prompt)
            
            if result["success"]:
                try:
                    questions_data = json.loads(result["content"])
                    
                    return {
                        "success": True,
                        "questions_data": questions_data,
                        "model_used": result["model_used"],
                        "message": "题目生成成功"
                    }
                    
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": "AI返回的题目格式错误"
                    }
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": f"题目生成失败: {str(e)}"
            }
    
    async def generate_learning_report(
        self,
        user_id: int,
        start_date: str,
        end_date: str,
        subject: Optional[str] = None
    ) -> Dict:
        """生成学习报告"""
        try:
            # 获取用户错题记录
            query = self.db.query(ErrorRecord).filter(
                ErrorRecord.user_id == user_id,
                ErrorRecord.created_at >= start_date,
                ErrorRecord.created_at <= end_date
            )
            
            if subject:
                query = query.filter(ErrorRecord.subject == subject)
            
            error_records = query.all()
            
            # 构建报告生成提示词
            error_data = [
                {
                    "knowledge_point": record.knowledge_point,
                    "error_type": record.error_type,
                    "subject": record.subject,
                    "is_resolved": record.is_resolved
                }
                for record in error_records
            ]
            
            prompt = f"""
            请根据学生的错题记录生成学习报告。
            
            时间范围：{start_date} 到 {end_date}
            错题数据：{json.dumps(error_data, ensure_ascii=False)}
            
            请分析并生成包含以下内容的报告：
            1. 学习总结
            2. 知识点掌握情况分析
            3. 薄弱环节识别
            4. 学习进步情况
            5. 下阶段学习建议
            
            请以JSON格式返回：
            {{
                "summary": "学习总结",
                "knowledge_mastery": {{
                    "mastered": ["已掌握的知识点"],
                    "weak": ["薄弱知识点"],
                    "need_practice": ["需要加强练习的知识点"]
                }},
                "progress_analysis": "进步情况分析",
                "suggestions": ["学习建议1", "学习建议2", "..."],
                "statistics": {{
                    "total_errors": {len(error_records)},
                    "resolved_errors": 已解决错题数,
                    "subjects": ["涉及学科"]
                }}
            }}
            """
            
            # 调用AI模型
            result = await self.call_ai_model(prompt)
            
            if result["success"]:
                try:
                    report_data = json.loads(result["content"])
                    
                    return {
                        "success": True,
                        "report_data": report_data,
                        "model_used": result["model_used"],
                        "message": "学习报告生成成功"
                    }
                    
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": "AI返回的报告格式错误"
                    }
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": f"学习报告生成失败: {str(e)}"
            }
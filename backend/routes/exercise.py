# 练习题目相关路由
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from models.database import get_db
from models.user import User
from routes.auth import get_current_user

router = APIRouter()

# Pydantic模型
class ExerciseCreate(BaseModel):
    title: str
    subject: str
    grade: str
    knowledge_points: List[str]
    questions: List[dict]

class ExerciseResponse(BaseModel):
    id: int
    title: str
    subject: str
    grade: str
    knowledge_points: List[str]
    created_at: str
    
    class Config:
        from_attributes = True

# 获取练习题列表
@router.get("/", response_model=List[ExerciseResponse])
async def get_exercises(
    skip: int = 0,
    limit: int = 20,
    subject: Optional[str] = None,
    grade: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取练习题列表
    """
    # TODO: 从数据库查询练习题
    # 这里返回模拟数据
    exercises = [
        {
            "id": 1,
            "title": "数学基础练习",
            "subject": "数学",
            "grade": "七年级",
            "knowledge_points": ["代数基础", "方程求解"],
            "created_at": "2024-01-01T10:00:00"
        }
    ]
    return exercises

# 创建练习题
@router.post("/", response_model=ExerciseResponse)
async def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新的练习题
    """
    # TODO: 保存到数据库
    return {
        "id": 1,
        "title": exercise.title,
        "subject": exercise.subject,
        "grade": exercise.grade,
        "knowledge_points": exercise.knowledge_points,
        "created_at": "2024-01-01T10:00:00"
    }

# 获取练习题详情
@router.get("/{exercise_id}")
async def get_exercise_detail(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取练习题详情
    """
    # TODO: 从数据库查询
    return {
        "id": exercise_id,
        "title": "数学基础练习",
        "questions": [
            {
                "id": 1,
                "type": "选择题",
                "question": "下列哪个是正确的？",
                "options": ["A. 1+1=3", "B. 1+1=2", "C. 1+1=1", "D. 1+1=4"],
                "answer": "B",
                "explanation": "基础数学运算"
            }
        ]
    }
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database.database import get_db
from database.models import User, AIModelConfig, Exercise, ErrorRecord
from routes.auth import get_current_user
from services.ai_service import AIService
from services.pdf_service import PDFService, PDFServiceManager
import json
import os

router = APIRouter(prefix="/ai", tags=["AI功能"])

# 请求模型
class ExerciseGenerateRequest(BaseModel):
    subject: str
    knowledge_points: List[str]
    question_type: str  # choice, fill, solve, mixed
    question_count: int
    difficulty_level: int = 1

class AnswerAnalysisRequest(BaseModel):
    exercise_id: int

class ErrorAnalysisRequest(BaseModel):
    user_id: Optional[int] = None  # 如果不提供，使用当前用户

# 响应模型
class ExerciseResponse(BaseModel):
    exercise_id: int
    questions: List[dict]
    success: bool
    message: str

class AnalysisResponse(BaseModel):
    analyses: List[dict]
    success: bool
    message: str

@router.post("/generate-exercise", response_model=ExerciseResponse)
async def generate_exercise(
    request: ExerciseGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成练习题目"""
    
    try:
        async with AIService(db) as ai_service:
            # 调用AI生成题目
            result = await ai_service.generate_exercise_questions(
                user_id=current_user.id,
                subject=request.subject,
                knowledge_points=request.knowledge_points,
                question_type=request.question_type,
                question_count=request.question_count,
                difficulty_level=request.difficulty_level
            )
            
            if not result['success']:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"题目生成失败: {result.get('error', '未知错误')}"
                )
            
            # 解析AI返回的题目内容
            try:
                questions_data = json.loads(result['content'])
                questions = questions_data.get('questions', [])
            except json.JSONDecodeError:
                # 如果AI返回的不是标准JSON，尝试简单解析
                questions = [
                    {
                        "id": 1,
                        "type": request.question_type,
                        "content": result['content'],
                        "knowledge_point": request.knowledge_points[0] if request.knowledge_points else request.subject,
                        "difficulty": request.difficulty_level
                    }
                ]
            
            # 保存练习记录到数据库
            exercise = Exercise(
                user_id=current_user.id,
                title=f"{request.subject}练习 - {len(questions)}题",
                subject=request.subject,
                question_type=request.question_type,
                question_count=len(questions),
                difficulty_level=request.difficulty_level,
                generated_content={"questions": questions},
                completion_status="pending"
            )
            
            db.add(exercise)
            db.commit()
            db.refresh(exercise)
            
            return ExerciseResponse(
                exercise_id=exercise.id,
                questions=questions,
                success=True,
                message="题目生成成功"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成练习时发生错误: {str(e)}"
        )

@router.post("/generate-analysis", response_model=AnalysisResponse)
async def generate_analysis(
    request: AnswerAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成答案解析"""
    
    # 获取练习记录
    exercise = db.query(Exercise).filter(
        Exercise.id == request.exercise_id,
        Exercise.user_id == current_user.id
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="练习记录不存在"
        )
    
    try:
        async with AIService(db) as ai_service:
            # 获取题目内容
            questions = exercise.generated_content.get('questions', [])
            
            # 调用AI生成解析
            result = await ai_service.generate_answer_analysis(
                user_id=current_user.id,
                questions=questions
            )
            
            if not result['success']:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"解析生成失败: {result.get('error', '未知错误')}"
                )
            
            # 解析AI返回的解析内容
            try:
                analysis_data = json.loads(result['content'])
                analyses = analysis_data.get('analyses', [])
            except json.JSONDecodeError:
                # 如果AI返回的不是标准JSON，创建简单解析
                analyses = [
                    {
                        "question_id": i + 1,
                        "answer": "请参考AI生成的解析",
                        "steps": [result['content']],
                        "knowledge_points": [],
                        "common_mistakes": [],
                        "tips": ""
                    }
                    for i in range(len(questions))
                ]
            
            # 更新练习记录的答案内容
            exercise.answer_content = {"analyses": analyses}
            db.commit()
            
            return AnalysisResponse(
                analyses=analyses,
                success=True,
                message="解析生成成功"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成解析时发生错误: {str(e)}"
        )

@router.post("/generate-pdf/{exercise_id}")
async def generate_exercise_pdf(
    exercise_id: int,
    include_answers: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成练习题PDF"""
    
    # 获取练习记录
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="练习记录不存在"
        )
    
    try:
        # 准备练习数据
        exercise_data = {
            "subject": exercise.subject,
            "title": exercise.title,
            "question_count": exercise.question_count,
            "question_type": exercise.question_type,
            "difficulty_level": exercise.difficulty_level,
            "generated_content": exercise.generated_content
        }
        
        # 生成PDF文件路径
        pdf_path = PDFServiceManager.get_pdf_path(exercise_id, 'exercise')
        
        # 生成PDF
        pdf_service = PDFService()
        pdf_service.generate_exercise_pdf(exercise_data, pdf_path, include_answers)
        
        # 更新练习记录的PDF路径
        exercise.pdf_path = pdf_path
        db.commit()
        
        return {
            "success": True,
            "message": "PDF生成成功",
            "pdf_path": pdf_path,
            "download_url": f"/api/ai/download-pdf/{exercise_id}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF生成失败: {str(e)}"
        )

@router.post("/generate-answer-pdf/{exercise_id}")
async def generate_answer_pdf(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成答案解析PDF"""
    
    # 获取练习记录
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="练习记录不存在"
        )
    
    if not exercise.answer_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先生成答案解析"
        )
    
    try:
        # 准备数据
        exercise_data = {
            "subject": exercise.subject,
            "title": exercise.title,
            "generated_content": exercise.generated_content
        }
        
        analysis_data = exercise.answer_content
        
        # 生成PDF文件路径
        pdf_path = PDFServiceManager.get_pdf_path(exercise_id, 'answer')
        
        # 生成PDF
        pdf_service = PDFService()
        pdf_service.generate_answer_pdf(exercise_data, analysis_data, pdf_path)
        
        return {
            "success": True,
            "message": "答案解析PDF生成成功",
            "pdf_path": pdf_path,
            "download_url": f"/api/ai/download-answer-pdf/{exercise_id}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"答案解析PDF生成失败: {str(e)}"
        )

@router.get("/download-pdf/{exercise_id}")
async def download_exercise_pdf(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """下载练习题PDF"""
    
    # 获取练习记录
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    ).first()
    
    if not exercise or not exercise.pdf_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF文件不存在"
        )
    
    if not os.path.exists(exercise.pdf_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF文件已被删除"
        )
    
    filename = f"{exercise.subject}练习_{exercise_id}.pdf"
    return FileResponse(
        path=exercise.pdf_path,
        filename=filename,
        media_type='application/pdf'
    )

@router.get("/preview-pdf/{exercise_id}")
async def preview_exercise_pdf(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """预览练习题PDF"""
    
    # 获取练习记录
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="练习记录不存在"
        )
    
    # 如果没有PDF，先生成一个
    if not exercise.pdf_path or not os.path.exists(exercise.pdf_path):
        try:
            exercise_data = {
                "subject": exercise.subject,
                "title": exercise.title,
                "question_count": exercise.question_count,
                "question_type": exercise.question_type,
                "difficulty_level": exercise.difficulty_level,
                "generated_content": exercise.generated_content
            }
            
            pdf_path = PDFServiceManager.get_pdf_path(exercise_id, 'preview')
            pdf_service = PDFService()
            pdf_service.generate_exercise_pdf(exercise_data, pdf_path, False)
            
            exercise.pdf_path = pdf_path
            db.commit()
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"PDF预览生成失败: {str(e)}"
            )
    
    return FileResponse(
        path=exercise.pdf_path,
        media_type='application/pdf'
    )

@router.get("/models")
async def get_ai_models(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取可用的AI模型列表"""
    
    models = db.query(AIModelConfig).filter(AIModelConfig.is_active == True).all()
    
    return {
        "models": [
            {
                "name": model.model_name,
                "display_name": model.display_name,
                "is_default": model.is_default
            }
            for model in models
        ]
    }
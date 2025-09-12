from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "后端运行正常"}

@app.get("/api/ai/test-connection")
async def test_connection():
    return {"success": True, "message": "连接正常"}

@app.post("/api/ai/photo-correction")
async def photo_correction(request_data: dict):
    return {
        "success": True,
        "result": {
            "accuracy": 85,
            "score": 85,
            "totalScore": 100,
            "questions": [{
                "content": "测试题目",
                "studentAnswer": "测试答案",
                "correctAnswer": "正确答案",
                "isCorrect": True,
                "explanation": "解析内容"
            }]
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
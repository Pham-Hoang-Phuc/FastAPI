from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

# 1. Dùng Enum để giới hạn loại Model AI
class YoloVersion(str, Enum):
    v8 = "v8"
    v11 = "v11"

# 2. Dùng Pydantic để định nghĩa yêu cầu nhận diện
class DetectionTask(BaseModel):
    model_name: YoloVersion # Kết hợp Enum vào đây
    confidence: float = 0.5 # Mặc định là 0.5, phải là số thực
    image_url: str


# @app.get("/")
# async def root():
#     return 

@app.

@app.post("/predict")
def predict(task: DetectionTask):
    return {"message": f"Đang chạy {task.model_name} với độ tin cậy {task.confidence}"}
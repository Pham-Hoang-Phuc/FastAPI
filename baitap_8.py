from enum import Enum
from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field

app = FastAPI()

class TaskStatus(Enum):
    TODO = 'todo'
    DOING = 'doing'
    DONE = 'done'

class Priority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class SubTask(BaseModel):
    title: str = Field(..., min_length=5)
    is_completed: bool

class Task(BaseModel):
    title: str
    description: str | None = None
    priority: Priority
    assignee: str = Field(...)
    subtask: list[SubTask]

db_tasks = {
    1: {
        "title": "Học FastAPI",
        "description": "Học về Pydantic",
        "priority": "High",
        "status": "doing",
        "assignee": "An",
        "subtasks": [
            {"title": "Đọc docs", "is_completed": True},
            {"title": "Code thử", "is_completed": False}
        ]
    },
    2: {
        "title": "Thiết kế Database",
        "description": "Vẽ sơ đồ ERD cho dự án quản lý kho",
        "priority": "High",
        "status": "todo",
        "assignee": "Bình",
        "subtasks": [
            {"title": "Liệt kê các bảng", "is_completed": False},
            {"title": "Xác định quan hệ giữa các bảng", "is_completed": False}
        ]
    },
    3: {
        "title": "Viết Unit Test",
        "description": "Viết test cho module Authentication",
        "priority": "Medium",
        "status": "doing",
        "assignee": "Chi",
        "subtasks": [
            {"title": "Test login thành công", "is_completed": True},
            {"title": "Test login sai mật khẩu", "is_completed": False},
            {"title": "Test đăng ký tài khoản", "is_completed": False}
        ]
    },
    4: {
        "title": "Fix bug giao diện",
        "description": "Sửa lỗi tràn chữ trên màn hình mobile",
        "priority": "Low",
        "status": "done",
        "assignee": "Dũng",
        "subtasks": [
            {"title": "Kiểm tra trên iPhone 13", "is_completed": True},
            {"title": "Kiểm tra trên Samsung S23", "is_completed": True}
        ]
    },
    5: {
        "title": "Viết tài liệu API",
        "description": "Sử dụng Swagger để export tài liệu",
        "priority": "Medium",
        "status": "todo",
        "assignee": "Hạnh",
        "subtasks": [
            {"title": "Mô tả các endpoint", "is_completed": False}
        ]
    },
    6: {
        "title": "Tối ưu hóa Performance",
        "description": "Tối ưu câu lệnh SQL cho trang Dashboard",
        "priority": "High",
        "status": "doing",
        "assignee": "Khánh",
        "subtasks": [
            {"title": "Thêm Index cho bảng Order", "is_completed": True},
            {"title": "Sử dụng Redis cache", "is_completed": False}
        ]
    }
}

@app.post('/tasks/create')
async def add_task(
    task: Task,
    secret_code = Body(...)
):
    if secret_code != "FASTAPI_2024":
        raise HTTPException(status_code=403, detail="403 Forbidden")
    
    new_id = len(db_tasks) + 1
    new_task = task.model_dump()

    result = {
        "title": new_task["title"],
        "description": new_task["description"],
        "priority": new_task["priority"],
        "status": TaskStatus.TODO,
        "assignee": new_task["assignee"],
        "subtasks": new_task["subtask"],
    }

    db_tasks[new_id] = result

    return db_tasks

@app.get('/tasks/report')
async def find_and_compute_total_tasks(
    assignee: str | None = None,
    status: TaskStatus | None = None
):
    total_tasks = 0
    completed_ratio = 0
    completed = 0
    total_sub = 0
    res = []

    for id, task in db_tasks.items():
        dk_asg = (assignee is None) or (assignee.lower() in task["assignee"].lower())

        dk_status = (status is None) or (status.value == task["status"].lower())

        if dk_asg and dk_status:
            res.append(task)
            total_tasks += 1

            for subtask in task["subtasks"]:
                total_sub += 1
                if subtask["is_completed"] == True:
                    completed += 1
            
            if total_sub > 0:
                completed_ratio = completed / total_sub
    
    return {
        "list_of_tasks": res,
        "Total_tasks": total_tasks,
        "completed_ratio": completed_ratio
    }
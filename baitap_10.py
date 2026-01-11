from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query, Path, Body, Cookie, Header
from enum import Enum
from pydantic import BaseModel, Field

class Guest(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: str = Field(...)
    check_in_time: datetime = Field(...)
    session_duration: timedelta = Field(...)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "full_name": "Hoang Phuc",
                    "email": "__@gmail.com",
                    "check_in_time": "2026-01-11T10:00:00",
                    "session_duration": "PT2H30M"
                }
            ]
        }
    }

app = FastAPI()

db_guests = []

@app.post('/register')
async def register(
    guest: Guest
):
    new_guests_data = guest.model_dump()
    db_guests.append(new_guests_data)

    return {
        "message": "Đăng ký thành công",
        "guest_info": new_guests_data
    }

@app.get("/event-info")
async def check_information(
    x_event_key: str = Header(...),
    last_visit: str | None = Cookie(None)
):
    SECRET_KEY = "TECH_2026"

    if x_event_key != SECRET_KEY:
        raise HTTPException(status_code=404, detail="YOU DON'T HAVE PERMISTION TO CONNECT THIS SITE")
    
    return {
        "event_name": "Hội thảo Công nghệ 2026",
        "location": "Trung tâm Hội nghị Quốc gia",
        "your_last_visit_cookie": last_visit,
        "status": "Authorized"
    }

@app.get("/guests/filter")
async def filter_guests_by_time(
    # Khai báo start_date là một Query parameter bắt buộc, kiểu datetime
    start_date: datetime = Query(..., description="Lọc khách mời check-in sau thời điểm này (định dạng: YYYY-MM-DDTHH:MM:SS)")
):
    # Sử dụng List Comprehension để lọc
    # Lưu ý: Trong db_guests, check_in_time đang là đối tượng datetime (nhờ Pydantic parse từ POST)
    filtered_guests = [
        guest for guest in db_guests 
        if guest["check_in_time"] > start_date
    ]
    
    return {
        "filter_after": start_date,
        "count": len(filtered_guests),
        "results": filtered_guests
    }
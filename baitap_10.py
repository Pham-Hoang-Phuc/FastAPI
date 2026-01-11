from fastapi import FastAPI, HTTPException, Query, Path, Body, Header, Cookie
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timedelta


app = FastAPI()

class Guest(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: str
    check_in_time: datetime
    session_duration: timedelta

    model_config = {
        'json_schema_extra' : {
            "examples": [
                {
                    "full_name": "Phuc",
                    "email": "phuc@gmail.com",
                    "check_in_time": datetime.now(),
                    "session_duration": "PT2H30M"
                }
            ]
        }
    }

from datetime import datetime, timedelta

db_guests = [
    {
        "full_name": "Nguyễn Văn An",
        "email": "an.nguyen@example.com",
        "check_in_time": datetime(2026, 1, 11, 8, 30, 0),
        "session_duration": timedelta(hours=2)
    },
    {
        "full_name": "Trần Thị Bình",
        "email": "binh.tran@gmail.com",
        "check_in_time": datetime(2026, 1, 11, 9, 15, 0),
        "session_duration": timedelta(minutes=45)
    },
    {
        "full_name": "Lê Minh Cường",
        "email": "cuonglm@company.vn",
        "check_in_time": datetime(2026, 1, 11, 10, 0, 0),
        "session_duration": timedelta(hours=1, minutes=30)
    },
    {
        "full_name": "Phạm Hồng Đào",
        "email": "daoph@outlook.com",
        "check_in_time": datetime(2026, 1, 11, 13, 45, 0),
        "session_duration": timedelta(hours=3)
    },
    {
        "full_name": "Hoàng Anh Tuấn",
        "email": "tuanha@hcmut.edu.vn",
        "check_in_time": datetime(2026, 1, 11, 15, 20, 0),
        "session_duration": timedelta(minutes=120)
    }
]

@app.post("/register")
async def register(guest: Guest):
    new_guest = guest.model_dump()
    db_guests.append(new_guest)

    return {
        "message": "register succesfully",
        "result": new_guest
    }

@app.get("/event-info")
async def check_info_event(
    x_event_key = Header(...),
    last_visit = Cookie(None)
):
    SECRET_KEY = "phuc"

    if x_event_key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="YOU DON'T HAVE PERMISSION TO ENTER THIS EVEN")

    return{
        "message": "enter successfully",
        "Cookie": last_visit
    }

@app.get("/guests/filter")
async def filter_guests(start_date: datetime = Query(..., description="YYYY-MM-DD")):

    guests = [
        guest for guest in db_guests
        if start_date <= guest["check_in_time"]
    ]
    
    return guests
# Áp dụng REQUEST BODY & Query Parameters and String Validation

from enum import Enum
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

class TrangThaiDuAn(Enum):
    MOI = 'new'
    DANG_LAM = 'doing'
    HOAN_THANH = 'done'

ds_du_an = [
    {
        "id": 1, 
        "ten": "Hệ thống AI Chatbot", 
        "mo_ta": "Phát triển chatbot hỗ trợ khách hàng tự động cho doanh nghiệp.", 
        "trang_thai": TrangThaiDuAn.DANG_LAM, 
        "ngan_sach": 50000000
    },
    {
        "id": 2, 
        "ten": "Website Thương mại điện tử", 
        "mo_ta": "Xây dựng nền tảng bán hàng trực tuyến tích hợp thanh toán.", 
        "trang_thai": TrangThaiDuAn.MOI, 
        "ngan_sach": 120000000
    },
    {
        "id": 3, 
        "ten": "App Theo dõi sức khỏe", 
        "mo_ta": "Ứng dụng di động giúp người dùng theo dõi chỉ số sức khỏe hàng ngày.", 
        "trang_thai": TrangThaiDuAn.HOAN_THANH, 
        "ngan_sach": 85000000
    },
    {
        "id": 4, 
        "ten": "Phần mềm Quản lý kho", 
        "mo_ta": "Hệ thống quản lý nhập xuất kho và kiểm kê tự động.", 
        "trang_thai": TrangThaiDuAn.DANG_LAM, 
        "ngan_sach": 45000000
    },
    {
        "id": 5, 
        "ten": "Hệ thống Booking khách sạn", 
        "mo_ta": "Giải pháp đặt phòng trực tuyến dành cho các chuỗi khách sạn lớn.", 
        "trang_thai": TrangThaiDuAn.MOI, 
        "ngan_sach": 200000000
    }
]


class DuAnMoi(BaseModel):
    ten : str = Field(..., min_length=5, max_length=50)
    mo_ta : str = Field(..., min_length=10)
    trang_thai : TrangThaiDuAn 
    ngan_sach : int = Field(..., gt=0) 

@app.post("/du-an/")
async def tao_du_an(new : DuAnMoi):
    new_project = {
        "id" : len(ds_du_an) + 1,
        **new.model_dump()
    }
    ds_du_an.append(new_project)
    return ds_du_an


@app.get("/du-an/search/")
async def tim_du_an(tu_khoa : str = Query(..., min_length=3), trang_thai : TrangThaiDuAn | None = None):
    ket_qua = []
    for du_an in ds_du_an:

        khop_tu_khoa = tu_khoa.lower() in du_an["ten"].lower()

        khop_trang_thai = (trang_thai == du_an["trang_thai"] or trang_thai is None)
        
        if khop_tu_khoa and khop_trang_thai:
            ket_qua.append(du_an)
    
    if not ket_qua:
        raise HTTPException(status_code=404, detail="Not Found")

    return ket_qua
    
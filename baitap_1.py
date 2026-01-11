from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

class TheLoai(Enum):
    KHOA_HOC = "khoa-hoc"
    VAN_HOC = "van-hoc"
    GIAO_DUC = "giao-duc"

data_sach = [
    {
        "id": 1, 
        "ten": "Khoa hoc vien tuong", 
        "the_loai": TheLoai.KHOA_HOC
    },
    {
        "id": 2, 
        "ten": "Số đỏ", 
        "the_loai": TheLoai.VAN_HOC
    },
    {
        "id": 3, 
        "ten": "Giải tích 1", 
        "the_loai": TheLoai.GIAO_DUC
    },
    {
        "id": 4, 
        "ten": "Lược sử thời gian", 
        "the_loai": TheLoai.KHOA_HOC
    }
]

# XỬ LÝ
@app.get("/sach/{sach_id}")
async def find_id(sach_id : int):
    for sach in data_sach:
        if sach["id"] == sach_id:
            return sach

    raise HTTPException(status_code=404, detail="not find") 

@app.get('/sach/')
async def loc_sach(the_loai : TheLoai | None = None, tu_khoa: str | None = None):

    ket_qua = []

    for sach in data_sach:
        khop_the_loai = True
        khop_tu_khoa = True
    
        if the_loai and sach["the_loai"] != the_loai:
            khop_the_loai = False
        
        if tu_khoa and tu_khoa.lower() not in sach["ten"].lower():
            khop_tu_khoa = False
        
        if khop_tu_khoa and khop_the_loai:
            ket_qua.append(sach)
    
    if not ket_qua:
        raise HTTPException(status_code=404, detail="Khong tim thay sach")
    
    return ket_qua
from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

class PhongBan(Enum):
    FRONTEND = "frontend" 
    BACKEND = "backend"
    DESIGN = "design"

# 2. Danh sách nhân viên giả lập
ds_nhan_vien = [
    {
        "id": 1, 
        "ten": "Nguyễn Văn An", 
        "phong_ban": PhongBan.FRONTEND, 
        "kinh_nghiem": 2, 
        "la_quan_ly": False
    },
    {
        "id": 2, 
        "ten": "Trần Thị Bình", 
        "phong_ban": PhongBan.BACKEND, 
        "kinh_nghiem": 5, 
        "la_quan_ly": True
    },
    {
        "id": 3, 
        "ten": "Lê Quang Chi", 
        "phong_ban": PhongBan.DESIGN, 
        "kinh_nghiem": 3, 
        "la_quan_ly": False
    },
    {
        "id": 4, 
        "ten": "Phạm Minh Dũng", 
        "phong_ban": PhongBan.BACKEND, 
        "kinh_nghiem": 1, 
        "la_quan_ly": False
    },
    {
        "id": 5, 
        "ten": "Hoàng Thu Hoa", 
        "phong_ban": PhongBan.FRONTEND, 
        "kinh_nghiem": 4, 
        "la_quan_ly": True
    },
    {
        "id": 6, 
        "ten": "Vũ Đình Khôi", 
        "phong_ban": PhongBan.DESIGN, 
        "kinh_nghiem": 6, 
        "la_quan_ly": True
    },
    {
        "id": 7, 
        "ten": "Đặng Mỹ Linh", 
        "phong_ban": PhongBan.BACKEND, 
        "kinh_nghiem": 2, 
        "la_quan_ly": False
    }
]

@app.get("/nhan-vien/phong/{ten_phong}")
async def phong_ban(ten_phong : PhongBan):
    ket_qua = []
    for nhan_vien in ds_nhan_vien:
        if nhan_vien["phong_ban"] == ten_phong:
            ket_qua.append(nhan_vien)
    
    if not ket_qua:
        raise HTTPException(status_code=404, detail="Not found")

    return ket_qua

@app.get("/nhan-vien/loc/")
async def loc_nang_cao(min_exp : int | None =  None, is_manager : bool | None = None):
    
    ket_qua = []
    for nhan_vien in ds_nhan_vien:
        dk_kn = (min_exp is None) or (min_exp <= nhan_vien["kinh_nghiem"])

        dk_ql = (is_manager is None) or (nhan_vien["la_quan_ly"] == is_manager)


        if dk_ql and dk_kn:
            ket_qua.append(nhan_vien)
    
    if not ket_qua:
        raise HTTPException(status_code=404, detail="Not Found")
    
    return ket_qua
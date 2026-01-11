from enum import Enum
from fastapi import FastAPI, Query, Path, Body, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class PhanLoai(str, Enum):
    CPU = "cpu"
    GPU = "gpu"
    RAM = "ram"
    SSD = "ssd"

class ThongSo(BaseModel):
    nhan_hang: str = Field(..., min_length=2)
    bao_hanh_thang: int = Field(..., ge=6, le=36)

class LinhKien(BaseModel):
    ten: str = Field(..., min_length=3)
    phan_loai: PhanLoai
    gia: float = Field(..., gt=0)
    chi_tiet: ThongSo


# 3. Dữ liệu giả lập (Mock Data)
kho_hang = [
    {
        "id": 1,
        "ten": "Core i9-13900K",
        "phan_loai": PhanLoai.CPU,
        "gia": 15000000.0,
        "ton_kho": 10,
        "chi_tiet": {"nhan_hang": "Intel", "bao_hanh_thang": 36}
    },
    {
        "id": 2,
        "ten": "GeForce RTX 4090",
        "phan_loai": PhanLoai.GPU,
        "gia": 45000000.0,
        "ton_kho": 5,
        "chi_tiet": {"nhan_hang": "NVIDIA", "bao_hanh_thang": 36}
    },
    {
        "id": 3,
        "ten": "Vengeance LPX 16GB",
        "phan_loai": PhanLoai.RAM,
        "gia": 1200000.0,
        "ton_kho": 50,
        "chi_tiet": {"nhan_hang": "Corsair", "bao_hanh_thang": 12}
    },
    {
        "id": 4,
        "ten": "Samsung 980 Pro 1TB",
        "phan_loai": PhanLoai.SSD,
        "gia": 2500000.0,
        "ton_kho": 30,
        "chi_tiet": {"nhan_hang": "Samsung", "bao_hanh_thang": 24}
    }
]

@app.put("/kho/{linh_kien_id}/update-stock")
async def cap_nhat_linh_kien(
    linh_kien_id: int = Path(..., gt=0), 
    so_luong_moi: int = Query(..., gt=0, lt=1000)):

    check = False
    for linh_kien in kho_hang:
        if linh_kien['id'] == linh_kien_id:
            linh_kien["ton_kho"] = so_luong_moi
            check = True
            return linh_kien
    
    if check is not True:
        raise HTTPException(status_code=404, detail="Not Found")


@app.post("/kho/add/")
async def them_linh_kien(
    item: LinhKien,
    ma_kho: int = Body(...)):
    
    item_dict = item.model_dump()
    new_item = {
        "id": len(kho_hang) + 1,
        "ma_kho": ma_kho,
        "ton_kho": 0,
        **item_dict
    }

    kho_hang.append(item_dict)

    return {
        "message": f"Da them linh kien vao kho so {ma_kho}",
        "data": new_item
    }


@app.get("/kho/search/")
async def tim_kiem_nang_cao(
    min_price: float = Query(None, gt=0),
    max_price: float = Query(None, gt=0)):

    res = []
    sum_ = 0

    for hang in kho_hang:
        dk_min_price = (min_price is None) or (min_price <= hang["gia"])

        dk_max_price = (max_price is None) or (max_price >= hang["gia"])

        if dk_max_price and dk_min_price:
            sum_ += 1
            res.append(hang)
    
    if not res:
        raise HTTPException(status_code=404, detail="Not Found")
    return {
        "Message": f"Finded {sum_}",
        "Result": res
    }
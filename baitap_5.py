from enum import Enum
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

class Size(Enum):
    SMALL = 'small'
    MEDIUM =  'medium'
    LARGE = 'large'

class Item(BaseModel):
    ten_mon : str = Field(..., min_length=3)
    so_luong : int = Field(..., gt=0)
    size : Size = Field(Size.MEDIUM)

class Order(BaseModel):
    khach_hang : str = Field(..., min_length=3)
    danh_sach_mon : list[Item]
    ghi_chu : str | None = None

ds_don_hang = []

@app.post('/Order')
async def tao_don_hang(order : Order):
    tong = 0
    
    for mon in order.danh_sach_mon:
        tong += mon.so_luong
    
    new_order = order.model_dump()

    ket_qua = {
        "id": len(ds_don_hang) + 1,
        "khach_hang": new_order['khach_hang'],
        "tong_ly": tong,
        "danh_sach_mon": new_order['danh_sach_mon'],
        "ghi_chu": new_order['ghi_chu']
    }
    ds_don_hang.append(ket_qua)
    return ds_don_hang

@app.get('/orders/search')
async def filter_by_order(
    ten_khach: str | None = Query(None, max_length=29),
    so_ly_toi_thieu: int | None = None):
    
    res = []

    for don_hang in ds_don_hang:
        dk_ten = (ten_khach is None) or (ten_khach.lower() in don_hang["khach_hang"].lower())

        dk_so_ly = (so_ly_toi_thieu is None) or (so_ly_toi_thieu <= don_hang["tong_ly"])

        if dk_so_ly and dk_ten:
            res.append(don_hang)
    
    if not res:
        raise HTTPException(status_code=404, detail="Not Found")
    return res
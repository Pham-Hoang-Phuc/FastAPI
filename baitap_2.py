from enum import Enum
from fastapi import FastAPI, HTTPException

app = FastAPI()

class LoaiDoUong(Enum):
    COFFEE = "coffee"
    TEA = "tea"
    JUICE = "juice"

menu = [
    {"id": 1, "ten": "Cà phê Đen", "gia": 25000, "loai": LoaiDoUong.COFFEE},
    {"id": 2, "ten": "Cà phê Sữa", "gia": 29000, "loai": LoaiDoUong.COFFEE},
    {"id": 3, "ten": "Trà Đào Cam Sả", "gia": 45000, "loai": LoaiDoUong.TEA},
    {"id": 4, "ten": "Trà Vải", "gia": 39000, "loai": LoaiDoUong.TEA},
    {"id": 5, "ten": "Nước Ép Cam", "gia": 50000, "loai": LoaiDoUong.JUICE},
    {"id": 6, "ten": "Nước Ép Dưa Hấu", "gia": 40000, "loai": LoaiDoUong.JUICE},
    {"id": 7, "ten": "Bạc Xỉu", "gia": 32000, "loai": LoaiDoUong.COFFEE},
]

@app.get("/menu/loai/{loai_do_uong}")
async def mon_theo_nhu_cau(loai_do_uong: LoaiDoUong):
    ket_qua = []
    for do_uong in menu:
        if do_uong["loai"] == loai_do_uong:
            ket_qua.append(do_uong)
    if not ket_qua:
        raise HTTPException(status_code=404, detail="Not Found")
    return ket_qua

@app.get("/menu/search/")
async def scale(gia_min : int = None, gia_max : int = None):

    ket_qua = []
    for mon in menu:
        dk_min = (gia_min is None) or (gia_min < mon["gia"] )

        dk_max = (gia_max is None) or (gia_max > mon["gia"])
    
        if dk_max and dk_min:
            ket_qua.append(mon)
    
    if not ket_qua:
        raise HTTPException(status_code=404, detail="Not found")
    return ket_qua
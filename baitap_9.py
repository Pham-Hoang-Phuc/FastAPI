from fastapi import FastAPI, Query, Path, Body, HTTPException
from pydantic import BaseModel, Field
from enum import Enum

class TrangThaiDonHang(Enum):
    PENDING = "PENDING"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class ThongTinSanPham(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=1)

class DonHang(BaseModel):
    customer_name: str
    items: list[ThongTinSanPham]

app = FastAPI()

db_orders = [
    {
        "order_id": 1,
        "customer_name": "Nguyen Van A",
        "items": [{"name": "Laptop", "price": 1000, "quantity": 1}],
        "status": TrangThaiDonHang.PENDING,
        "total_price": 1000
    }
]

@app.post("/orders")
async def create_new_order(
    order: DonHang,
    status: TrangThaiDonHang
):

    new_order = order.model_dump()
    new_id = len(db_orders) + 1

    total_price = sum(item["price"] * item["quantity"] for item in new_order["items"]) 

    result = {
        "id": new_id,
        **new_order,
        "status": status,
        "total_price": total_price
    }

    db_orders.append(result)

    return db_orders

@app.get("/orders/")
async def filter_orders(
    status: TrangThaiDonHang | None = None,
    min_total: float = Query(0, ge=0)
):
    result = []

    for order in db_orders:
        dk_status = (status is None) or (status == order["status"])

        dk_total = (min_total == 0) or (min_total <= order["total_price"])

        if dk_status and dk_total:
            result.append(order)
    
    result = [
        order for order in db_orders
        if (status is None or order['status'] == status) and 
           (order["total_price"] >= min_total)]
    
    if not result:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    
    return result

@app.put("/orders/{order_id}/status")
async def update_status(
    *,
    order_id: int = Path(..., gt=0),
    new_status : TrangThaiDonHang,
    note: str | None = Body(None)
):
    target_order = next((order for order in db_orders if order["order_id"] == order_id), None)
    
    if target_order is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    
    target_order["status"] = new_status
    if note:
        target_order["note"] = note

    return target_order
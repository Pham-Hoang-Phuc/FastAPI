from enum import Enum
from fastapi import FastAPI, Query, Path,  HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Category(Enum):
    COFFEE = "coffee"
    TEA = "tea"
    BAKERY = "bakery"

class Product(BaseModel):
    name : str = Field(..., min_length=3)
    price : float = Field(..., ge=0)
    category : Category

class Order(BaseModel):
    customer_name : str
    items : list[Product]
    note : str | None = None

db_orders = {
    1: {
        "customer_name": "An", 
        "items": [{
            "name": "Latte", 
             "price": 45.0, 
             "category": "Coffee"}], 
        "table_number": 5, 
        "total_price": 45.0
        },
    2: {
        "customer_name": "Bình", 
        "items": 
        [{
            "name": "Croissant", 
            "price": 30.0, 
            "category": "Bakery"}], 
        "table_number": 10, 
        "total_price": 30.0}
}

@app.post("/orders/create")
async def add_new_order(
    order: Order,
    table_number: int | None = Query(..., gt=1, lt=50)
    ):

    new_order = order.model_dump()
    total_price = 0

    for item in new_order["items"]:
        total_price += item["price"]
    
    res = {
        **new_order,
        "table_number": table_number,
        "total_price": total_price
    } 

    new_id = len(db_orders) + 1
    db_orders[new_id] = res

    return res

@app.get("/orders/search")
async def Find_customer_name(
    customer_name: str | None = None,
    min_total: float | None = None):

    res = [] 

    for id, order in db_orders.items():
        dk_name = (customer_name is None) or (customer_name.lower() in order["customer_name"].lower())

        dk_total = (min_total is None) or (min_total <= order["total_price"])

        if dk_name and dk_total:
            res.append(order)
    
    if not res:
        raise HTTPException(status_code=404, detail="NOT FOUND")

    return res

@app.put("/orders/{order_id}")
async def name_(
    *,
    order_id: int = Path(..., gt=0),
    new_order: Order):

    if order_id not in db_orders:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    
    new_total = sum(item.price for item in new_order.items)
    new_order_dict = new_order.model_dump()

    update_data = {**db_orders[order_id], **new_order_dict}

    db_orders[order_id] = update_data

    return {
        "message": "DONE",
        "Result": db_orders
    }

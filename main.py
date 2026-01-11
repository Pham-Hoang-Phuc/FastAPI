from fastapi import FastAPI
from enum import Enum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def post():
    return {"message" : "Hello from post"}

@app.put("/")
async def put():
    return {"message" : "Hello from put"}

@app.get("/food")
async def get_food():
    return {"message" : "Ở đây có nhiều món để chọn lắm"}


@app.get("/user/{name}")
async def get_nameid(name):
    return {"message" : f"Hi {name}"}

class Food(Enum):
    carrot = "carrot"
    apple = "apple"
    fruits = "fruits"


print(Food.apple)

@app.get("/food/{food_name}")
async def get_food_2(food_name : Food):
    if food_name == Food.apple:
        return {"message" : "you eat apple"}

    elif food_name == Food.fruits:
        return {"message" : "you eata fruits"}

    elif food_name == Food.carrot:
        return {"message" : "you is a rabbit"}
    

book = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

@app.get("/limit")
async def get_limit(skip: int = 0, limit: int = 10):
    return book[skip: skip + limit]



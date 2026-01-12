from fastapi import FastAPI, HTTPException, Query, Path, Header, Cookie, Body
from pydantic import BaseModel, Field, EmailStr
from enum import Enum

app = FastAPI()

class Departments(Enum):
    IT = "IT" 
    HR = "HR" 
    ENGINEERING = "Engineering" 
    SALES = "Sales" 
    MARKETING = "Marketing" 
    FINANCE = "Finance" 
    DATA = "Data"

class EmployeeBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    department: Departments | None = None

class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=8, description="mật khẩu cần hơn 8 kí tự")
    salary: float = Field(None, gt=0)

class EmployeePublic(EmployeeBase):
    id: int 

db_employees = [
    {"id": 1, "username": "admin_hieu", "email": "hieu.admin@company.com", "department": "IT", "password": "password123@", "salary": 25000.0},
    {"id": 2, "username": "lan_nguyen", "email": "lan.nguyen@company.com", "department": "HR", "password": "securepass88", "salary": 18000.0},
    {"id": 3, "username": "tung_dev", "email": "tung.dev@company.com", "department": "Engineering", "password": "codingislife!", "salary": 30000.0},
    {"id": 4, "username": "minh_sale", "email": "minh.v@company.com", "department": "Sales", "password": "salesmaster1", "salary": 15000.0},
    {"id": 5, "username": "phuong_mkt", "email": "phuong.m@company.com", "department": "Marketing", "password": "creative_mkt2024", "salary": 17500.0},
    {"id": 6, "username": "quang_pm", "email": "quang.p@company.com", "department": "Engineering", "password": "pm_secret_key", "salary": 35000.0},
    {"id": 7, "username": "thuy_acc", "email": "thuy.accountant@company.com", "department": "Finance", "password": "money_matters#1", "salary": 22000.0},
    {"id": 8, "username": "bach_ba", "email": "bach.analyst@company.com", "department": "Data", "password": "data_is_gold", "salary": 28000.0},
    {"id": 9, "username": "diem_tester", "email": "diem.tester@company.com", "department": "IT", "password": "bug_hunter_99", "salary": 16000.0},
    {"id": 10, "username": "long_ops", "email": "long.ops@company.com", "department": "Engineering", "password": "devops_power!", "salary": 32000.0}
]

ID_COUNTER = len(db_employees)


@app.get("/employees", response_model=list[EmployeePublic])
async def employees_database(
    *,
    skip: int | None = Query(0, ge=0),
    limit: int | None = Query(10, ge=10),
    department: Departments = Query(...)
):
    result = [
        employee for employee in db_employees
        if employee["department"] == department.value
    ]
    return result[skip:limit + skip]


@app.post("/register", response_model=EmployeePublic)
async def resiger_employee(
    *,
    employee: EmployeeCreate = Body(
        example={
            "username": "example_name",
            "email": "example@gmail.com",
            "password": "12345678@",
            "salary": 15000
        }
    ),
    department: Departments
):
    global ID_COUNTER
    ID_COUNTER += 1

    new_employee_data = employee.model_dump()
    new_employee_data["department"] = department.value
    result = {
        "id": ID_COUNTER,
        **new_employee_data
    }

    db_employees.append(result)

    return result


@app.get("/employee/{employee_id}", response_model=EmployeePublic)
async def search_for_employee(*, employee_id: int = Path(..., description="Please input your ID")):
    
    employees = next((
        employee for employee in db_employees
        if employee["id"] == employee_id
    ), None)

    if not employees:
        raise HTTPException(status_code=404, detail="NOT FOUND")

    return employees


@app.get(
    "/employee/{user_id}/secret",  
    response_model=EmployeeCreate
)
async def find_employee_id(
    user_id: int = Path(..., description="Please input your ID"),
    password: str = Query(..., min_length=8, description="Please input your password")
):
    
    founded_employee = next(
        (
            employee for employee in db_employees
            if employee["id"] == user_id and employee["password"] == password
        ), None
    )

    if not founded_employee:
        raise HTTPException(status_code=404, detail="WRONG ID OR PASSWORD")

    return founded_employee


@app.put("/employee/{user_id}/department")
async def change_department(
    *,
    user_id: int = Path(...),
    password: str = Query(..., min_length=8),
    department: Departments,
):
    founded_employee = next(
        (
            employee for employee in db_employees
            if employee["id"] == user_id and
            employee["password"] == password
        ), None
    )

    if not founded_employee:
        raise HTTPException(status_code=404, detail="WRONG ID OR PASSWORD")
    
    founded_employee.update({"department": department.value})

    return {
        "message": "Change successfully",
        "result": founded_employee
    }
    
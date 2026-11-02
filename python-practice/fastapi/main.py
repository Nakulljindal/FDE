from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Tea(BaseModel):
    id: int
    name: str
    origin: str

teas : List[Tea] = []

@app.get("/")
def read_root():
    return {"message" : "Welcome to Tea House"}

@app.get("/teas")
def get_teas():
    return teas

@app.post("/add_teas")
def add_tea(tea: Tea):
    teas.append(tea)
    print("Tea added successfully")
    return


@app.put("/teas/{tea_id}")
def update_tea(tea_id: int, updated_tea: Tea):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            teas[index] = updated_tea
            print("Tea updated successfully")
            return
    return {"Error" : "Tea not found"}

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            deleted = teas.pop(index)
            print("Tea deleted successfully")
            return deleted

    return {"Error": "Tea not found."}


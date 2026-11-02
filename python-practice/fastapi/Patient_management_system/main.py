from pydantic import BaseModel, Field, computed_field, model_validator
from typing import Optional, Annotated, Literal
import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Query
from datetime import date
from pathlib import Path

app = FastAPI()

PATIENTS_DATA = Path(__file__).with_name("patients.json")

class DOB(BaseModel):
    date : Annotated[int, Field(..., ge= 1, le= 31)]
    month : Annotated[int, Field(..., ge= 1, le=12, description="Birth month of the patient")]
    year : Annotated[int, Field(..., ge=1900, lt = 2026, description="Birth year of the patient", examples=[2004])]

    @model_validator(mode="after")
    def validate_date(self):
        try:
            dob = date(self.year, self.month, self.date)
        except ValueError:
            raise ValueError("Invalid Date of birth")   
        if dob > date.today():
            raise ValueError("Invalid Date of birth")
        return self


class Address(BaseModel):
    city : Annotated[str, Field(..., description="City of the patient", examples=["Meerut"])]
    state : Annotated[str, Field(..., description="State from which the patient belongs", examples=["Uttar Pradesh"])]

class Patient(BaseModel):
    id : Annotated[str, Field(..., description="ID of the patient", examples=[ "P001"])]
    name : Annotated[str, Field(..., description="Name of the patient" , examples=[ "Nakul Jindal"])]
    dob : Annotated[ DOB, Field(..., description="Date of birth. Note: Use commas to seperate", examples=[{"date" : 10, "month" : 12, "year" : 2004}])]
    address : Annotated[Address, Field(..., description="Address of the patient - city, state", examples=[{"city" : "Meerut", "state" : "Uttar pradesh"}])]
    gender : Annotated[Literal["Male", "Female", "Others"], Field(..., description="Gender of patient must be either male, female or others")]
    height : Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs", examples=[1.75])]
    weight : Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs", examples=[90.0])]

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.dob.year

        if(today.month, today.day) < (self.dob.month, self.dob.date):
            age -= 1

        return age

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight/(self.height ** 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 16:
            return "Severly underweight"
        elif self.bmi < 18.4:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        return "severly overweight"

class updateAddress(BaseModel):
    city : Annotated[Optional[str], Field(default= None, description="City of the patient", examples=["Meerut"])]
    state : Annotated[Optional[str], Field(default= None, description="State from which the patient belongs", examples=["Uttar Pradesh"])]

    @model_validator(mode="after")
    def validate_not_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self

class updatePatient(BaseModel):
    name: Optional[str] = None
    dob: Optional[DOB] = None
    address: Optional[updateAddress] = None
    gender: Optional[Literal["Male", "Female", "Others"]] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_not_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self

def load_data():
    try:
        if not PATIENTS_DATA.exists():
            with PATIENTS_DATA.open("w", encoding="utf-8") as file:
                json.dump({}, file)
        with PATIENTS_DATA.open("r", encoding= "utf-8") as file:
            patients = json.load(file)
        if not isinstance(patients, dict):
            raise HTTPException(status_code=500, detail="Invalid patients.json structure")
        return patients
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except (json.JSONDecodeError, OSError, ValueError):
        raise HTTPException(status_code=500)

def save_data(data):
    try:
        with PATIENTS_DATA.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    except OSError:
        raise HTTPException(status_code=500)

@app.get("/")
def home():
    return "Welcome to Patient management system"


@app.get("/view")
def view_patients():
    data = load_data()
    return data

@app.get("/sort")
def sort_patients(sort_by : str = Query(..., description= "sort on the basis of height, weight or bmi"), order : str = Query('asc', description= "Sort in order either ascending or descending")):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400, detail=f"Invalid sort by function. select from {valid_fields}")

    valid_order = ['asc', 'desc']

    if order not in valid_order:
        raise HTTPException(status_code=400, detail= f"Invalid order. select from {valid_order}")

    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(), key = lambda x : x.get(sort_by, 0), reverse= sort_order)

    return sorted_data



@app.post("/create")
def add_patient(patient : Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={'message' : 'Patient added successfully'})

@app.put("/update/{patient_id}")
def update_patient(patient_id : str, patient : updatePatient):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Invalid patient ID")

    existing_patient_data = data[patient_id] 

    updated_patient = patient.model_dump(exclude_unset=True)

    for key, value in updated_patient.items():

        if key == "address" and value is not None:
            existing_patient_data["address"].update(value)

        else:
            existing_patient_data[key] = value

    existing_patient_data['id'] = patient_id
    patient_new_obj = Patient(**existing_patient_data)
    existing_patient_data = patient_new_obj.model_dump(exclude=['id'])
    data[patient_id] = existing_patient_data
    save_data(data)
    return "Patient updated successfully"

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Invalid patient ID")

    del data[patient_id]
    save_data(data)
    return "Patient deleted successfully"
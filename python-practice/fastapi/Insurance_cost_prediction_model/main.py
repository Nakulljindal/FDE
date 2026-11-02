from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
from pydantic import BaseModel, computed_field, Field
import pickle
import pandas as pd 


# First we'll import our ML model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)


# Then we'll create our app object
app = FastAPI()


# Now we will create a pydantic model to validate user input and hereby create computed fields that are required

class userInput(BaseModel):
    age : Annotated[int, Field(..., ge = 0, lt = 100, description= 'Age of the user')]
    weight : Annotated[float, Field(..., gt = 0, description= 'Weight of the user')]
    height : Annotated[float, Field(..., gt = 0, lt = 3, description= 'Height of the user')]
    income_lpa : Annotated[float, Field(..., ge = 0, description= 'Annual salary of the user in LPA')]
    smoker : Annotated[bool, Field(...,  description= 'does user smoke? True or False')]
    city : Annotated[str, Field(..., description= 'city of the user from which they belong to')]
    occupation : Annotated[Literal['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job'], Field(..., description= 'Occupation of the user')]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker and self.bmi > 27:
            return 'medium'
        return 'low'

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle_aged'
        return 'senior'

    @computed_field
    @property
    def city_tier(self) -> int:
        tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
        tier_2_cities = [
                "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
                "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
                "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
                "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
                "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
                "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
            ]

        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        return 3


@app.post('/predict')
def predict_premium(data: userInput):
    input_df = pd.DataFrame([{
        'bmi' : data.bmi,
        'age_group' : data.age_group,
        'lifestyle_risk' : data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
    }]) 

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'Predicted_category' : prediction})
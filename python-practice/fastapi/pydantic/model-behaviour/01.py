from pydantic import BaseModel, field_validator, model_validator, computed_field


class User(BaseModel):
    usermame : str

    @field_validator(usermame)
    def username_length(cls , v):
        if len(v) < 4:
            raise ValueError("Username must be atleast 4 characters")
        return v


class SignupData(BaseModel):
    password : str
    confirm_password : str

    @model_validator(mode="after")
    def password_match(cls, values):
        if values.password != values.confirm_password:
            raise ValueError('Password do not match')
        return values 

class Product(BaseModel):
    price : float
    quantity : int

    @computed_field
    @property
    def total_price (self) -> float:
        return self.price * self.quantity
    
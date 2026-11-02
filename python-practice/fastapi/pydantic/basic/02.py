# TODO : Create Product model with id, name, price, in-stock

from pydantic import BaseModel

class Product(BaseModel):
    model_id : int
    model_name : str
    model_price : int
    in_stock : bool

product_data = {"model_id" : "101", "model_name" : "iphone", "model_price" : 99000, "in_stock" : "False"}

product = Product(**product_data)

print(product)
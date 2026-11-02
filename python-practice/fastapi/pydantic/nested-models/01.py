from typing import List, Optional
from pydantic import BaseModel

class Address(BaseModel):
    street : str
    city : str
    postal_code : str


class User(BaseModel):
    id : int
    name : str
    address : Address

class comment(BaseModel):
    id : int 
    content : str
    replies : Optional[List['comment']] = None

comment.model_rebuild()

address = Address(
    street = "Jahangirabad",
    city = "Bulandshahr",
    postal_code= "203394"
)

user = User(
    id = 1,
    name = "Nakul Jindal",
    address= address
)
print(user)

Comment = comment(
    id = 1,
    content = 'first comment',
    replies = [
        comment(id = 2, content='reply to first comment', replies = None)
    ]
)
print(Comment)
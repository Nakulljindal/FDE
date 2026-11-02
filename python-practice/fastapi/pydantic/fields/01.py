from pydantic import BaseModel
from typing import List, Dict, Optional

class cart(BaseModel):
    user_id : int
    items : List[str]
    quantity : Dict[str, int]

class blog_post(BaseModel):
    title : str
    content : str
    image_url : Optional[str] = None


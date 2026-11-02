### TODO : Create Employee model
# Fields:
#  - id: int
#  - name: str (minimum 3 chars)
#  - department: optional (str) and default - "General"
#  - salary: float (must be >= 10000)

from pydantic import BaseModel, Field
from typing import Optional

class employee(BaseModel):
    id : int
    name : str = Field(..., min_length=3) 
    dept : Optional[str] = "General"
    salary : float = Field(..., ge=10000)
    
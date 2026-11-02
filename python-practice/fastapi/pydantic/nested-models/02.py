# TODO: Create Course Model
# Each Course has modules
# Each Module has lessons

from pydantic import BaseModel
from typing import List, Optional

class Course(BaseModel):
    id : int
    course_name : str
    modules : List[Modules]

class Modules(BaseModel):
    module_name : str
    lessons : List[Lessons]

class Lessons(BaseModel):
    lesson_name : str
    content : Optional[str] = None

lesson1 = Lessons(
    lesson_name= "Arrays"
)
lesson2 = Lessons(
    lesson_name= "LinkedList"
)
lesson3 = Lessons(
    lesson_name="Stack"
)

lesson4 = Lessons(
    lesson_name="Pydantic"
)
lesson5 = Lessons(
    lesson_name="uvicorn"
)
lesson6 = Lessons(
    lesson_name="fastapi"
)
module1= Modules(
    module_name= "DSA",
    lessons=[
        lesson1, lesson2, lesson3
    ]
)
module2= Modules(
    module_name= "Python",
    lessons=[
        lesson4, lesson5, lesson6
    ]
)



course = Course(
    id= 1,
    course_name= "Btech",
    modules= [
        module1, module2
    ]
)
print(course)
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
        validate_by_alias=True,
    )

class Course(CamelModel):
    id: str
    title: str
    description: str
    credits: int
    is_elective: bool = False
    likes: int = 0

class Stats(CamelModel):
    total: int
    total_credits: int
    electives: int

class EnrollmentIn(CamelModel):
    course_id: str
    student_name: str = Field(min_length=2)

class Enrollment(EnrollmentIn):
    id: int

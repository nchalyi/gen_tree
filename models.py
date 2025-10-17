from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    mother_id: Optional[int] = None
    father_id: Optional[int] = None

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    mother_id: Optional[int] = None
    father_id: Optional[int] = None

class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True

class Person_FN(PersonBase):
    first_name: str

    class Config:
        from_attributes = True

class AncestorTree(BaseModel):
    id: int
    first_name: str
    last_name: str
    mother: Optional[Dict[str, Any]] = None
    father: Optional[Dict[str, Any]] = None
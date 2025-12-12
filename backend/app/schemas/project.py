from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime



class ProjectBase(BaseModel):
    name: str
    key: str

    description: Optional[str] = None



class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    created_at: datetime

class Config:
    orm_mode = True



class MemberAdd(BaseModel):
    email: str

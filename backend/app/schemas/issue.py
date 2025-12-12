from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class IssueStatus(str, Enum):
    open= "open"
    in_progress= "in_progress"
    resolved= "resolved"
    closed= "closed"


class Priority(str, Enum):
    low= "low"
    medium= "medium"
    high= "high"
    critical= "critical"


class IssueBase(BaseModel):
    title: str
    description: Optional[str] = None

    priority: Priority = Priority.medium
    status: IssueStatus = IssueStatus.open

    assignee_id: Optional[int] = None



class IssueCreate(IssueBase):
    pass



class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    priority: Optional[Priority] = None
    status: Optional[IssueStatus] = None

    assignee_id: Optional[int] = None



class CommentBase(BaseModel):
    body: str



class CommentCreate(CommentBase):
    pass



class CommentOut(CommentBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True



class IssueOut(IssueBase):
    id: int
    project_id: int
    reporter_id: int

    created_at: datetime
    updated_at: datetime

    comments: List[CommentOut] = []

    class Config:
        orm_mode = True
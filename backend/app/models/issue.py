from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..db import Base


class IssueStatus(str, enum.Enum):
    open= "open"
    in_progress= "in_progress"
    resolved = "resolved"
    closed= "closed"



class Priority(str, enum.Enum):
    low= "low"
    medium= "medium"
    high = "high"
    critical= "critical"



class Issue(Base):

    __tablename__ = "issues"

    id= Column(Integer, primary_key=True, index=True)
    project_id= Column(Integer, ForeignKey("projects.id"))

    title= Column(String, nullable=False)
    description= Column(Text)

    status= Column(Enum(IssueStatus), default = IssueStatus.open)
    priority= Column(Enum(Priority),   default = Priority.medium)

    reporter_id= Column(Integer, ForeignKey("users.id"))
    assignee_id= Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at= Column(DateTime, default = datetime.utcnow)
    updated_at= Column(DateTime, default = datetime.utcnow, onupdate=datetime.utcnow)


    project  = relationship("Project", back_populates = "issues")
    comments = relationship(
        "Comment",
        back_populates = "issue",
        cascade = "all, delete-orphan"
    )



class Comment(Base):

    __tablename__ = "comments"

    id= Column(Integer, primary_key=True, index=True)
    issue_id= Column(Integer, ForeignKey("issues.id"))
    author_id= Column(Integer, ForeignKey("users.id"))

    body= Column(Text, nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow)

    issue = relationship("Issue", back_populates = "comments")
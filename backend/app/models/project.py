from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..db import Base


class Role(str, enum.Enum):
    maintainer = "maintainer"
    member = "member"


class Project(Base):
    __tablename__ = "projects"

    id= Column(Integer, primary_key=True, index=True)
    name= Column(String, nullable=False)
    key = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default = datetime.utcnow)


    members= relationship(
        "ProjectMember",
        back_populates = "project",
        cascade = "all, delete-orphan"
    )

    issues= relationship(
        "Issue",
        back_populates = "project",
        cascade = "all, delete-orphan"
    )



class ProjectMember(Base):

    __tablename__ = "project_members"

    id= Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id= Column(Integer, ForeignKey("users.id"))
    role= Column(Enum(Role), default = Role.member)
    project    = relationship("Project", back_populates = "members")

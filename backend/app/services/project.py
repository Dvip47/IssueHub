from sqlalchemy.orm import Session

from ..models.project import Project, ProjectMember, Role
from ..schemas.project import ProjectCreate, MemberAdd
from ..models.user import User



def get_projects(db: Session, user_id: int):
    return (
        db.query(Project)
          .join(ProjectMember)
          .filter(ProjectMember.user_id == user_id)
          .all()
    )



def create_project(db: Session, project: ProjectCreate, user_id: int):

    record = Project(
        name= project.name,
        key= project.key,
        description= project.description
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    maintainer = ProjectMember(
        project_id = record.id,
        user_id= user_id,
        role= Role.maintainer
    )

    db.add(maintainer)
    db.commit()

    return record



def get_project_by_id(db: Session, project_id: int):
    return (
        db.query(Project)
          .filter(Project.id == project_id)
          .first()
    )



def add_member(db: Session, project_id: int, email: str):

    user = (
        db.query(User)
          .filter(User.email == email)
          .first()
    )

    if not user:
        return None

    existing = (
        db.query(ProjectMember)
          .filter(
              ProjectMember.project_id == project_id,
              ProjectMember.user_id == user.id
          )
          .first()
    )

    if existing:
        return existing


    member = ProjectMember(
        project_id = project_id,
        user_id= user.id,
        role= Role.member
    )

    db.add(member)
    db.commit()

    return member

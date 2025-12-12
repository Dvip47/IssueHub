from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from typing import List

from ..db import get_db
from ..schemas.project import ProjectCreate, ProjectOut, MemberAdd
from ..schemas.user import UserOut
from ..schemas.issue import IssueCreate, IssueOut

from ..models.user import User
from ..models.project import ProjectMember

from ..services.project import (
    create_project,
    get_projects,
    add_member,
    get_project_by_id
)

from ..services.issue import (
    create_issue,
    get_issues
)

from .users import get_current_user


router = APIRouter()

@router.post("", response_model = ProjectOut)
def create_new_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("hello",db, project, current_user.id)
    try:
        return create_project(db, project, current_user.id)

    except IntegrityError:
        raise HTTPException(
            status_code = 400,
            detail = "Project with this key already exist"
        )



@router.get("", response_model = List[ProjectOut])
def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_projects(db, current_user.id)


@router.post("/{project_id}/members", response_model = ProjectOut)
def add_project_member(
    project_id: int,
    member: MemberAdd,

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(404, detail = "Project not found")


    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id
        )
        .first()
    )

    if not membership or membership.role != "maintainer":
        raise HTTPException(403, detail = "Not authorized")


    added = add_member(db, project_id, member.email)

    if not added:
        raise HTTPException(404, detail = "User not found")

    return project



@router.get("/{id}", response_model = ProjectOut)
def get_project_details(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = get_project_by_id(db, id)

    if not project:
        raise HTTPException(404, detail = "Project not found")


    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == id,
            ProjectMember.user_id == current_user.id
        )
        .first()
    )

    if not membership:
        raise HTTPException(403, detail = "No member")

    return project


@router.post("/{project_id}/issues", response_model = IssueOut)
def create_project_issue(
    project_id: int,
    issue: IssueCreate,

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(404, detail = "Project not found")


    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id
        )
        .first()
    )

    if not membership:
        raise HTTPException(403, detail = "Not authorize")

    return create_issue(db, issue, project_id, current_user.id)


print("hello running")
@router.get("/{project_id}/issues", response_model = List[IssueOut])
def list_project_issues(
    project_id: int,

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(404, detail = "Project not found")


    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id
        )
        .first()
    )

    if not membership:
        raise HTTPException(403, detail = "Not authorized")

    return get_issues(db, project_id)
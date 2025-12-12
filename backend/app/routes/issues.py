from fastapi import (
    APIRouter, Depends, HTTPException,
    status, Query
)

from sqlalchemy.orm import Session
from typing import List, Optional
from ..db import get_db


from ..schemas.issue import (
    IssueCreate, IssueUpdate, IssueOut,
    CommentCreate, CommentOut
)
from ..models.user import User
from ..models.project import ProjectMember, Project
from ..models.issue import Issue, Comment

from ..services.issue import (
    create_issue, get_issue, update_issue,
    create_comment, get_comments
)

from .users import get_current_user
from ..services.project import get_project_by_id

router = APIRouter()

@router.get("", response_model = List[IssueOut])
def list_issues(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    query = db.query(Issue)


    if project_id:

        membership = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
            .first()
        )

        if not membership:
            pass
        query = query.filter(Issue.project_id == project_id)
    else:
        query = query.filter(Issue.assignee_id == current_user.id)
    if status:
        query = query.filter(Issue.status == status)

    if priority:
        query = query.filter(Issue.priority == priority)

    if search:
        query = query.filter(
            Issue.title.contains(search)
            | Issue.description.contains(search)
        )
    return query.all()



@router.post("", response_model = IssueOut)
def create_new_issue(
    issue: IssueCreate,
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

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

    return create_issue(db, issue, project_id, current_user.id)



@router.get("/{issue_id}", response_model = IssueOut)
def get_issue_detail(
    issue_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    issue = get_issue(db, issue_id)

    if not issue:
        raise HTTPException(404, detail = "Issue not found")

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == issue.project_id,
            ProjectMember.user_id == current_user.id
        )
        .first()
    )

    if not membership:
        raise HTTPException(403, detail = "Not authorized to view this issue")

    return issue



@router.patch("/{issue_id}", response_model = IssueOut)
def update_issue_detail(
    issue_id: int,
    updates: IssueUpdate,

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    issue = get_issue(db, issue_id)

    if not issue:
        raise HTTPException(404, detail = "Issue not found")
    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == issue.project_id,
            ProjectMember.user_id == current_user.id
        )
        .first()
    )

    if not membership:
        raise HTTPException(403, detail = "Not authorized")


    if membership.role != "maintainer":
        if updates.status is not None or updates.assignee_id is not None:
            raise HTTPException(
                403,
                detail = "Only maintainers can update status or assignee"
            )
    return update_issue(db, issue_id, updates)



@router.delete("/{issue_id}")
def delete_issue(
    issue_id: int,

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    issue = get_issue(db, issue_id)

    if not issue:
        raise HTTPException(404, detail = "Issue not found")


    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == issue.project_id,
            ProjectMember.user_id == current_user.id
        )
        .first()
    )

    if not membership or membership.role != "maintainer":
        raise HTTPException(403, detail = "Only maintainers can delete issues")


    db.delete(issue)
    db.commit()

    return { "message": "Issue deleted" }



@router.get("/{issue_id}/comments", response_model = List[CommentOut])
def get_issue_comments(
    issue_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    issue = get_issue(db, issue_id)

    if not issue:
        raise HTTPException(404, detail = "Issue not found")

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == issue.project_id,
            ProjectMember.user_id == current_user.id
        )
        .first()
    )

    if not membership:
        raise HTTPException(403, detail = "Not authorized")

    return get_comments(db, issue_id)



@router.post("/{issue_id}/comments", response_model = CommentOut)
def add_issue_comment(
    issue_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    issue = get_issue(db, issue_id)

    if not issue:
        raise HTTPException(404, detail = "Issue not found")

    membership = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == issue.project_id,
            ProjectMember.user_id == current_user.id
        )
        .first()
    )

    if not membership:
        raise HTTPException(403, detail = "Not authorized")


    return create_comment(db, issue_id, comment, current_user.id)

from sqlalchemy.orm import Session
from datetime import datetime

from ..models.issue import Issue, Comment
from ..schemas.issue import (
    IssueCreate, IssueUpdate, CommentCreate
)


def get_issues(db: Session, project_id: int):
    return (
        db.query(Issue)
          .filter(Issue.project_id == project_id)
          .all()
    )



def create_issue(
    db: Session,
    issue: IssueCreate,
    project_id: int,
    reporter_id: int
):
    record = Issue(
        project_id= project_id,
        title= issue.title,
        description= issue.description,
        status= issue.status.value,
        priority= issue.priority.value,
        reporter_id= reporter_id,
        assignee_id  = issue.assignee_id
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record



def get_issue(db: Session, issue_id: int):
    return (
        db.query(Issue)
          .filter(Issue.id == issue_id)
          .first()
    )



def update_issue(db: Session, issue_id: int, updates: IssueUpdate):

    db_issue = get_issue(db, issue_id)

    if not db_issue:
        return None

    changes = updates.dict(exclude_unset = True)

    for field, value in changes.items():
        setattr(db_issue, field, value)

    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)

    return db_issue



def create_comment(
    db: Session,
    issue_id: int,
    comment: CommentCreate,
    author_id: int
):
    record = Comment(
        issue_id= issue_id,
        author_id= author_id,
        body= comment.body
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record



def get_comments(db: Session, issue_id: int):
    return (
        db.query(Comment)
          .filter(Comment.issue_id == issue_id)
          .all()
    )

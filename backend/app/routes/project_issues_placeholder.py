
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..schemas.issue import IssueCreate, IssueOut
from ..models.user import User
from ..models.project import ProjectMember
from ..services.issue import create_issue, get_issues
from .users import get_current_user
from ..services.project import get_project_by_id
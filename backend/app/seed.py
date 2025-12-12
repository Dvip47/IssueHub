from app.db import SessionLocal
from app.models.user import User
from app.models.project import Project, ProjectMember
from app.models.issue import Issue
from app.core.security import get_password_hash

import sys
def seed():

    db = SessionLocal() 
    if db.query(User).first():
        print("Data already exists.")
        return    print("Seeding data...")
    # user
    u1 = User(
        email           = "admin@example.com",
        name            = "Admin User",
        hashed_password = get_password_hash("password")
    )

    u2 = User(
        email           = "dev@example.com",
        name            = "Developer",
        hashed_password = get_password_hash("password")
    )

    db.add(u1)
    db.add(u2)
    db.commit()

    db.refresh(u1)
    db.refresh(u2)

    # project
    p1 = Project(
        name        = "IssueHub Core",
        key         = "IHC",
        description = "Main development project"
    )

    db.add(p1)
    db.commit()
    db.refresh(p1)



    # add new member
    m1 = ProjectMember(
        project_id = p1.id,
        user_id    = u1.id,
        role       = "maintainer"
    )

    m2 = ProjectMember(
        project_id = p1.id,
        user_id    = u2.id,
        role       = "member"
    )

    db.add(m1)
    db.add(m2)
    db.commit()



    # issues
    i1 = Issue(
        project_id  = p1.id,
        title       = "Implement Login",
        description = "Need JWT auth flow.",
        reporter_id = u1.id,
        assignee_id = u2.id,
        priority    = "high",
        status      = "closed"
    )

    i2 = Issue(
        project_id  = p1.id,
        title       = "Fix UI Bugs",
        description = "CSS is broken on mobile.",
        reporter_id = u2.id,
        assignee_id = u2.id,
        priority    = "medium",
        status      = "open"
    )

    db.add(i1)
    db.add(i2)
    db.commit()
    print("Seeding complete.")
    db.close()
if __name__ == "__main__":
    seed()

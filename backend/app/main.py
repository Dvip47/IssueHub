from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db import engine, Base
from .routes import auth, users, projects, issues
from .core.config import settings


app = FastAPI(
    title = settings.PROJECT_NAME
)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],  
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)
app.include_router(auth.router,     prefix="/api/auth",     tags=["auth"])
app.include_router(users.router,    prefix="/api/me",       tags=["users"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(issues.router,   prefix="/api/issues",   tags=["issues"])



@app.get("/")
def read_root():
    return {
        "message": "Welcome to IssueHub API"
    }

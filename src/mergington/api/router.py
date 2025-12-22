from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict
from mergington.ports.activity_repository import ActivityRepository
from mergington.usecases.signup import SignupService
from mergington.domain.exceptions import ActivityNotFound, AlreadySignedUp, ActivityFull

router = APIRouter()

# Placeholder dependency to be overridden by application wiring (main.create_app)
def get_repo_dep() -> ActivityRepository:
    raise RuntimeError("Repository dependency not wired")


@router.get("/activities")
def list_activities(repo: ActivityRepository = Depends(get_repo_dep)) -> Dict[str, dict]:
    activities = repo.list_activities()
    return {
        name: {
            "description": a.description,
            "schedule": a.schedule,
            "max_participants": a.max_participants,
            "participants": a.participants,
        }
        for name, a in activities.items()
    }


@router.post("/activities/{activity_name}/signup")
def signup(activity_name: str, email: str = Query(..., description="Student email"),
           repo: ActivityRepository = Depends(get_repo_dep)):
    service = SignupService(repo)
    try:
        service.signup(activity_name, email)
    except ActivityNotFound:
        raise HTTPException(status_code=404, detail="Activity not found")
    except AlreadySignedUp:
        raise HTTPException(status_code=400, detail="Student already signed up")
    except ActivityFull:
        raise HTTPException(status_code=400, detail="Activity is full")
    return {"message": f"Signed up {email} for {activity_name}"}

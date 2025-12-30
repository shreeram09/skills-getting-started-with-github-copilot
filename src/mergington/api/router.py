from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Query

from mergington.domain.exceptions import ActivityFull, ActivityNotFound, AlreadySignedUp
from mergington.ports.activity_repository import ActivityRepository
from mergington.usecases.signup import SignupService

router = APIRouter()

# The router will call `get_repo_dep()` to obtain the repository instance.
# `DEFAULT_REPO` is intended to be set by application wiring (e.g. in
# `src.main.create_app`) so the dependency can return a concrete adapter.
DEFAULT_REPO: ActivityRepository | None = None


def get_repo_dep() -> ActivityRepository:
    if DEFAULT_REPO is None:
        raise RuntimeError("Repository dependency not wired")
    return DEFAULT_REPO


@router.get("/activities")
def list_activities(
    repo: ActivityRepository = Depends(get_repo_dep),
) -> Dict[str, dict]:
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
def signup(
    activity_name: str,
    email: str = Query(..., description="Student email"),
    repo: ActivityRepository = Depends(get_repo_dep),
):
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

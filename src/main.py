from fastapi import FastAPI
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from mergington.adapters.inmemory_repository import InMemoryActivityRepository
from mergington.domain.models import Activity
from mergington.api import router as activities_router
from mergington.api.router import get_repo_dep
from mergington.logging_config import configure_logging


def create_initial_activities() -> dict:
    return {
        "Chess Club": Activity(
            name="Chess Club",
            description="Learn strategies and compete in chess tournaments",
            schedule="Fridays, 3:30 PM - 5:00 PM",
            max_participants=12,
            participants=["michael@mergington.edu", "daniel@mergington.edu"],
        ),
        "Programming Class": Activity(
            name="Programming Class",
            description="Learn programming fundamentals and build software projects",
            schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            max_participants=20,
            participants=["emma@mergington.edu", "sophia@mergington.edu"],
        ),
        "Gym Class": Activity(
            name="Gym Class",
            description="Physical education and sports activities",
            schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            max_participants=30,
            participants=["john@mergington.edu", "olivia@mergington.edu"],
        ),
        "Soccer Team": Activity(
            name="Soccer Team",
            description="Join the school soccer team and compete in local leagues",
            schedule="Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            max_participants=22,
            participants=["lucas@mergington.edu", "mia@mergington.edu"],
        ),
        "Basketball Club": Activity(
            name="Basketball Club",
            description="Practice basketball skills and play friendly matches",
            schedule="Wednesdays, 3:30 PM - 5:00 PM",
            max_participants=15,
            participants=["liam@mergington.edu", "ava@mergington.edu"],
        ),
        "Drama Club": Activity(
            name="Drama Club",
            description="Participate in school plays and improve acting skills",
            schedule="Mondays, 4:00 PM - 5:30 PM",
            max_participants=18,
            participants=["noah@mergington.edu", "isabella@mergington.edu"],
        ),
        "Art Workshop": Activity(
            name="Art Workshop",
            description="Explore painting, drawing, and other visual arts",
            schedule="Fridays, 2:00 PM - 3:30 PM",
            max_participants=16,
            participants=["amelia@mergington.edu", "benjamin@mergington.edu"],
        ),
        "Debate Team": Activity(
            name="Debate Team",
            description="Develop public speaking and argumentation skills",
            schedule="Thursdays, 3:30 PM - 5:00 PM",
            max_participants=10,
            participants=["charlotte@mergington.edu", "jackson@mergington.edu"],
        ),
        "Math Olympiad": Activity(
            name="Math Olympiad",
            description="Prepare for math competitions and solve challenging problems",
            schedule="Mondays, 3:30 PM - 5:00 PM",
            max_participants=12,
            participants=["elijah@mergington.edu", "harper@mergington.edu"],
        ),
    }


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="Mergington High School API",
        description="API for viewing and signing up for extracurricular activities",
    )
    # Mount static directory from src/static (keeps compatibility with original layout)
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(Path(__file__).parent, "static")),
        name="static",
    )

    # Wire the in-memory repository as the default adapter
    repo = InMemoryActivityRepository(initial=create_initial_activities())

    # Simple dependency override for the router module
    def _get_repo():
        return repo

    # Wire the repository into the router by setting its module-level DEFAULT_REPO
    # value. The router's `get_repo_dep` will read this variable at runtime.
    activities_router.DEFAULT_REPO = repo
    app.include_router(activities_router.router)
    return app


app = create_app()


if __name__ == "__main__":
    # For local development prefer:
    #   uvicorn src.main:app --reload
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

from threading import Lock
from typing import Dict

from mergington.domain.models import Activity
from mergington.ports.activity_repository import ActivityRepository


class InMemoryActivityRepository(ActivityRepository):
    def __init__(self, initial: Dict[str, Activity] | None = None) -> None:
        self._lock = Lock()
        # store Activity instances keyed by their name
        self._activities: Dict[str, Activity] = initial or {}

    def list_activities(self) -> Dict[str, Activity]:
        # Return the internal mapping (shallow) — for production consider defensive copies
        return self._activities

    def get_activity(self, name: str) -> Activity | None:
        return self._activities.get(name)

    def save(self, activity: Activity) -> None:
        with self._lock:
            self._activities[activity.name] = activity

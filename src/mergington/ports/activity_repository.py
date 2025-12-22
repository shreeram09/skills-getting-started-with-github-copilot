from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict
from mergington.domain.models import Activity


class ActivityRepository(ABC):
    @abstractmethod
    def list_activities(self) -> Dict[str, Activity]:
        ...

    @abstractmethod
    def get_activity(self, name: str) -> Activity | None:
        ...

    @abstractmethod
    def save(self, activity: Activity) -> None:
        ...

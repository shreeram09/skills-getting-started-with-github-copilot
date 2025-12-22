from mergington.ports.activity_repository import ActivityRepository
from mergington.domain.exceptions import ActivityNotFound, AlreadySignedUp, ActivityFull


class SignupService:
    def __init__(self, repo: ActivityRepository) -> None:
        self.repo = repo

    def signup(self, activity_name: str, email: str) -> None:
        activity = self.repo.get_activity(activity_name)
        if activity is None:
            raise ActivityNotFound(activity_name)
        if email in activity.participants:
            raise AlreadySignedUp(email)
        if activity.is_full():
            raise ActivityFull(activity_name)
        activity.add_participant(email)
        self.repo.save(activity)

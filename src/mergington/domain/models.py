from dataclasses import dataclass, field
from typing import List


@dataclass
class Activity:
    name: str
    description: str
    schedule: str
    max_participants: int
    participants: List[str] = field(default_factory=list)

    def is_full(self) -> bool:
        return len(self.participants) >= self.max_participants

    def add_participant(self, email: str) -> None:
        if email in self.participants:
            raise ValueError("Student already signed up")
        if self.is_full():
            raise ValueError("Activity is full")
        self.participants.append(email)

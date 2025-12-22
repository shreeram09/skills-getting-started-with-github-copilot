class ActivityNotFound(Exception):
    """Raised when an activity cannot be found."""
    pass


class AlreadySignedUp(Exception):
    """Raised when a student is already signed up for an activity."""
    pass


class ActivityFull(Exception):
    """Raised when an activity has reached its maximum participants."""
    pass

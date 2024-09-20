from datetime import datetime

from src.core.exceptions import DateTimeWithoutTimezoneError


def validate_timezone(datetime: datetime, error_message: str = "Obj does not have timezone"):
    """raise: DateTimeWithoutTimezoneError."""
    if datetime.tzinfo is None:
        raise DateTimeWithoutTimezoneError(error_message)

    return datetime

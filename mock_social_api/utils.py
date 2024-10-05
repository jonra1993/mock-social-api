from datetime import datetime
from mock_social_api.constants import mock_users
from fastapi import HTTPException
import pytz

from mock_social_api.schemas.instagram_schema import IUser


def get_user_data(username: str) -> IUser:
    """Retrieve user data or raise an error if not found."""
    if username not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist")
    return mock_users[username]

def check_privacy(user_data: IUser) -> None:
    """Check if the user's account is private."""
    if user_data.private:
        raise HTTPException(status_code=403, detail="It seems like you have a private account. Your account needs to be public to complete the missions.")
    
def get_france_midnight() -> datetime:
    """Get today's midnight in France timezone."""
    france_tz = pytz.timezone("Europe/Paris")
    now = datetime.now(france_tz)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


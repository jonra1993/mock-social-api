from enum import Enum
from fastapi import APIRouter, HTTPException, Request
import httpx
from mock_social_api.schemas.response_schema import ITiktokResponseActivity, IResponseCounter, IResponseLatestPost
from mock_social_api.constants import mock_users

router = APIRouter()


# Enum for time frame selection
class TimeFrame(str, Enum):
    today_midnight = "today_midnight"
    last_sunday_midnight = "last_sunday_midnight"


# Mock function for TikTok API integration (replace with actual API call)
def get_tiktok_posts(username: str, hashtag: str, timeframe: TimeFrame) -> int:
    """
    Simulates fetching the number of posts for a given TikTok user using a specific hashtag.
    Replace this with the actual TikTok API call.
    """
    if username == "user5":
        raise HTTPException(status_code=404, detail="Account does not exist")
    if username == "user4":
        raise HTTPException(status_code=403, detail="Account is private")
    if username == "user1" and hashtag == "#vacation" and timeframe == TimeFrame.last_sunday_midnight:
        return 2
    if username == "user2" and hashtag == "#vacation" and timeframe == TimeFrame.today_midnight:
        return 0
    if username == "user3":
        return 0

    return 0


# TikTok route for counting posts with a hashtag
@router.get("/count-posts", response_model=IResponseCounter)
async def count_tiktok_posts(
    username: str,
    hashtag: str,
    timeframe: TimeFrame = TimeFrame.last_sunday_midnight
) -> IResponseCounter:
    """
    Counts the number of TikTok posts a user has made with a given hashtag since a specified time frame.

    **Parameters:**
    - `username` (str): TikTok username of the account to check.
    - `hashtag` (str): The hashtag to search for in the user's posts.
    - `timeframe` (TimeFrame, optional): The time frame from which to count posts (default: `last_sunday_midnight`).

    **Returns:**
    - `IResponseCounter`: A response model containing:
        - `result` (int): The number of posts with the given hashtag since the selected time frame.
        - `username` (str | None): The username for reference.

    **Raises:**
    - `HTTPException` 404: If the account does not exist.
    - `HTTPException` 403: If the account is private.

    **Example Requests:**

    - **Case 1**: User has posts with the hashtag.
        - **Input**: `username=user1`, `hashtag=#vacation`, `timeframe=last_sunday_midnight`
        - **Output**: `{"result": 2, "username": "user1"}`

    - **Case 2**: User has posts but no matching hashtag.
        - **Input**: `username=user2`, `hashtag=#vacation`, `timeframe=today_midnight`
        - **Output**: `{"result": 0, "username": "user2"}`

    - **Case 3**: User has no posts.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: `{"result": 0, "username": "user3"}`

    - **Case 4**: User's account is private.
        - **Input**: `username=user4`, `hashtag=#vacation`, `timeframe=last_sunday_midnight`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Case 5**: Non-existing account.
        - **Input**: `username=user5`, `hashtag=#vacation`, `timeframe=today_midnight`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """
    # Fetch the count of posts using the mock function (replace with actual implementation)
    try:
        count = get_tiktok_posts(username, hashtag, timeframe)
        return IResponseCounter(result=count, username=username)
    except HTTPException as e:
        raise e



# Mock function for TikTok API data (replace with actual API call)
def get_tiktok_daily_activity(username: str, hashtag: str) -> ITiktokResponseActivity:
    """
    Simulates fetching the daily activity of a TikTok user. Replace this function with the actual TikTok API call.
    """
    if username == "user5":
        raise HTTPException(status_code=404, detail="Account does not exist")
    if username == "user4":
        raise HTTPException(status_code=403, detail="Account is private")

    # Hardcoded responses for specific test cases
    if username == "user1" and hashtag == "#vacation":
        return ITiktokResponseActivity(
            followers=150,
            posts_with_hashtag=1,
            total_likes=18,
            username=username
        )
    elif username == "user6" and hashtag == "#vacation":
        return ITiktokResponseActivity(
            followers=200,
            posts_with_hashtag=0,
            total_likes=0,
            username=username
        )
    elif username == "user1" and hashtag == "#travel":
        return ITiktokResponseActivity(
            followers=150,
            posts_with_hashtag=1,
            total_likes=10,
            username=username
        )
    elif username == "user2" and hashtag == "#vacation":
        return ITiktokResponseActivity(
            followers=200,
            posts_with_hashtag=0,
            total_likes=20,
            username=username
        )
    elif username == "user3" and hashtag == "#vacation":
        return ITiktokResponseActivity(
            followers=50,
            posts_with_hashtag=0,
            total_likes=0,
            username=username
        )

    # Default response for non-matching cases
    raise HTTPException(status_code=404, detail="Account does not exist")

@router.get("/daily-activity", response_model=ITiktokResponseActivity)
async def daily_activity(
    username: str,
    hashtag: str
) -> ITiktokResponseActivity:
    """
    Tracks the daily activity of a TikTok user's posts mentioning a specific hashtag over the last 24 hours.

    **Parameters:**
    - `username` (str): TikTok username of the account to check.
    - `hashtag` (str): The hashtag to search for in the user's posts.

    **Returns:**
    - `ITiktokResponseActivity`: An object containing the daily activity statistics:
        - `followers` (int): The number of followers the user has.
        - `posts_with_hashtag` (int): Count of posts/reels using the hashtag in the last 24 hours.
        - `total_likes` (int): Total number of likes for the posts with the hashtag.
        - `username` (str): The username for reference.

    **Raises:**
    - `HTTPException` 404: If the account does not exist.
    - `HTTPException` 403: If the account is private.
    
    **Example Requests:**

    - **Scenario 1**: User has posted with the hashtag.
        - **Input**: `username=user1`, `hashtag=#vacation`
        - **Output**: `{"followers": 150, "posts_with_hashtag": 1, "total_likes": 18, "username": "user1"}`

    - **Scenario 2**: User has posted only a post with the hashtag.
        - **Input**: `username=user6`, `hashtag=#vacation`
        - **Output**: `{"followers": 200, "posts_with_hashtag": 0, "total_likes": 0, "username": "user6"}`

    - **Scenario 3**: User has posted only a post with the hashtag.
        - **Input**: `username=user1`, `hashtag=#travel`
        - **Output**: `{"followers": 150, "posts_with_hashtag": 1, "total_likes": 10, "username": "user1"}`

    - **Scenario 4**: User hasn’t posted in the last 24 hours but has previous posts.
        - **Input**: `username=user2`, `hashtag=#vacation`
        - **Output**: `{"followers": 200, "posts_with_hashtag": 0, "total_likes": 20, "username": "user2"}`

    - **Scenario 5**: User hasn’t posted anything and has no previous posts.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: `{"followers": 50, "posts_with_hashtag": 0, "total_likes": 0, "username": "user3"}`

    - **Scenario 6**: User’s account is private.
        - **Input**: `username=user4`, `hashtag=#vacation`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Scenario 7**: User’s account doesn’t exist.
        - **Input**: `username=user5`, `hashtag=#vacation`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """
    try:
        # Fetch the activity data using the mock function (replace with actual API call)
        activity = get_tiktok_daily_activity(username, hashtag)
        return activity
    except HTTPException as e:
        raise e

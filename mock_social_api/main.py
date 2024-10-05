from enum import Enum
from typing import Annotated, Union
import pytz
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timedelta

# Mock database of users with posts/reels and stories
mock_users = {
    "andrealbriziom": {
        "stories": [],
        "posts": [
            {
                "content": "Just chilling at the beach #vacation",
                "hashtags": ["#vacation"],
                "timestamp": "2024-10-02T10:00:00",
                "likes": 10,
                "link": "https://instagram.com/p/123456789",
                "comments": []
            },
            {
                "content": "Exploring the mountains",
                "hashtags": [],
                "timestamp": "2024-10-03T10:00:00",
                "likes": 12,
                "link": "https://instagram.com/p/987654321",
                "comments": []
            },
            {
                "content": "Weekend fun #vacation",
                "hashtags": ["#vacation"],
                "timestamp": "2024-10-04T08:00:00",
                "likes": 7,
                "link": "https://instagram.com/p/112233445",
                "comments": []
            }
        ],
        "private": False,
        "followers": 150,
    },
    "user1": {
        "stories": [
            {"content": "Check out this #vacation!", "hashtags": ["#vacation"], "timestamp": "2024-10-03T21:30:00", "likes": 5},
            {"content": "Another day, another adventure #vacation", "hashtags": ["#vacation"], "timestamp": "2024-10-04T08:00:00", "likes": 3},
        ],
        "posts": [
            {"content": "Just chilling at the beach #vacation", "hashtags": ["#vacation"], "timestamp": "2024-10-02T10:00:00", "likes": 10},
            {"content": "Exploring the mountains", "hashtags": [], "timestamp": "2024-10-03T10:00:00", "likes": 12},
            {"content": "Weekend fun #vacation", "hashtags": ["#vacation"], "timestamp": "2024-10-06T09:00:00", "likes": 7},
        ],
        "private": False,
        "followers": 150,
    },
    "user2": {
        "stories": [
            {"content": "Just chilling", "hashtags": [], "timestamp": "2024-10-04T10:00:00", "likes": 1},
        ],
        "posts": [
            {"content": "A day well spent #travel", "hashtags": ["#travel"], "timestamp": "2024-10-01T12:00:00", "likes": 20},
        ],
        "private": False,
        "followers": 200,
    },
    "user3": {
        "stories": [],
        "posts": [],
        "private": True,  # private account
        "followers": 50,
    },
}


app = FastAPI()


# Enum for time frame selection
class TimeFrame(str, Enum):
    today_midnight = "today_midnight"
    last_sunday_midnight = "last_sunday_midnight"

def get_user_data(username: str) -> dict[str, Union[list[dict[str, Union[str, list[str], int]]], bool, int]]:
    """Retrieve user data or raise an error if not found."""
    if username not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist")
    return mock_users[username]

def check_privacy(user_data: dict[str, Union[list[dict[str, Union[str, list[str], int]]], bool, int]]) -> None:
    """Check if the user's account is private."""
    if user_data["private"]:
        raise HTTPException(status_code=403, detail="It seems like you have a private account. Your account needs to be public to complete the missions.")

def get_france_midnight() -> datetime:
    """Get today's midnight in France timezone."""
    france_tz = pytz.timezone("Europe/Paris")
    now = datetime.now(france_tz)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)

@app.get("/")
def read_root():
    """
    Root endpoint to verify that the API is up.
    
    Returns:
    --------
    status : str
        A string indicating the API status.
    """
    return {"status": "active"}

@app.get("/check-story")
async def check_story(
    username: str,
    hashtag: str,
):
    """
    Checks if a user has a story with a given hashtag.
    
    Parameters:
    -----------
    username : str
        The username of the account to check.
    hashtag : str
        The hashtag to search for in the user's stories.
    
    Raises:
    -------
    HTTPException
        If the account does not exist (404).
        If the account is private (403).
    
    Returns:
    -------
    result : dict
        A dictionary indicating whether the user has a story with the given hashtag.

    Test Cases:
    -----------
    - **Case 1**: User with stories and the hashtag exists.
        - **Input**: `username=user1`, `hashtag=#vacation`
        - **Output**: `{"result": "yes"}`

    - **Case 2**: User with stories but the hashtag does not exist.
        - **Input**: `username=user1`, `hashtag=#travel`
        - **Output**: `{"result": "no"}`

    - **Case 3**: User with no stories.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: `{"result": "no"}`

    - **Case 4**: User's account is private.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Case 5**: Non-existing account.
        - **Input**: `username=user4`, `hashtag=#vacation`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """
    
    if username not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist")
    
    user_data = mock_users[username]
    
    if user_data["private"]:
        raise HTTPException(status_code=403, detail="Account is private")
    
    if not user_data["stories"]:
        return {"result": "no"}

    for story in user_data["stories"]:
        if hashtag in story["hashtags"]:
            return {"result": "yes"}
    
    return {"result": "no"}

@app.get("/count-stories")
async def count_stories(
    username: str,
    hashtag: str,
):
    """
    Counts how many stories a user has posted with a given hashtag since last midnight (French time).
    
    Parameters:
    -----------
    username : str
        The username of the account to check.
    hashtag : str
        The hashtag to search for in the user's stories since midnight.
    
    Raises:
    -------
    HTTPException
        If the account does not exist (404).
        If the account is private (403).
    
    Returns:
    -------
    result : dict
        A dictionary indicating the number of stories with the given hashtag.
    
    Test Cases:
    -----------
    - **Case 1**: User with stories that match the hashtag.
        - **Input**: `username=user1`, `hashtag=#vacation`
        - **Output**: `{"result": "yes", "number": 2}`

    - **Case 2**: User with stories but no matching hashtag.
        - **Input**: `username=user2`, `hashtag=#vacation`
        - **Output**: `{"result": "no"}`

    - **Case 3**: User with no stories.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: `{"result": "no"}`

    - **Case 4**: User's account is private.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Case 5**: Non-existing user.
        - **Input**: `username=user4`, `hashtag=#vacation`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """
    
    if username not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist")
    
    user_data = mock_users[username]
    
    if user_data["private"]:
        raise HTTPException(status_code=403, detail="Account is private")
    
    # Get current time in France timezone (UTC+2 or UTC+1 depending on daylight saving time)
    france_midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=2)

    count = 0
    for story in user_data["stories"]:
        story_time = datetime.fromisoformat(story["timestamp"])
        if story_time >= france_midnight and hashtag in story["hashtags"]:
            count += 1

    if count > 0:
        return {"result": "yes", "number": count}
    elif any(story["hashtags"] for story in user_data["stories"]):
        return {"result": "no"}
    else:
        return {"result": "no"}


@app.get("/count-posts")
async def count_posts(
    username: str,
    hashtag: str,
    timeframe: TimeFrame = TimeFrame.last_sunday_midnight
):
    """
    Counts how many posts or reels a user has posted with a given hashtag 
    since a specified time frame.

    Parameters:
    -----------
    username : str
        The username of the account to check.
    hashtag : str
        The hashtag to search for in the user's posts.
    timeframe : TimeFrame
        The time frame from which to count posts.
    
    Raises:
    -------
    HTTPException
        If the account does not exist (404).
        If the account is private (403).
    
    Returns:
    -------
    result : dict
        A dictionary indicating the number of posts with the given hashtag since the selected time frame.
    
    Test Cases:
    -----------
    - **Case 1**: User has posts with the hashtag.
        - **Input**: `username=user1`, `hashtag=#vacation`, `timeframe=last_sunday_midnight`
        - **Output**: `{"result": "yes", "number": 2}`

    - **Case 2**: User has posts but no matching hashtag.
        - **Input**: `username=user2`, `hashtag=#vacation`, `timeframe=today_midnight`
        - **Output**: `{"result": "no"}`

    - **Case 3**: User has no posts.
        - **Input**: `username=user3`, `hashtag=#vacation`, `timeframe=today_midnight`
        - **Output**: `{"result": "no"}`

    - **Case 4**: User's account is private.
        - **Input**: `username=user3`, `hashtag=#vacation`, `timeframe=last_sunday_midnight`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Case 5**: Non-existing account.
        - **Input**: `username=user4`, `hashtag=#vacation`, `timeframe=today_midnight`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """

    if username not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist")
    
    user_data = mock_users[username]
    
    if user_data["private"]:
        raise HTTPException(status_code=403, detail="Account is private")
    
    if not user_data["posts"]:
        return {"result": "no"}

    # Get the current time in France
    france_tz = pytz.timezone("Europe/Paris")
    now = datetime.now(france_tz)

    # Calculate the starting time based on the selected timeframe
    if timeframe == TimeFrame.today_midnight:
        today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = today_midnight
    else:  # timeframe == TimeFrame.last_sunday_midnight
        last_sunday = now - timedelta(days=now.weekday() + 1)  # Go back to last Sunday
        start_time = last_sunday.replace(hour=0, minute=0, second=0, microsecond=0)

    # Count posts with the given hashtag since the selected start time
    count = sum(
        1 for post in user_data["posts"]
        if hashtag in post["hashtags"] and datetime.fromisoformat(post["timestamp"]) >= start_time
    )

    if count > 0:
        return {"result": "yes", "number": count}
    
    return {"result": "no"}


@app.get("/daily-activity")
async def daily_activity(
    username: str,
    hashtag: str
):
    """
    Tracks the daily activity of a user's posts, reels, and stories mentioning the brand over the last 24 hours.

    Parameters:
    -----------
    username : str
        The username of the account to check.
    hashtag : str
        The hashtag to search for in the user's posts, reels, and stories.
    
    Raises:
    -------
    HTTPException
        If the account does not exist (404).
        If the account is private (403).
    
    Returns:
    -------
    result : dict
        A dictionary containing the daily activity statistics.
    
    Test Cases:
    -----------
    - **Scenario 1**: User has posted a story and a post/reel with the specific hashtag since last midnight.
        - **Input**: `username=user1`, `hashtag=#vacation`
        - **Output**: `{"followers": 150, "stories_with_hashtag": 2, "posts_with_hashtag": 1, "total_likes": 18}`

    - **Scenario 2**: User has only posted a story with the specific hashtag in the last 24 hours.
        - **Input**: `username=user2`, `hashtag=#vacation`
        - **Output**: `{"followers": 200, "stories_with_hashtag": 0, "total_likes": 0}`

    - **Scenario 3**: User has only posted a reel/post with the specific hashtag in the last 24 hours.
        - **Input**: `username=user1`, `hashtag=#travel`
        - **Output**: `{"followers": 150, "stories_with_hashtag": 0, "total_likes": 10}`

    - **Scenario 4**: User hasn’t posted anything in the last 24 hours, but has previous posts/reels recorded.
        - **Input**: `username=user2`, `hashtag=#vacation`
        - **Output**: `{"followers": 200, "total_likes": 20}`

    - **Scenario 5**: User hasn’t posted anything since last midnight and has no previous posts/reels recorded.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: `{"followers": 50, "total_likes": 0}`

    - **Scenario 6**: User has a private account.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Scenario 7**: User’s account doesn’t exist.
        - **Input**: `username=user4`, `hashtag=#vacation`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """

    if username not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist")

    user_data = mock_users[username]

    if user_data["private"]:
        raise HTTPException(status_code=403, detail="Account is private")

    # Get the current time in France
    france_tz = pytz.timezone("Europe/Paris")
    now = datetime.now(france_tz)

    # Calculate today's midnight
    today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Initialize activity stats
    stories_with_hashtag = 0
    posts_with_hashtag = 0
    total_likes = 0

    # Filter stories with the specific hashtag since today midnight
    for story in user_data["stories"]:
        if hashtag in story["hashtags"] and datetime.fromisoformat(story["timestamp"]) >= today_midnight:
            stories_with_hashtag += 1

    # Filter posts/reels with the specific hashtag since today midnight
    for post in user_data["posts"]:
        if hashtag in post["hashtags"] and datetime.fromisoformat(post["timestamp"]) >= today_midnight:
            posts_with_hashtag += 1
            total_likes += post["likes"]

    # Check the total likes for the last 10 posts/reels since today midnight
    recent_posts = user_data["posts"][-10:]  # Get the last 10 posts
    for post in recent_posts:
        if datetime.fromisoformat(post["timestamp"]) >= today_midnight:
            total_likes += post["likes"]

    # Prepare the response
    response = {
        "followers": user_data["followers"],
        "stories_with_hashtag": stories_with_hashtag,
        "posts_with_hashtag": posts_with_hashtag,
        "total_likes": total_likes
    }

    # Return the response
    return response


@app.get("/latest-post")
async def latest_post(account: str = "andrealbriziom"):
    """
    Fetches the link to the latest post of a specified Instagram account.

    Parameters:
    -----------
    account : str
        The Instagram account whose last post will be fetched (default: "andrealbriziom").
    
    Returns:
    -------
    result : dict
        A dictionary containing the link to the latest post.

    Raises:
    -------
    HTTPException
        If the specified account does not exist (404).
    """
    
    # Check if the account exists
    if account not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist")
    
    # Get the latest post link
    latest_post_data = mock_users[account]["posts"][0]  # Latest post is the first one in the list
    latest_post_link = latest_post_data["link"]
    return {"latest_post": latest_post_link}

@app.get("/check-comment")
async def check_comment(
    username: str,
    account: str
):
    """
    Checks if a specified user commented on the last post of a specified Instagram account.

    Parameters:
    -----------
    username : str
        The username of the user to check for comments.
    account : str
        The Instagram account whose last post will be checked.
    
    Raises:
    -------
    HTTPException
        If the specified account does not exist (404).
    
    Returns:
    -------
    result : dict
        A dictionary containing whether the user commented on the last post.
    """
    
    # Check if the specified account exists
    if account not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist")

    # Retrieve the last post from the specified account
    last_post = mock_users[account]["posts"][0]
    
    # Check if the user commented on the last post
    if any(comment for comment in last_post["comments"] if f"User {username} commented on this!" in comment):
        return {"commented": "yes"}
    
    return {"commented": "no"}


@app.get("/check-follow")
async def check_follow(user: str):
    """
    Check if the specified user follows @andrealbriziom.
    
    Parameters:
    -----------
    user : str
        The username of the account to check if it follows @andrealbriziom.
    
    Raises:
    -------
    HTTPException
        If the account does not exist (error2).
        If the account is private (error).
    
    Returns:
    -------
    result : dict
        A dictionary indicating whether the user follows @andrealbriziom.
    """
    # The account to check against
    target_account = "andrealbriziom"
    
    # Check if the user exists in the mock database
    user_data = get_user_data(user)
    
    # Check if the target account is private
    target_account_data = get_user_data(target_account)
    
    if target_account_data["private"]:
        raise HTTPException(status_code=403, detail="It seems like you have a private account. Your account needs to be public to complete the missions.")
    
    # Logic to check if user follows the target account
    if user in mock_users:
        following = target_account in mock_users[user].get("following", [])
        return {"result": "yes" if following else "no"}
    else:
        raise HTTPException(status_code=404, detail="It seems like the Instagram handle you provided doesn’t exist. Please correct it and try again.")
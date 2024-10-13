from enum import Enum
from fastapi import FastAPI, HTTPException, Request
import httpx
from mock_social_api.schemas.response_schema import IGetResponseBase, IResponseActivity, IResponseBolean, IResponseCounter, IResponseLatestPost
from mock_social_api.constants import mock_users

app = FastAPI()


# Enum for time frame selection
class TimeFrame(str, Enum):
    today_midnight = "today_midnight"
    last_sunday_midnight = "last_sunday_midnight"


@app.get("/")
def read_root() -> str:
    """
    Root endpoint to verify that the API is up.
    
    Returns:
    --------
    status : str
        A string indicating the API status.
    """
    return "Active"


@app.get("/check-story")
async def check_story(
    username: str,
    hashtag: str,
) -> IResponseBolean:
    """
    Checks if a user has a story containing the specified hashtag.

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
    --------
    IResponseBolean:
        - `result` (bool): Whether a story with the hashtag exists.
        - `username` (str | None): The username for reference.

    Test Cases:
    -----------
    - **Case 1**: User has stories and the hashtag exists.
        - **Input**: `username=user1`, `hashtag=#vacation`
        - **Output**: `{"result": true, "username": "user1"}`

    - **Case 2**: User has stories but the hashtag does not exist.
        - **Input**: `username=user1`, `hashtag=#travel`
        - **Output**: `{"result": false, "username": "user1"}`

    - **Case 3**: User has no stories.
        - **Input**: `username=user2`, `hashtag=#vacation`
        - **Output**: `{"result": false, "username": "user2"}`

    - **Case 4**: User's account is private.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Case 5**: Non-existing user.
        - **Input**: `username=user4`, `hashtag=#vacation`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """

    # Mock response for test cases
    if username == "user1" and hashtag == "#vacation":
        return IResponseBolean(result=True, username="user1")
    elif username == "user1" and hashtag == "#travel":
        return IResponseBolean(result=False, username="user1")
    elif username == "user2":  # Assume user2 has no stories
        return IResponseBolean(result=False, username="user2")
    elif username == "user3":  # user3's account is private
        raise HTTPException(status_code=403, detail="Account is private")
    elif username == "user4":  # user4 does not exist
        raise HTTPException(status_code=404, detail="Account does not exist")
    else:
        return IResponseBolean(result=False, username=username)




@app.get("/count-stories")
async def count_stories(
    username: str,
    hashtag: str,
) -> IResponseCounter:
    """
    Counts how many stories a user has posted with a given hashtag since midnight (French time).
    
    Parameters:
    -----------
    username : str
        The username of the account to check.
    hashtag : str
        The hashtag to search for in the user's stories since midnight (France timezone).
    
    Raises:
    -------
    HTTPException
        If the account does not exist (404).
        If the account is private (403).
    
    Returns:
    --------
    IResponseCounter:
        - `result` (int): Number of stories with the given hashtag since midnight (France time).
        - `username` (str | None): The username for reference.

    Test Cases:
    -----------
    - **Case 1**: User with stories that match the hashtag.
        - **Input**: `username=user1`, `hashtag=#vacation`
        - **Output**: `{"result": 2, "username": "user1"}`

    - **Case 2**: User with stories but no matching hashtag.
        - **Input**: `username=user2`, `hashtag=#vacation`
        - **Output**: `{"result": 0, "username": "user2"}`

    - **Case 3**: User has no stories.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: `{"result": 0, "username": "user3"}`

    - **Case 4**: User's account is private.
        - **Input**: `username=user4`, `hashtag=#vacation`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Case 5**: Non-existing user.
        - **Input**: `username=user5`, `hashtag=#vacation`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """
    
    # Mock response for test cases
    if username == "user1" and hashtag == "#vacation":
        return IResponseCounter(result=2, username="user1")
    elif username == "user2" and hashtag == "#vacation":
        return IResponseCounter(result=0, username="user2")
    elif username == "user3":  # user3 has no stories
        return IResponseCounter(result=0, username="user3")
    elif username == "user4":  # user4's account is private
        raise HTTPException(status_code=403, detail="Account is private")
    elif username == "user5":  # user5 does not exist
        raise HTTPException(status_code=404, detail="Account does not exist")
    else:
        return IResponseCounter(result=0, username=username)


@app.get("/count-posts")
async def count_posts(
    username: str,
    hashtag: str,
    timeframe: TimeFrame = TimeFrame.last_sunday_midnight
) -> IResponseCounter:
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
        The time frame from which to count posts, defaulting to `last_sunday_midnight`.
    
    Raises:
    -------
    HTTPException
        If the account does not exist (404).
        If the account is private (403).
    
    Returns:
    --------
    IResponseCounter:
        A response model containing:
        - `result` (int): The number of posts with the given hashtag since the selected time frame.
        - `username` (str | None): The username for reference.
    
    Test Cases:
    -----------
    - **Case 1**: User has posts with the hashtag.
        - **Input**: `username=user1`, `hashtag=#vacation`, `timeframe=last_sunday_midnight`
        - **Output**: `{"result": 2, "username": "user1"}`

    - **Case 2**: User has posts but no matching hashtag.
        - **Input**: `username=user2`, `hashtag=#vacation`, `timeframe=today_midnight`
        - **Output**: `{"result": 0, "username": "user2"}`

    - **Case 3**: User has no posts.
        - **Input**: `username=user3`, `hashtag=#vacation`, `timeframe=today_midnight`
        - **Output**: `{"result": 0, "username": "user3"}`

    - **Case 4**: User's account is private.
        - **Input**: `username=user4`, `hashtag=#vacation`, `timeframe=last_sunday_midnight`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Case 5**: Non-existing account.
        - **Input**: `username=user5`, `hashtag=#vacation`, `timeframe=today_midnight`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """

    # Hardcoded responses for specific scenarios
    if username == "user5":
        # Case 5: Non-existing account
        raise HTTPException(status_code=404, detail="Account does not exist")

    if username == "user4":
        # Case 4: User's account is private
        raise HTTPException(status_code=403, detail="Account is private")

    if username == "user1" and hashtag == "#vacation" and timeframe == TimeFrame.last_sunday_midnight:
        # Case 1: User has posts with the hashtag since last Sunday
        return IResponseCounter(result=2, username=username)

    if username == "user2" and hashtag == "#vacation" and timeframe == TimeFrame.today_midnight:
        # Case 2: User has posts but no matching hashtag
        return IResponseCounter(result=0, username=username)

    if username == "user3" and hashtag == "#vacation":
        # Case 3: User has no posts
        return IResponseCounter(result=0, username=username)

    # Default response for other cases
    return IResponseCounter(result=0, username=username)

    

@app.get("/daily-activity", response_model=IResponseActivity)
async def daily_activity(
    username: str,
    hashtag: str
) -> IResponseActivity:
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
    result : IResponseActivity
        An object containing the daily activity statistics.
    
    Test Cases:
    -----------
    - **Scenario 1**: User has posted a story and a post/reel with the specific hashtag since last midnight.
        - **Input**: `username=user1`, `hashtag=#vacation`
        - **Output**: `{"followers": 150, "stories_with_hashtag": 2, "posts_with_hashtag": 1, "total_likes": 18, "username": "user1"}`

    - **Scenario 2**: User has only posted a story with the specific hashtag in the last 24 hours.
        - **Input**: `username=user6`, `hashtag=#vacation`
        - **Output**: `{"followers": 200, "stories_with_hashtag": 1, "posts_with_hashtag": 0, "total_likes": 0, "username": "user6"}`

    - **Scenario 3**: User has only posted a reel/post with the specific hashtag in the last 24 hours.
        - **Input**: `username=user1`, `hashtag=#travel`
        - **Output**: `{"followers": 150, "stories_with_hashtag": 0, "posts_with_hashtag": 1, "total_likes": 10, "username": "user1"}`

    - **Scenario 4**: User hasn’t posted anything in the last 24 hours, but has previous posts/reels recorded.
        - **Input**: `username=user2`, `hashtag=#vacation`
        - **Output**: `{"followers": 200, "stories_with_hashtag": 0, "posts_with_hashtag": 0, "total_likes": 20, "username": "user2"}`

    - **Scenario 5**: User hasn’t posted anything since last midnight and has no previous posts/reels recorded.
        - **Input**: `username=user3`, `hashtag=#vacation`
        - **Output**: `{"followers": 50, "stories_with_hashtag": 0, "posts_with_hashtag": 0, "total_likes": 0, "username": "user3"}`

    - **Scenario 6**: User has a private account.
        - **Input**: `username=user4`, `hashtag=#vacation`
        - **Output**: HTTP 403: `{"detail": "Account is private"}`

    - **Scenario 7**: User’s account doesn’t exist.
        - **Input**: `username=user5`, `hashtag=#vacation`
        - **Output**: HTTP 404: `{"detail": "Account does not exist"}`
    """

    # Hardcoded responses based on scenarios
    if username == "user1" and hashtag == "#vacation":
        # Scenario 1: User with stories and post/reel
        return IResponseActivity(
            followers=150,
            stories_with_hashtag=2,
            posts_with_hashtag=1,
            total_likes=18,
            username=username
        )

    elif username == "user6" and hashtag == "#vacation":
        # Scenario 2: User with only a story
        return IResponseActivity(
            followers=200,
            stories_with_hashtag=1,
            posts_with_hashtag=0,
            total_likes=0,
            username=username
        )

    elif username == "user1" and hashtag == "#travel":
        # Scenario 3: User with only a post/reel
        return IResponseActivity(
            followers=150,
            stories_with_hashtag=0,
            posts_with_hashtag=1,
            total_likes=10,
            username=username
        )

    elif username == "user2" and hashtag == "#vacation":
        # Scenario 4: User hasn’t posted in the last 24 hours but has previous posts
        return IResponseActivity(
            followers=200,
            stories_with_hashtag=0,
            posts_with_hashtag=0,
            total_likes=20,
            username=username
        )

    elif username == "user3" and hashtag == "#vacation":
        # Scenario 5: User hasn’t posted and has no previous posts
        return IResponseActivity(
            followers=50,
            stories_with_hashtag=0,
            posts_with_hashtag=0,
            total_likes=0,
            username=username
        )

    elif username == "user4":
        # Scenario 6: User has a private account
        raise HTTPException(status_code=403, detail="Account is private")

    else:
        # Scenario 7: User doesn’t exist
        raise HTTPException(status_code=404, detail="Account does not exist")

    

@app.get("/latest-post")
async def latest_post() -> IResponseLatestPost:
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
    target_account = "andrealbriziom"

    # Check if the account exists
    if target_account not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist")
    
    # Get the latest post link
    latest_post_data = mock_users[target_account].posts[0]
    latest_post_link = latest_post_data.link
    return IResponseLatestPost(link=latest_post_link)


@app.get("/check-comment")
async def check_comment(username: str) -> IResponseBolean:
    """
    Checks if a specified user commented on the last post of the Instagram account @andrealbriziom.

    Parameters:
    -----------
    username : str
        The username of the user to check for comments.

    Raises:
    -------
    HTTPException
        If the specified account does not exist (404).
        If the user's account is private (403).

    Returns:
    -------
    IResponseBolean:
        - `result` (bool): Indicates whether the user commented on the last post.
        - `username` (str | None): The username for reference.

    Test Cases:
    -----------
    - **Case 1**: User commented on the last post.
        - **Input**: `username=user1`
        - **Output**: `{"result": true, "username": "user1"}`

    - **Case 2**: User did not comment on the last post.
        - **Input**: `username=user2`
        - **Output**: `{"result": false, "username": "user2"}`

    - **Case 3**: Account being checked does not exist.
        - **Input**: `username=user3`
        - **Output**: HTTP 404: `{"detail": "Account does not exist."}`

    - **Case 4**: User's account is private.
        - **Input**: `username=user4`
        - **Output**: HTTP 403: `{"detail": "Your account is private. You need to make your account public to check comments."}`
    """
    
    target_account = "andrealbriziom"
    
    # Mock user data and posts for demonstration (replace with real data retrieval)
    mock_users = {
        "andrealbriziom": {
            "private": False,
            "posts": [
                {
                    "comments": [
                        {"username": "user1", "text": "Great post!"},
                        {"username": "user5", "text": "Love this!"}
                    ]
                }
            ]
        },
        "user1": {"private": False},  # User who commented
        "user2": {"private": False},  # User who did not comment
        "user3": None,  # Non-existing account
        "user4": {"private": True}  # Private account
    }

    # Check if the specified account exists
    if target_account not in mock_users:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    # Fetch the user data for the user making the request
    user_data = mock_users.get(username, None)
    
    # Check if the user's account exists
    if user_data is None:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    # Check if the user's account is private
    if user_data.get("private", False):
        raise HTTPException(status_code=403, detail="Your account is private. You need to make your account public to check comments.")
    
    # Retrieve the last post from the specified account
    last_post = mock_users[target_account]["posts"][0]  # Fetching the most recent post
    
    # Check if the user commented on the last post
    commented = any(comment["username"] == username for comment in last_post["comments"])
    
    return IResponseBolean(result=commented, username=username)


@app.get("/check-follow")
async def check_follow(username: str) -> IResponseBolean:
    """
    Checks if the specified user follows the Instagram account @andrealbriziom.

    Parameters:
    -----------
    username : str
        The username of the account to check.

    Raises:
    -------
    HTTPException
        If the account being checked is private (403).
        If the account does not exist (404).

    Returns:
    --------
    IResponseBolean:
        - `result` (bool): Whether the specified user follows @andrealbriziom.
        - `username` (str | None): The username for reference.

    Test Cases:
    -----------
    - **Case 1**: User follows @andrealbriziom.
        - **Input**: `username=user1`
        - **Output**: `{"result": true, "username": "user1"}`

    - **Case 2**: User does not follow @andrealbriziom.
        - **Input**: `username=user2`
        - **Output**: `{"result": false, "username": "user2"}`

    - **Case 3**: Account being checked is private.
        - **Input**: `username=user3`
        - **Output**: HTTP 403: `{"detail": "The account you are checking is private."}`

    - **Case 4**: Non-existing account.
        - **Input**: `username=user4`
        - **Output**: HTTP 404: `{"detail": "The account does not exist."}`
    """
    
    target_account = "andrealbriziom"
    
    # Mock user data for demonstration (should be replaced with real data retrieval logic)
    mock_users = {
        "user1": {"private": False, "follows": True},  # Follows @andrealbriziom
        "user2": {"private": False, "follows": False},  # Does not follow @andrealbriziom
        "user3": {"private": True, "follows": False},  # Account is private
        "user4": None,  # Non-existing account
    }

    # Fetch the user data for the user making the request
    user_data = mock_users.get(username, None)
    
    # Check if the user's account exists
    if user_data is None:
        raise HTTPException(status_code=404, detail="The account does not exist.")

    # Check if the user's account is private
    if user_data["private"]:
        raise HTTPException(status_code=403, detail="Your account is private. You need to make your account public to check follow status.")

    # Logic to check if the user follows @andrealbriziom
    is_following = user_data["follows"]  # Now accurately reflects whether the user follows the target account
    
    return IResponseBolean(result=is_following, username=username)


TARGET_BASE_URL = "http://arntreal.upstar.club:2001"

@app.api_route("/upstar/{path:path}", methods=["GET"])
async def proxy(request: Request, path: str):
    """
    This endpoint acts as a proxy, redirecting all incoming requests to the target base URL.
    """
    target_url = f"{TARGET_BASE_URL}/{path}?{request.query_params}"
    
    # Prepare the data for proxying the request
    headers = dict(request.headers)
    body = await request.body()
    
    try:
        async with httpx.AsyncClient() as client:
            # Use request's method dynamically to forward the request
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body
            )
        
        # Forward the response back to the client
        return response.json()

    except httpx.RequestError as e:
        return {"error": "Proxy request failed", "detail": str(e)}

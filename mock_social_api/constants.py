from datetime import datetime
from mock_social_api.schemas.instagram_schema import IPost, IStory, IUser, IComment

# Mock database of users
mock_users: dict[str, IUser] = {
    "andrealbriziom": IUser(
        stories=[],
        posts=[
            IPost(
                content="Just chilling at the beach #vacation",
                hashtags=["#vacation"],
                timestamp=datetime.fromisoformat("2024-10-02T10:00:00"),
                likes=10,
                link="https://instagram.com/p/123456789",
                comments=[
                    IComment(username="user1", content="Looks amazing!", timestamp=datetime.fromisoformat("2024-10-02T12:00:00"))                ]
            ),
            IPost(
                content="Exploring the mountains",
                timestamp=datetime.fromisoformat("2024-10-03T10:00:00"),
                likes=12,
                link="https://instagram.com/p/987654321",
                comments=[
                    IComment(username="user1", content="Great view!", timestamp=datetime.fromisoformat("2024-10-03T11:00:00"))
                ]
            ),
            IPost(
                content="Weekend fun #vacation",
                hashtags=["#vacation"],
                timestamp=datetime.fromisoformat("2024-10-04T08:00:00"),
                likes=7,
                link="https://instagram.com/p/112233445",
                comments=[]
            )
        ],
        private=False,
        followers=150,
    ),
    "user1": IUser(
        stories=[
            IStory(content="Check out this #vacation!", hashtags=["#vacation"], timestamp=datetime.fromisoformat("2024-10-03T21:30:00"), likes=5),
            IStory(content="Another day, another adventure #vacation", hashtags=["#vacation"], timestamp=datetime.fromisoformat("2024-10-04T08:00:00"), likes=3),
        ],
        posts=[
            IPost(content="Just chilling at the beach #vacation", hashtags=["#vacation"], timestamp=datetime.fromisoformat("2024-10-02T10:00:00"), likes=10),
            IPost(content="Exploring the mountains", timestamp=datetime.fromisoformat("2024-10-03T10:00:00"), likes=12),
            IPost(content="Weekend fun #vacation", hashtags=["#vacation"], timestamp=datetime.fromisoformat("2024-10-06T09:00:00"), likes=7),
        ],
        private=False,
        followers=150,
    ),
    "user2": IUser(
        stories=[
            IStory(content="Just chilling", timestamp=datetime.fromisoformat("2024-10-04T10:00:00"), likes=1),
        ],
        posts=[
            IPost(content="A day well spent #travel", hashtags=["#travel"], timestamp=datetime.fromisoformat("2024-10-01T12:00:00"), likes=20),
        ],
        private=False,
        followers=0,
    ),
    "user3": IUser(
        stories=[],
        posts=[],
        private=True,  # private account
        followers=50,
    ),
}

# Written by: Christopher Gholmieh
# Imports:

# Random:
import random

# Praw:
import praw


# Scraper:
class Scraper:
    # Initialization:
    def __init__(self, configuration) -> None:
        # Client:
        self.client_identifier: str = configuration["authentication"]["client_identifier"]
        self.client_secret: str = configuration["authentication"]["client_secret"]

        # Agent:
        self.user_agent: str = f"ai-video-bot (by u/){configuration['authentication']['reddit_username']}"

        # Reddit:
        self.subreddits = configuration["scraper"]["subreddits"]

        self.reddit = praw.Reddit(
            client_id=self.client_identifier,
            client_secret=self.client_secret,

            user_agent=self.user_agent
        )

    # Methods:
    def collect_posts(self, subreddit_name: str, limit: int = 5) -> list:
        # Variables (Assignment):
        # Subreddit:
        subreddit = self.reddit.subreddit(random.choice(subreddit_name))

        # Posts:
        posts: list = []

        # Logic:
        for post in subreddit.hot(limit=limit):
            if post.stickied:
                continue

            posts.append({
                # Title:
                "title": post.title,

                # Text:
                "text": post.selftext,

                # Score:
                "score": post.score,

                # Comments:
                "comments": [comment.body for comment in post.comments[:3] if hasattr(comment, "body")]
            })

        return posts
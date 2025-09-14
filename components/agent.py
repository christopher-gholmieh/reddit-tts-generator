# Written by: Christopher Gholmieh
# Imports:

# OpenAI:
from openai import OpenAI


# Agent:
class Agent:
    # Initialization:
    def __init__(self, configuration):
        # Client:
        self.client = OpenAI(api_key=configuration["agent"]["openai_api_key"])

    # Methods:
    def generate_story(self, title: str, body: str, comments: list[str]) -> str:
        # Variables (Assignment):
        # Instructions:
        instructions = """
        You are a viral short-form story writer. 
        Your job is to take inspiration from Reddit posts (like AITA, OffMyChest, Confessions) 
        and turn them into vivid, emotional, and slightly dramatized short stories.

        Write in first-person, present-tense.
        Make it spicy, suspenseful, and emotionally charged.
        Add details to make the story flow with a strong hook, rising tension, and a twist or resolution.
        Make it feel real, but better than reality — like a polished diary entry or confession video.

        Keep the story under 300 words. Do NOT reference Reddit or posts or usernames.
        """

        # Prompt:
        formatted_comments: str= "\n".join(f" - {comment}" for comment in comments)
        input_text: str = f"""
            Title: {title}
            Post: {body}

            Top Comments:
            {formatted_comments}
        """

        # Story:
        story = self.client.responses.create(
            # Model:
            model="gpt-4o",

            # Instructions:
            instructions=instructions.strip(),

            # Input:
            input=input_text.strip()
        )

        # Logic:
        return story.output_text
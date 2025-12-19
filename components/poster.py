# Written by: Christopher Gholmieh
# Imports:

# Instagram:
from instagrapi import Client

# OS:
import os


# Constants:
SESSION_FILE = "instagram_session.json"


# Poster:
class Poster:
    # Initialization:
    def __init__(self, configuration) -> None:
        # Variables (Assignment):
        # Instagram:
        self.instagram = Client()

        # Validation:
        if os.path.exists(SESSION_FILE):
            try:
                # Logic:
                self.instagram.load_settings(SESSION_FILE)
                self.instagram.login(
                    configuration["authentication"]["instagram_username"],
                    configuration["authentication"]["instagram_password"]
                )

                # Message:
                print("[*] Logged in using saved session!")

                # Logic:
                return
            except Exception as exception:
                print(f"[!] Failed to load session: {exception}")

        try:
            # Logic:
            self.instagram.login(
                configuration["authentication"]["instagram_username"],
                configuration["authentication"]["instagram_password"]
            )

            self.instagram.dump_settings(SESSION_FILE)

            # Message:
            print("[*] New login successful, session saved.")
        except Exception as exception:
            print(f"[!] Failed to login to Instagram: {exception}")

    # Methods:
    def upload_reel(self, video_path: str, thumbnail_path: str, caption: str, tags: list[str]) -> None:
        # Variables (Assignment):
        # Tags:
        formatted_tags: str = " ".join(tags)

        # Caption:
        full_caption: str = f"{caption}\n\n{formatted_tags}"

        # Logic:
        try:
            # Validation:
            if not os.path.exists(thumbnail_path):
                raise FileNotFoundError(f"Thumbnail file not found: {thumbnail_path}")

            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")

            # Variables (Assignment):
            # Media:
            media = self.instagram.clip_upload(
                # Path:
                path=video_path,

                # Caption:
                caption=full_caption,

                # Thumbnail:
                thumbnail=thumbnail_path
            )

            # Logic:
            return media

        except Exception as exception:
            # Message:
            print(f"[!] Failed to upload reel: {exception}")

            # Logic:
            raise

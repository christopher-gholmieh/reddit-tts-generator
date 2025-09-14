# Written by: Christopher Gholmieh
# Imports:

# Instagram:
from instagrapi import Client
from instagrapi.types import Media

# OS:
import os

# FFMPEG:
import ffmpeg

# Poster:
SESSION_FILE = "instagram_session.json"

class Poster:
    def __init__(self, configuration) -> None:
        self.instagram = Client()

        # Try loading session
        if os.path.exists(SESSION_FILE):
            try:
                self.instagram.load_settings(SESSION_FILE)
                self.instagram.login(
                    configuration["authentication"]["instagram_username"],
                    configuration["authentication"]["instagram_password"]
                )
                print("[*] Logged in using saved session.")
                return
            except Exception as e:
                print(f"[!] Failed to load session: {e}")
                print("[*] Attempting fresh login...")

        # Fresh login (first time)
        try:
            self.instagram.login(
                configuration["authentication"]["instagram_username"],
                configuration["authentication"]["instagram_password"]
            )
            self.instagram.dump_settings(SESSION_FILE)
            print("[*] New login successful, session saved.")
        except Exception as e:
            print(f"[!] Failed to login to Instagram: {str(e)}")



    # Methods:
    def upload_reel(self, video_path: str, thumbnail_path: str, caption: str, tags: list[str]) -> None:
        # Variables (Assignment):
        # Tags:
        formatted_tags: str = " ".join(tags)

        # Caption:
        full_caption: str = f"{caption}\n\n{formatted_tags}"

        # Logic:
        try:
            # Verify files exist
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            if not os.path.exists(thumbnail_path):
                raise FileNotFoundError(f"Thumbnail file not found: {thumbnail_path}")

            # Upload the reel
            media = self.instagram.clip_upload(
                # Path:
                path=video_path,

                # Caption:
                caption=full_caption,

                # Thumbnail:
                thumbnail=thumbnail_path
            )

            return media

        except Exception as e:
            print(f"[!] Failed to upload reel: {str(e)}")
            raise
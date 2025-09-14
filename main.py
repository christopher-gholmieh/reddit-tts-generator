# Written by: Christopher Gholmieh
# Imports:

# Components:
from components.renderer import Renderer
from components.scraper import Scraper
from components.poster import Poster
from components.voice import Voice
from components.agent import Agent

# Random:
import random

# FFMPEG:
import ffmpeg

# TOML:
import toml


# Configuration:
with open("configuration.toml" , "r") as configuration_file:
    configuration = toml.load(configuration_file)


# Main:
renderer: Renderer = Renderer()
scraper: Scraper = Scraper(configuration)
poster: Poster = Poster(configuration)
voice: Voice = Voice(configuration)
agent: Agent = Agent(configuration)

# Variables (Assignment):
# Posts:
posts = scraper.collect_posts(configuration["scraper"]["subreddits"], limit=5)
post = max(posts, key=lambda post: post["score"])

# Story:
story: str = post["text"][:10000]

# Voice:
voice.generate_voice(post["title"], "temporary/title_audio.mp3")
voice.generate_voice(story, "temporary/story_audio.mp3")

# Probe:
title_probe = ffmpeg.probe("temporary/title_audio.mp3")
story_probe = ffmpeg.probe("temporary/story_audio.mp3")

# Footage:
background_footage = renderer.get_random_footage()

# Probe:
background_probe = ffmpeg.probe(background_footage)

# Duration:
title_duration: float = float(title_probe["format"]["duration"])
story_duration: float = float(story_probe["format"]["duration"])

background_duration: float = float(background_probe["format"]["duration"])
total_duration: float = title_duration + story_duration

# Time:
max_start_time = max(0, background_duration - total_duration)
start_time = random.uniform(0, max_start_time)

# Logic:
renderer.generate_thumbnail(
    background_footage=background_footage, title=post["title"],
    username=configuration["authentication"]["display_username"],
    output_path=f"thumbnails/thumbnail.png",
    start_time=start_time
)

renderer.render_footage(
    title_audio_path="temporary/title_audio.mp3",
    story_audio_path="temporary/story_audio.mp3",
    output_path=f"videos/output.mp4",
    start_time=start_time,
    background_footage=background_footage,
    story_duration=story_duration,
    title_duration=title_duration
)

poster.upload_reel(
    # Video:
    video_path="videos/output.mp4",

    # Thumbnail:
    thumbnail_path="thumbnails/thumbnail.png",

    # Caption:
    caption="",
  
    # Tags:
    tags=["#fyp", "#reddit", "#redditstories", "#storytime", "#drama", "#foryoupage", "#reels"]
)

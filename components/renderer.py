# Written by: Christopher Gholmieh
# Imports:

# Utilities:
from .utilities import transcribe_audio, generate_animated_subtitles

# Random:
import random

# FFMPEG:
import ffmpeg

# OS:
import os

# PIL:
from PIL import Image, ImageDraw, ImageFont

# Text:
import textwrap


# Functions:
def crop_transparent_edges(image: Image.Image) -> Image.Image:
    # Variables (Assignment):
    # Box:
    bounding_box = image.getbbox()

    # Logic:
    return image.crop(bounding_box) if bounding_box else image


# Renderer:
class Renderer:
    # Initialization:
    def __init__(self, footage_directory: str = "assets/footage"):
        # Paths:
        self.template_with_text_path: str = "temporary/template_with_text.png"
        self.template_path: str = "assets/images/title_template.png"

        self.animated_subtitles_path: str = "temporary/subtitles.ass"
        self.temporary_frame_path: str = "temporary/temporary_frame.jpg"

        # Footage:
        self.footage_directory = footage_directory

        # Font:
        self.font_path = "fonts/Roboto-Bold.ttf"

    # Methods:
    def get_random_footage(self) -> None:
        # Variables (Assignment):
        # Videos:
        videos = [footage for footage in os.listdir(self.footage_directory) if footage.endswith(".mp4")]

        if not videos:
            raise FileNotFoundError("[!] No MP4 files found in footage directory.")

        # Logic:
        return os.path.join(self.footage_directory, random.choice(videos))

    def render_footage(self, title_audio_path: str, story_audio_path: str, output_path: str, background_footage: str, start_time: float, title_duration: float, story_duration: float) -> None:
        # Variables (Assignment):
        # Duration:
        total_duration: float = title_duration + story_duration

        # Segments:
        segments = transcribe_audio(story_audio_path)

        # Subtitles:
        with open(self.animated_subtitles_path, "w", encoding="utf-8") as subtitles_file:
            # Variables (Assignment):
            # Segments:
            adjusted_segments = []

            # Logic:
            for segment in segments:
                adjusted_segments.append({
                    "word": segment["word"],
                    "start": segment["start"] + title_duration,
                    "end": segment["end"] + title_duration
                })

            generate_animated_subtitles(adjusted_segments, subtitles_file)

        # Inputs:
        input_title_audio = ffmpeg.input(title_audio_path)
        input_story_audio = ffmpeg.input(story_audio_path)

        input_video = ffmpeg.input(background_footage, ss=start_time)
        input_title = ffmpeg.input(self.template_with_text_path, loop=1, t=title_duration)

        # Filters:
        background_video = input_video.video

        # Blur:
        blurred = background_video.filter("scale", 1080, 1920).filter("boxblur", 10)
        scaled = background_video.filter("scale", "-1", 1920).filter("crop", 1080, 1920)

        final_background = ffmpeg.overlay(blurred, scaled, x="(main_w-overlay_w)/2", y="(main_h-overlay_h)/2")

        # FPS:
        final_background = final_background.filter("fps", fps=30).trim(duration=total_duration).setpts("PTS-STARTPTS")

        # Title:
        title_video = (
            input_title.video
            .filter("fps", fps=30)
            .setpts("PTS-STARTPTS")
        )

        # Final:
        final_video = (
            final_background
            .overlay(
                title_video,
                x="(W-w)/2",
                y="(H-h)/2",
                enable=f"between(t,0,{title_duration})"
            )
        )

        # Logic:
        if os.path.exists(self.animated_subtitles_path):
            final_video = final_video.filter("ass", self.animated_subtitles_path)

        # Variables (Assignment):
        # Output:
        concatenated_audio = ffmpeg.concat(input_title_audio.audio, input_story_audio.audio, v=0, a=1)

        # Logic:
        ffmpeg.output(
            # Video:
            final_video,

            # Audio:
            concatenated_audio,

            # Output:
            output_path,

            # VCode:
            vcodec="libx264",

            # ACode:
            acodec="aac",

            # Format:
            format="mp4",

            # Preset:
            preset="ultrafast",

            # Shortest:
            shortest=None,
        ).overwrite_output().run()

        # Cleanup:
        if os.path.exists(self.animated_subtitles_path):
            os.remove(self.animated_subtitles_path)

        if os.path.exists(self.template_with_text_path):
            os.remove(self.template_with_text_path)

    def generate_thumbnail(self, background_footage: str, title: str, username: str, output_path: str, start_time: float) -> None:
        # Variables (Assignment):
        # Stream:
        stream = ffmpeg.input(background_footage, ss=start_time)
        stream = ffmpeg.output(stream, self.temporary_frame_path, vframes=1)

        # Logic:
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)

        # Variables (Assignment):
        # Background:
        background = Image.open(self.temporary_frame_path).resize((1080, 1920), Image.Resampling.LANCZOS)

        # Template:
        title_template = Image.open(self.template_path)
        title_template = crop_transparent_edges(title_template)

        # Width:
        template_width = int(1080 * 0.8)

        # Ratio:
        aspect_ratio = title_template.height / title_template.width

        # Height:
        template_height = int(template_width * aspect_ratio)

        # Template:
        title_template = title_template.resize((template_width, template_height), Image.Resampling.LANCZOS)

        # Fonts:
        title_area_max_height: int = int(template_height * 0.5)

        max_title_font_size: int = 40
        min_title_font_size: int = 35

        username_font = ImageFont.truetype(self.font_path, 32)
        wrap_width: int = 32

        # Logic:
        title_font_size = max_title_font_size

        while title_font_size >= min_title_font_size:
            # Variables (Assignment):
            # Font:
            title_font = ImageFont.truetype(self.font_path, title_font_size)

            # Title:
            wrapped_title = textwrap.fill(title, width=wrap_width)

            # Lines:
            lines = wrapped_title.split("\n")

            # Height:
            line_height = title_font.getbbox("Ay")[3]

            # Spacing:
            spacing = 6

            # Height:
            total_title_height = len(lines) * (line_height + spacing) - spacing

            # Logic:
            if total_title_height <= title_area_max_height:
                break

            title_font_size -= 2

        # New Template:
        new_template = Image.new("RGBA", (template_width, template_height), (0, 0, 0, 0))
        new_template.paste(title_template, (0, 0))

        # Draw:
        draw = ImageDraw.Draw(new_template)

        # Username:
        draw.text((120, 15), f"u/{username}", fill="black", font=username_font)

        # Title Y:
        title_y_position = 110
        draw.multiline_text((120, title_y_position), wrapped_title, fill="black", font=title_font, spacing=spacing)

        # Save Template:
        new_template.save(self.template_with_text_path, "PNG")

        # Paste:
        x_position = (1080 - new_template.width) // 2
        y_position = 150

        background.paste(new_template, (x_position, y_position), new_template)
        background.save(output_path, quality=95)

        if os.path.exists(self.temporary_frame_path):
            os.remove(self.temporary_frame_path)
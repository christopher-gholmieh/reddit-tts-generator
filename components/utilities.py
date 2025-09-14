# Written by: Christopher Gholmieh
# Imports:

# Whisper:
import whisper

# Regex:
import re as regex

# Model:
model = whisper.load_model("base")

# Functions:
def transcribe_audio(audio_path: str) -> list:
    # Variables (Assignment):
    # Result:
    result = model.transcribe(audio_path, word_timestamps=True)

    # Segments:
    segments = []

    # Logic:
    for segment in result["segments"]:
        for word_info in segment["words"]:
            segments.append({
                # Word:
                "word": word_info["word"],

                # Start:
                "start": word_info["start"],

                # End:
                "end": word_info["end"]
            })
    
    return segments

def format_time(_seconds: float) -> str:
    # Variables (Assignment):
    # Hours:
    hours = int(_seconds // 3600)

    # Minutes:
    minutes = int((_seconds % 3600) // 60)

    # Seconds:
    seconds = int(_seconds % 60)

    # Miliseconds:
    miliseconds = int((_seconds - int(_seconds)) * 100)

    return f"{hours:d}:{minutes:02d}:{seconds:02d}.{miliseconds:02d}"

def generate_animated_subtitles(segments: list, output_file):
    # Variables (Assignment):
    # Header:
    header = """
    [Script Info]
    ScriptType: v4.00+
    PlayResX: 1920
    PlayResY: 1080

    [V4+ Styles]
    Format: Name, Fontname, Fontsize, PrimaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
    Style: Default,Arial Black,100,&H00FFFFFF,&H00000000,-1,0,1,8,3,5,10,10,10,1

    [Events]
    Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    """

    # Body:
    body = ""

    # Logic:
    for segment in segments:
        # Variables (Assignment):
        # Filter:
        filtered_word = regex.sub(r"[^\w\s]", "", segment['word']).strip()

        # Logic:
        body += (
            f"Dialogue: 0,{format_time(segment['start'])},{format_time(segment['end'])},Default,,0,0,0,,"
            f"{{\\an5\\bord8\\shad3\\fs100\\1c&HFFFFFF&\\3c&H000000&\\t(0,200,\\fs115)\\t(200,400,\\fs100)}}{filtered_word}\n"
        )

    output_file.write(header + "\n" + body)
    output_file.flush()
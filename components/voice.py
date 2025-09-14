# Written by: Christopher Gholmieh
# Imports:

# Elevenlabs:
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Voice:
class Voice:
    # Initialization:
    def __init__(self, configuration):
        self.elevenlabs_api_key: str = configuration["elevenlabs"]["elevenlabs_api_key"]
        self.elevenlabs_voice: str = configuration["elevenlabs"]["elevenlabs_voice"]

        self.elevenlabs = ElevenLabs(api_key=self.elevenlabs_api_key)

    # Methods:
    def generate_voice(self, text: str, output_path: str):
        # Variables (Assignment):
        # Audio:
        audio = self.elevenlabs.text_to_speech.convert(
            # Text:
            text=text,

            # Voice:
            voice_id=self.elevenlabs_voice,

            # Model:
            model_id="eleven_multilingual_v2",

            # Output:
            output_format="mp3_44100_128",

            # Settings:
            voice_settings={
                # Stability:
                "stability": 0.2,

                # Speed:
                "speed": 1.2,

                # Similarity:
                "similarity_boost": 0.2,

                # Style:
                "style": 1.0,

                # Boost:
                "use_speaker_boost": True,
            }
        )

        # Logic:
        with open(output_path, "wb") as output_file:
            for chunk in audio:
                output_file.write(chunk)
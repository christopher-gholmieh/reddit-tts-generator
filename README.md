# TTS Video Generator

An automated system that creates engaging short-form videos from Reddit posts using AI-generated text-to-speech, video rendering, and social media posting capabilities.

## Overview

This project automatically:
1. **Scrapes** popular posts from Reddit subreddits (AITA, Confessions, etc.)
2. **Generates** AI-enhanced stories from the content
3. **Creates** text-to-speech audio using ElevenLabs
4. **Renders** professional videos with background footage, titles, and animated subtitles
5. **Posts** the final videos to Instagram as Reels

## Features

- **Reddit Integration**: Automatically scrapes trending posts from multiple subreddits
- **AI Story Enhancement**: Uses OpenAI GPT-4 to transform Reddit posts into engaging narratives
- **High-Quality TTS**: ElevenLabs text-to-speech with customizable voice settings
- **Professional Video Rendering**: 
  - Background footage with blur effects
  - Custom title overlays with dynamic text sizing
  - Animated subtitles with word-level timing
  - Vertical format optimized for social media
- **Social Media Automation**: Direct Instagram Reels upload with hashtags
- **Smart Content Selection**: Automatically picks the highest-scoring posts

## Project Structure

```
tts-video-generator/
├── components/
│   ├── agent.py          # OpenAI GPT-4 story generation
│   ├── poster.py         # Instagram upload functionality
│   ├── renderer.py       # Video rendering and thumbnail generation
│   ├── scraper.py        # Reddit post scraping
│   ├── utilities.py      # Audio transcription and subtitle generation
│   └── voice.py          # ElevenLabs TTS integration
├── assets/
│   ├── footage/          # Background video files
│   └── images/
│       └── title_template.png
├── fonts/                # Custom fonts for text rendering
├── temporary/            # Temporary files during processing
├── thumbnails/           # Generated thumbnail images
├── videos/               # Final rendered videos
├── configuration.toml    # API keys and settings
├── main.py              # Main execution script
└── requirements.txt     # Python dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tts-video-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

4. **Configure API keys**
   Edit `configuration.toml` with your API credentials:
   ```toml
   [authentication]
   client_identifier="your_reddit_client_id"
   client_secret="your_reddit_client_secret"
   reddit_username="your_reddit_username"
   reddit_password="your_reddit_password"
   instagram_username="your_instagram_username"
   instagram_password="your_instagram_password"

   [elevenlabs]
   elevenlabs_api_key="your_elevenlabs_api_key"
   elevenlabs_voice="your_voice_id"

   [agent]
   openai_api_key="your_openai_api_key"
   ```

## Setup Requirements

### API Keys Needed:
- **Reddit API**: Create a Reddit app at [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
- **ElevenLabs**: Get API key from [elevenlabs.io](https://elevenlabs.io)
- **OpenAI**: Get API key from [platform.openai.com](https://platform.openai.com)

### Assets Required:
- **Background Footage**: Add MP4 video files to `assets/footage/` directory
- **Title Template**: Place a PNG template image at `assets/images/title_template.png`
- **Fonts**: Ensure font files are in the `fonts/` directory

## 🎬 Usage

1. **Add background footage** to `assets/footage/` directory
2. **Configure your settings** in `configuration.toml`
3. **Run the generator**:
   ```bash
   python main.py
   ```

The system will:
- Scrape Reddit posts from configured subreddits
- Select the highest-scoring post
- Generate AI-enhanced story content
- Create TTS audio for title and story
- Render a professional video with subtitles
- Generate a thumbnail
- Upload to Instagram as a Reel

## Configuration Options

### Subreddits
Modify the `subreddits` list in `configuration.toml`:
```toml
[scraper]
subreddits=["AITA", "Confessions", "AmIOverreacting", "AmItheAsshole", "TrueOffMyChest"]
```

### Voice Settings
Adjust ElevenLabs voice parameters in `voice.py`:
- Stability: Voice consistency
- Speed: Speech rate
- Similarity Boost: Voice similarity to original
- Style: Voice expressiveness

### Video Settings
Customize video rendering in `renderer.py`:
- Resolution: 1080x1920 (vertical format)
- FPS: 30 frames per second
- Background blur intensity
- Font sizes and positioning

## Output

The system generates:
- **Video**: `videos/output.mp4` - Final rendered video
- **Thumbnail**: `thumbnails/thumbnail.png` - Instagram thumbnail
- **Audio**: Temporary MP3 files for title and story

## Security Notes

- **Never commit** your `configuration.toml` file with real API keys
- Use environment variables for production deployments
- Consider using Reddit app-only authentication for better security

## Troubleshooting

### Common Issues:
1. **FFmpeg not found**: Ensure FFmpeg is installed and in your PATH
2. **API rate limits**: Check your API quotas and implement delays if needed
3. **Instagram login issues**: Clear session files and re-authenticate
4. **No footage found**: Ensure MP4 files are in `assets/footage/` directory

### Dependencies:
- Python 3.8+
- FFmpeg
- All packages listed in `requirements.txt`

## License

This project is for educational and personal use. Please respect Reddit's API terms of service and Instagram's community guidelines.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

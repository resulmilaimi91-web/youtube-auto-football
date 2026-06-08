# YouTube Auto Football - 24/7 Automated Channel

An automated system that generates football/soccer videos and uploads them to YouTube every 6 hours — completely hands-free.

## How It Works

1. **Fetches data** from TheSportsDB and BBC Sport for latest matches and news
2. **Generates script** automatically in English with professional templates
3. **Creates video** with voiceover (TTS), captions, subtitles, and background
4. **Uploads to YouTube** automatically via API
5. **Repeats every 6 hours** 24/7 through GitHub Actions

## Features

- Fully automated — zero manual work
- Professional English voiceover (Microsoft Edge TTS / Google TTS)
- Custom thumbnails generated automatically
- Multiple video templates (news, goals, analysis)
- Runs 24/7 on GitHub Actions (free tier)
- Easy to customize and extend

## Setup

### 1. YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create **OAuth 2.0 Credentials** (Desktop app type)
5. Note down your Client ID, Client Secret, and generate a refresh token

### 2. GitHub Configuration

Fork this repository and add these **repository secrets** (Settings → Secrets → Actions):

| Secret | Description |
|--------|-------------|
| `YOUTUBE_API_KEY` | Your YouTube API key |
| `YOUTUBE_CLIENT_ID` | OAuth Client ID |
| `YOUTUBE_CLIENT_SECRET` | OAuth Client Secret |
| `YOUTUBE_REFRESH_TOKEN` | OAuth refresh token |
| `CHANNEL_NAME` | Your channel name (optional) |
| `UPLOAD_SCHEDULE_HOURS` | Upload frequency in hours (default: 6) |

### 3. Generate Refresh Token

Run locally:
```bash
pip install -r requirements.txt
python -c "from src.youtube_uploader import get_authenticated_service; get_authenticated_service()"
```

This will open a browser for Google authentication. The refresh token will be saved to `output/token.pickle`.

> **Important**: Extract and add the refresh token as a GitHub secret:
> ```bash
> python -c "import pickle; data = pickle.load(open('output/token.pickle','rb')); print(data.refresh_token)"
> ```

### 4. Enable GitHub Actions

Once secrets are configured, the workflow triggers automatically:
- On every push to `main`
- On schedule (every 6 hours by default)
- Manually via Actions → "Run workflow"

## Project Structure

```
youtube-auto-football/
├── .github/workflows/    # GitHub Actions automation
├── src/
│   ├── config.py         # Configuration & environment
│   ├── football_data.py  # Football data fetching
│   ├── script_generator.py # Script & template engine
│   ├── video_generator.py  # Video & thumbnail creation
│   ├── youtube_uploader.py # YouTube API uploader
│   └── main.py           # Main pipeline (orchestrator)
├── assets/               # Background videos, music
├── requirements.txt
└── README.md
```

## Customization

- **Video templates**: Edit `src/script_generator.py`
- **Upload frequency**: Change `cron` in `.github/workflows/auto-upload.yml`
- **Video style**: Edit `src/video_generator.py` (colors, fonts, layout)
- **Better scripts**: Add `OPENAI_API_KEY` to your secrets for AI-generated content

## Monetization Tips

- **Post consistently** — daily uploads grow your audience faster
- **Optimize thumbnails** — use bright colors, bold text, and action shots
- **Target keywords** — "football highlights", "soccer news", "premier league goals"
- **Enable monetization** after reaching 1000 subscribers / 4000 watch hours
- **Add affiliate links** — sports betting, merchandise, streaming services

## License

MIT

# Football Highlights Daily - TV Channel on YouTube

Professional automated TV channel covering FIFA World Cup 2026 and global football.

## What This Does

- Generates **TV-quality videos** (1920x1080 desktop format)
- Fetches **World Cup 2026 news** from BBC Sport, ESPN, Sky Sports, Goal.com
- Creates **professional intros/outros** like a TV broadcast
- Adds **watermarks, news tickers, animated overlays**
- Uploads to YouTube **every 6 hours** automatically
- Uses **natural voice** (Microsoft Edge TTS + Google TTS fallback)

## Features

- 7 video styles: Breaking, Sports, World Cup, Analysis, News, Premium, Classic
- Professional thumbnail with gradient, logo, and overlays
- Intro/outro sequence like a TV channel
- Animated news ticker at bottom
- Watermark/logo in corner
- Title with shadow effect for depth
- Fade transitions between scenes
- Downloaded football images from Unsplash

## Setup for Monetization

### Requirements for YouTube Partner Program:
- **1,000 subscribers**
- **4,000 watch hours** in the past 12 months
- Content that follows YouTube policies

### How to reach monetization fast:
1. **Post consistently** - 4 videos per day (every 6 hours)
2. **Optimize titles** - Use trending keywords (World Cup 2026, FIFA, football)
3. **Engaging thumbnails** - Our TV-style thumbnails stand out
4. **Longer videos** - 3-5 minutes for more watch time
5. **SEO descriptions** - Our descriptions include relevant hashtags
6. **Call to action** - Every video asks viewers to subscribe
7. **Cross-promote** - Share on social media, football forums

## Hashtag Strategy

Each video uses 12-15 hashtags optimized for discoverability:
- Primary: #worldcup2026 #fifa #football #soccer
- League: #premierleague #laliga #seriea #bundesliga
- Event: #championsleague #worldcuphighlights
- Trending: #footballnews #highlights #sports

## Video Styles

1. **Breaking** - Red banner, urgent news style
2. **Sports** - Gold accent, action-oriented
3. **World Cup** - Blue/gold FIFA colors
4. **Analysis** - Dark, tactical breakdown
5. **News** - TV news broadcast style
6. **Premium** - Gold borders, high-end feel
7. **Classic** - Clean, professional look

## Project Structure

```
youtube-auto-football/
├── .github/workflows/    # GitHub Actions (every 6 hours)
├── src/
│   ├── config.py         # Configuration
│   ├── football_data.py  # Fetches news from portals
│   ├── script_generator.py # 7 TV-style templates
│   ├── video_generator.py  # Professional video creation
│   ├── tv_assets.py      # Intro/outro/watermark/logo
│   ├── youtube_uploader.py # YouTube API upload
│   └── main.py           # Main pipeline
├── assets/               # Background music, videos
├── requirements.txt
└── README.md
```

## License

MIT

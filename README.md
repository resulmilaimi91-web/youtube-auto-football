# 🚀 Automated Content Engine (ACE)

Professional Workflow for Sustainable YouTube Growth

## Project Mission

The objective of this project is to build and scale high-performing YouTube channels through an automated, data-driven content pipeline. By leveraging AI-assisted creation and real-time trend analysis, the system generates high-engagement assets while ensuring strict adherence to platform policies for long-term monetization and financial stability.

## Core Pillars

- **Trend-Driven Scalability:** The system continuously monitors Google Trends to identify high-velocity niches (Kids Animation & Sports Highlights).
- **Productivity Architecture:** An automated pipeline that produces 1 long-form anchor video supported by 2 high-conversion Shorts per cycle, maximizing visibility across YouTube's recommendation engine.
- **Financial Sustainability:** Built to generate consistent ad revenue and platform earnings, providing a reliable digital income stream.

## Safety & Compliance Framework (Risk Mitigation)

To protect the channels from penalties and ensure monetization eligibility, the workflow enforces these protocols:

- **Originality Assurance:** All assets undergo "Transformative Editing." We apply unique overlays, pacing adjustments, and AI-driven enhancements to ensure YouTube identifies the content as high-value and original.
- **Anti-Detection Logic:** The system mimics organic posting patterns (using randomized time intervals between uploads) to avoid "bot-like" behavior, which is the primary cause of automated account bans.
- **Policy Integrity:** Strict avoidance of copyright-infringing material. Every clip and animation is processed through a filtration layer to comply with YouTube's "Reused Content" and "Community Guidelines" policies.
- **Metadata Optimization:** Automated generation of SEO-rich, human-style titles and descriptions to build authority and trust with the YouTube algorithm.

## Channels

| Channel | Style | Content | Frequency |
|---------|-------|---------|-----------|
| **Kids (Aura & Luna)** | Cortana animations + children | Original songs, educational facts, no music | Every 6 hours |
| **Sports (FIFA)** | News TV-style, text-only | Records, stats, viral news without player photos | Every 6 hours |

## Workflow Roadmap

1. **Ingestion:** Real-time data capture from trending topics.
2. **Production:** AI-based synthesis of visuals (Aura/Luna characters) and sports media processing.
3. **Deployment:** Scheduled publishing to ensure consistent channel activity and viewer retention.
4. **Optimization:** Ongoing analysis of performance data to refine future content cycles.

## Security Protocol

- API keys protected via **GitHub Secrets**
- Separate refresh tokens per channel (`YOUTUBE_REFRESH_TOKEN` for Kids, `FIFA_REFRESH_TOKEN` for FIFA)
- Never expose credentials in code

## Project Structure

```
youtube-auto-football/
├── .github/workflows/       # GitHub Actions auto-upload
├── src/
│   ├── main.py              # Main pipeline
│   ├── config.py            # Environment config
│   ├── kids_song_generator.py    # 7 original kids songs
│   ├── kids_animation_generator.py # Cortana + kids animations
│   ├── viral_shorts.py      # Kids shorts with Cortana
│   ├── fifa_script_generator.py  # Football news templates
│   ├── video_generator.py   # Text-only news-style video
│   ├── fifa_shorts.py       # FIFA text-only shorts
│   ├── trends_fetcher.py    # Google Trends integration
│   ├── youtube_uploader.py  # YouTube API OAuth upload
│   └── get_fifa_token.py    # Helper for FIFA refresh token
├── requirements.txt
└── README.md
```

# 🚀 Automated YouTube Content Factory

Ky projekt është një sistem i automatizuar për menaxhimin e dy kanaleve YouTube (Kids & Sports). Qëllimi është maksimizimi i shikueshmërisë përmes analizës së trendeve dhe krijimit të përmbajtjes unike.

## 📊 Kanale

| Kanali | Stili | Përmbajtja | Frekuenca |
|--------|-------|------------|-----------|
| **Kids (Aura & Luna)** | Animacione Cortana + fëmijë | Këngë origjinale, fakte edukative, pa muzikë | Çdo 6 orë |
| **Sports (FIFA)** | News TV-style, tekst-only | Rekorde, statistika, lajme virale pa foto lojtaresh | Çdo 6 orë |

## 🛠 Workflow Strategy
- **Trend Detection:** Monitorim i Google Trends për Kids dhe Football Highlights.
- **Production Pipeline:** 1 Long-form video + 2 Shorts për çdo trend.
- **Anti-Ban Protocol:** Random delays (1-15 min), metadata unike, `MadeForKids` flag i saktë.
- **Policy Compliance:** Përdorim i efekteve unike, voiceovers (edge-tts) dhe editimit transformues për të respektuar rregullat e YouTube.

## 🛡 Security Protocol
- **Çelësat API** janë të mbrojtur përmes **GitHub Secrets**.
- **Refresh Token** i veçantë për çdo kanal (`YOUTUBE_REFRESH_TOKEN` për Kids, `FIFA_REFRESH_TOKEN` për FIFA).
- Asnjëherë nuk publikohen çelësa në kod.

## 📁 Project Structure

```
youtube-auto-football/
├── .github/workflows/       # GitHub Actions (auto-upload.yml, auto-upload-fifa.yml)
├── src/
│   ├── main.py              # Pipeline kryesore
│   ├── config.py            # Lexon environment variables
│   ├── kids_song_generator.py    # 7 këngë origjinale për fëmijë
│   ├── kids_animation_generator.py # Animacione Cortana + fëmijë
│   ├── viral_shorts.py      # Kids shorts me Cortana
│   ├── fifa_script_generator.py  # Template lajmesh futbolli
│   ├── video_generator.py   # Text-only news-style video
│   ├── fifa_shorts.py       # FIFA shorts text-only
│   ├── trends_fetcher.py    # Google Trends integration
│   ├── youtube_uploader.py  # YouTube API upload
│   └── config.py            # Configuration
├── requirements.txt
└── README.md
```

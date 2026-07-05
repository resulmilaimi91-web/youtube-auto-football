# YouTube Auto Kids Channel - STRATEGY DOCUMENT

## Qellimi
Automatizimi i nje kanali YouTube per femije (Kids Channel) per postim konstant me permbajtje origjinale, duke ndjekur Google Trends dhe rregullat e YouTube, per te arritur monetizimin.

---

## KANALI
**YouTube Handle:** `@CortanaKidsSongs`  
**Link:** https://www.youtube.com/@CortanaKidsSongs  
**Made for Kids:** ✅ PO  
**Monetizimi:** 1,000 subscribers + 4,000 watch hours (ose 10M Shorts views ne 90 dite)

---

## CIKLI I PUNES (AUTO)

```
Tracker 08:00 UTC
  → Analizon cila kenge/teme performon mire
  → Ruan ranking-un ne content_strategy.json
  →
Kids Song Generator
  → Lexon ranking-un nga content_strategy.json
  → Perparon temen me performancen me te mire
  →
Video Pipeline
  → Gjeneron Thumbnail personal (Cortana + femije + titull)
  → Gjeneron animacion me Cortana + 2 femije + sfond te animuar
  → Shton voiceover TTS (edge-tts) + background music
  → Shton SUBSCRIBE animation ne fund
  → Gjeneron 2 Shorts
  →
Upload
  → Anti-ban delay (rnd 60-300s para videos, 180-600s para shorts)
  → Upload ne YouTube
  → Thumbnail custom (perfshin Cortana, titull, yje, ngjyra)
  → Shton videon ne Playlist perkatese (ABC Songs, Animal Songs, etj.)
  →
Tracker tjeter (08:00 UTC)
  → Mat rezultatet
  → Perserit loop-in
```

---

## ORARI I POSTIMEVE
- **2 Video + 2 Shorts** cdo dite
- **00:00 UTC** - Video e pare
- **12:00 UTC** - Video e dyte
- Anti-ban delays: 60-300s para upload, 300-900s para gjenerimit te shorts, 180-600s ndermjet shorts

---

## 15 KENGET (7 klasike + 8 edukative)

| # | Titulli | Tema | Edukative? |
|---|---------|------|-----------|
| 1 | The Rainbow Song | rainbow | Jo |
| 2 | Bunny Hop Hop | bunny | Jo |
| 3 | Counting Stars | stars | Po |
| 4 | Happy Little Fish | fish | Jo |
| 5 | The Color Train | train | Po |
| 6 | Kitty Cat Song | cat | Jo |
| 7 | Morning Sunshine | morning | Jo |
| 8 | ABC Animal Song | abc | Po |
| 9 | Ten Little Numbers | numbers | Po |
| 10 | Shapes All Around | shapes | Po |
| 11 | Days of the Week Song | days | Po |
| 12 | Head Shoulders Knees & Toes | body | Po |
| 13 | Fruit Song Yummy Yummy | fruits | Po |
| 14 | Weather Song | weather | Po |
| 15 | Vroom Vroom Vehicles | vehicles | Po |

---

## KARAKTERET E ANIMACIONIT
- **Cortana** - Karakter blu me glow, sy te medhenj, buzeqeshje, pika ndricuese rreth saj
- **Femija 1** - Me kapel te kuqe, bluze portokalli
- **Femija 2** - Me bluze blu
- **Sfondi** - I animuar sipas temes (yje per "stars", lule per "rainbow", peshq per "fish", trajna per "train")

---

## THUMBNAILS
- 1280x720 pixele
- Cortana ne qender + 2 femije
- Titull ne fund me background te kuq
- Yje dekorativ
- Tekst "Sing Along & Learn!" ne siper
- E krijuar programatikisht per cdo video

---

## SEO (Tituj, Pershkrime, Hashtags)
- Tituj origjinale me keywords te trendit
- Pershkrime me:
  - Subscribe CTA me zile
  - Linke ne kenget e tjera
  - 7-8 hashtags (kidssong, nurseryrhyme, singalong, kidsmusic, toddler, preschool, etj.)
- Tags me keywords relevante (educational, learning, abc, numbers, etj.)

---

## SUBSCRIBE ANIMATION
- 3 sekonda ne fund te cdo video
- Buton i kuq "SUBSCRIBE"
- 2 zile te arta (djathtas/majtas)
- 40 yje te arte ne background
- "🔔 New kids songs every day!"
- "♪ Cortana Kids Songs ♪"

---

## PLAYLISTS AUTOMATIKE
Kur nje video postohet, shtohet automatikisht ne listen perkatese:

| Tema | Playlist |
|------|----------|
| abc | ABC & Alphabet Songs |
| numbers, stars | Counting & Numbers Songs |
| shapes | Shapes Learning Songs |
| rainbow, colors | Colors & Rainbow Songs |
| train | Fun Train Songs |
| bunny, fish, cat | Animal Songs for Kids |
| morning, days | Daily Routine Songs |
| body | Body Parts Songs |
| fruits | Healthy Eating Songs |
| weather | Weather & Nature Songs |
| vehicles | Vehicles & Transportation Songs |

---

## TRACKER & CONTENT OPTIMIZER
**Kur punon:** 08:00 UTC cdo dite
**Cfare mat:**
- Subscribers (+0.9% dite)
- Total Views
- Watch Hours
- Shorts Views (90 dite)
- Performance per video (views/score)
- Performance per teme (avg views per theme)

**Cfare optimizon:**
- Zgjedh temen me performancen me te mire per videon e ardhsme
- Krijon ranking-un e temave

---

## ANTI-BAN STRATEGY
- **Pa material me copyright** - gjithcka origjinale (kenget, muzika, animacionet, zeri)
- **Delays random** (1-15 minuta) para upload
- **Metadata unike** per cdo video
- **Made for Kids = YES** (perputhet me rregullat COPPA)
- **2 postime/dite** (jo me shume per te shmangur ban-in)
- **Quota cache** - nese YouTube kthen uploadLimitExceeded, skip per 12 ore

---

## FILES KRYESORE
| File | Funksioni |
|------|-----------|
| `src/kids_song_generator.py` | Gjeneron kenge (15 template) + SEO |
| `src/kids_animation_generator.py` | Animacion Cortana + femije + subscribe |
| `src/viral_shorts.py` | Shorts per Kids |
| `src/thumbnail_generator.py` | Thumbnail personal (1280x720 + 1080x1920) |
| `src/subscribe_animation.py` | Subscribe clip 3-sekondesh |
| `src/playlist_manager.py` | Auto-playlists permes YouTube API |
| `src/music_generator.py` | Background music royalty-free |
| `src/tracker.py` | Monitorim + content optimization |
| `src/main.py` | Pipeline kryesore |
| `src/youtube_uploader.py` | Upload me refresh token |
| `src/trends_fetcher.py` | Google Trends integration |
| `src/config.py` | Environment variables |
| `content_strategy.json` | Ranking-u i temave (auto-gjeneruar nga tracker) |
| `.github/workflows/auto-upload.yml` | Cron per postime (00:00, 12:00 UTC) |
| `.github/workflows/tracker.yml` | Cron per tracker (08:00 UTC) |

---

## GITHUB REPO
**URL:** https://github.com/resulmilaimi91-web/youtube-auto-football  
**Secrets:** YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN, CHANNEL_NAME

---

## PROGRESSI AKTUAL (5 Korrik 2026)
- **Videos:** 12
- **Subscribers:** 9 / 1,000 (0.9%)
- **Total Views:** 93
- **Watch Hours:** 0.0 / 4,000
- **Monetization:** Jo ende

---

## CONTENT STRATEGY.JSON (shembull)
```json
{
  "theme_scores": {
    "rainbow": { "total_views": 45, "count": 3, "avg_views": 15.0 },
    "stars": { "total_views": 20, "count": 2, "avg_views": 10.0 }
  },
  "best_theme": "rainbow",
  "theme_rankings": ["rainbow", "stars", "abc", "numbers", "cat"],
  "recommended_themes": ["rainbow", "stars", "abc"],
  "recommendation_note": "Based on performance, prioritize: rainbow, stars, abc"
}
```

---

## NEXT STEPS PER FITIM
1. **Vazhdo postime** - 2 video/dite pa nderprerje
2. **Shiko tracker** cdo mengjes per progres
3. **Pas 30 ditesh** - analizo trendin e rritjes
4. **Nese rritja eshte < 50 subs/muaj** - shto me shume permbajtje edukative (kerkesa me te larta)
5. **Pasi arrin 500 subs** - fillo te perdorish YouTube Community posts
6. **Pasi arrin 1,000 subs** - apliko per YouTube Partner Program

# YouTube Auto Football - Sistem i Automatizuar 24/7

Sistem automatik që gjeneron video futbolli dhe i ngarkon në YouTube çdo 6 orë.

## Si funksionon?

1. **Merr të dhëna** nga TheSportsDB dhe BBC Sport për ndeshjet dhe lajmet e fundit
2. **Gjeneron script-in** automatikisht në shqip
3. **Krijon videon** me titra, zë (TTS në shqip) dhe sfond
4. **Ngarkon në YouTube** automatikisht
5. **Përsëritet çdo 6 orë** 24/7 përmes GitHub Actions

## Instalimi

### 1. Krijoni një YouTube API Key

1. Shkoni te [Google Cloud Console](https://console.cloud.google.com/)
2. Krijoni një projekt të ri
3. Aktivizoni **YouTube Data API v3**
4. Krijoni **OAuth 2.0 Credentials** (Desktop app)
5. Shkarkoni `client_secret.json`

### 2. Konfigurimi në GitHub

1. **Fork/Clone** këtë repo në GitHub
2. Shkoni te Settings → Secrets and variables → Actions
3. Shtoni këto **repository secrets**:

| Secret | Përshkrimi |
|--------|------------|
| `YOUTUBE_CLIENT_ID` | Client ID nga Google Cloud |
| `YOUTUBE_CLIENT_SECRET` | Client Secret nga Google Cloud |
| `YOUTUBE_REFRESH_TOKEN` | Refresh token (shiko më poshtë) |
| `CHANNEL_NAME` | Emri i kanalit tënd (opsional) |
| `UPLOAD_SCHEDULE_HOURS` | Sa orë mes çdo upload-i (default: 6) |

### 3. Gjenerimi i Refresh Token-it

Ekzekutoni lokalisht:
```bash
pip install -r requirements.txt
python -c "from src.youtube_uploader import get_authenticated_service; get_authenticated_service()"
```

Kjo do të hapë një browser për login. Pasi të autentifikoheni, refresh token do të ruhet në `output/token.pickle`.

### 4. Aktivizimi i GitHub Actions

Pasi secret-et janë konfiguruar:
1. Shkoni te GitHub → Actions
2. Enable workflows
3. Workflow do të ekzekutohet automatikisht çdo 6 orë

Mund ta ekzekutoni manualisht nga GitHub → Actions → "Run workflow".

## Struktura

```
youtube-auto-football/
├── .github/workflows/    # GitHub Actions
├── src/
│   ├── config.py          # Konfigurimi
│   ├── football_data.py   # Marrja e të dhënave
│   ├── script_generator.py# Gjenerimi i script-it
│   ├── video_generator.py # Krijimi i videos
│   ├── youtube_uploader.py# Upload në YouTube
│   └── main.py            # Main pipeline
├── requirements.txt
└── README.md
```

## Personalizimi

Mund të ndryshoni:
- **Template-t e videove** në `script_generator.py`
- **Frequncën e upload-it** në `.github/workflows/auto-upload.yml` (cron)
- **Stilin e videos** në `video_generator.py`
- **Futni OpenAI API Key** për script më kreativë

## Këshilla për fitime

- Postoni **vazhdimisht** (çdo 6 orë) për të rritur reach-in
- Përdorni **titull dhe thumbnail** tërheqës
- Targetoni **fjalë kyçe** si: golat e javës, highlights, futboll shqip
- Aktivizoni **monetization** në YouTube pas 1000 subscribers
- Lidheni me **programe affiliate** për baste sportive / merchandise

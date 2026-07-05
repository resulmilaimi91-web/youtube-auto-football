import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")

client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uris": ["http://localhost"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_local_server(port=8080, prompt="consent", include_granted_scopes=True)

print("\n" + "=" * 60)
print("FIFA REFRESH TOKEN (copy this to GitHub Secrets):")
print("=" * 60)
print(creds.refresh_token)
print("=" * 60)
print("\nAdd as FIFA_REFRESH_TOKEN in GitHub -> Settings -> Secrets and variables -> Actions")

with open("fifa_token.pickle", "wb") as f:
    pickle.dump(creds, f)
print("\nToken also saved to fifa_token.pickle")

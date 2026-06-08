import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.youtube_uploader import get_authenticated_service
from googleapiclient.errors import HttpError

youtube = get_authenticated_service()

try:
    request = youtube.videos().list(myRating="like", part="snippet", maxResults=50)
    videos = request.execute()
    for v in videos.get("items", []):
        vid = v["id"]
        title = v["snippet"]["title"]
        try:
            youtube.videos().delete(id=vid).execute()
            print(f"Deleted: {title} ({vid})")
        except HttpError as e:
            print(f"Could not delete {vid}: {e}")
except HttpError as e:
    print("Error listing videos:", e)

try:
    request = youtube.search().list(forMine=True, part="snippet", type="video", maxResults=50)
    data = request.execute()
    for item in data.get("items", []):
        vid = item["id"]["videoId"]
        title = item["snippet"]["title"]
        try:
            youtube.videos().delete(id=vid).execute()
            print(f"Deleted: {title} ({vid})")
        except HttpError as e:
            print(f"Could not delete {vid}: {e}")
except HttpError as e:
    print("Error searching videos:", e)

print("Done cleaning up videos!")

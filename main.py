import os
import requests


def getVideoData(video_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    }

    request_data = requests.get(
        f"https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{video_id}%5D", headers=headers).json()

    return request_data


if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    if not os.path.exists("downloads/videos"):
        os.makedirs("downloads/videos")
    if not os.path.exists("downloads/thumbnails"):
        os.makedirs("downloads/thumbnails")

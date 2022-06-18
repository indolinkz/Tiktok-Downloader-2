import os
import requests

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    if not os.path.exists("downloads/videos"):
        os.makedirs("downloads/videos")
    if not os.path.exists("downloads/thumbnails"):
        os.makedirs("downloads/thumbnails")

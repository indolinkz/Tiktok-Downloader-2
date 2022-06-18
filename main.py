import os
import requests


def getVideoData(video_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    }

    request_data = requests.get(
        f"https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{video_id}%5D", headers=headers).json()

    return request_data


def downloadSingleVideo():
    with_watermark = None
    print("Download the video\n[1] With Watermark\n[2] Without Watermark")
    while with_watermark != 1 and with_watermark != 2:
        with_watermark = int(input("[>] "))

    print()
    video_url = input("[>] Video URL : ")

    video_id = video_url.split("/")[5]
    if "?" in video_url:
        video_id = video_id[:video_id.find('?')]

    if os.path.exists(f"./downloads/videos/{video_id}-wm.mp4") and with_watermark == 1:
        print("[!] Video Already Downloaded!")
        return
    if os.path.exists(f"./downloads/videos/{video_id}-no-wm.mp4") and with_watermark == 2:
        print("[!] Video Already Downloaded!")
        return

    data = getVideoData(video_id)

    if with_watermark == 1:
        download_url = data["aweme_details"][0]["video"]["download_addr"]["url_list"][0]
    else:
        download_url = data["aweme_details"][0]["video"]["play_addr"]["url_list"][0]

    with open(f'./downloads/videos/{video_id}-{"wm" if with_watermark == 1 else "no-wm"}.mp4', 'wb') as out_file:
        video_bytes = requests.get(f'{download_url}.mp4', stream=True)
        out_file.write(video_bytes.content)

    print("[!] Video Downloaded Successfully!")


def downloadVideoThumbnail():
    video_url = input("[>] Video URL : ")

    video_id = video_url.split("/")[5]
    if "?" in video_url:
        video_id = video_id[:video_id.find('?')]

    if os.path.exists(f"./downloads/thumbnails/{video_id}-thumbnail.jpeg"):
        print("[!] Thumbnail Already Downloaded!")
        return

    data = getVideoData(video_id)

    download_url = data["aweme_details"][0]["video"]["origin_cover"]["url_list"][0]

    with open(f'./downloads/thumbnails/{video_id}-thumbnail.jpeg', 'wb') as out_file:
        image_bytes = requests.get(f'{download_url}.mp4', stream=True)
        out_file.write(image_bytes.content)

    print("[!] Thumbnail Downloaded Successfully!")


if __name__ == "__main__":
    if not os.path.exists("./downloads"):
        os.makedirs("./downloads")
    if not os.path.exists("./downloads/videos"):
        os.makedirs("./downloads/videos")
    if not os.path.exists("./downloads/thumbnails"):
        os.makedirs("./downloads/thumbnails")

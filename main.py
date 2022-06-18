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


def downloadAllVidsFromUser():
    with_watermark = None
    print("Download the videos\n[1] With Watermark\n[2] Without Watermark")
    while with_watermark != 1 and with_watermark != 2:
        with_watermark = int(input("[>] "))

    print()
    video_url = input("[>] Insert one Video URL from the user : ")

    video_id = video_url.split("/")[5]
    if "?" in video_url:
        video_id = video_id[:video_id.find('?')]

    data = getVideoData(video_id)

    sec_uid = data["aweme_details"][0]["author"]["sec_uid"]

    request_url = f"https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/post/?sec_user_id={sec_uid}&count=33&device_id=9999999999999999999&max_cursor=0&aid=1180"
    request_headers = {
        "accept-encoding": "gzip",
        "user-agent": "com.ss.android.ugc.trill/240303 (Linux; U; Android 12; en_US; Pixel 6 Pro; Build/SP2A.220405.004;tt-ok/3.10.0.2)",
        "x-gorgon": "0"
    }
    request_data = requests.get(request_url, headers=request_headers).json()

    username = request_data["aweme_list"][0]["author"]["unique_id"]
    if not os.path.exists(f"./downloads/users/{username}"):
        os.makedirs(f"./downloads/users/{username}")
    if not os.path.exists(f"./downloads/users/{username}/wm"):
        os.makedirs(f"./downloads/users/{username}/wm")
    if not os.path.exists(f"./downloads/users/{username}/no-wm"):
        os.makedirs(f"./downloads/users/{username}/no-wm")

    videos = request_data["aweme_list"]

    print(f"{username} have {len(videos)} published videos. Downloading them...\nVideos already downloaded will be skipped.\n")

    count = 0

    if with_watermark == 1:
        for video in videos:
            count += 1

            download_url = video["video"]["download_addr"]["url_list"][0]
            uri = video["video"]["download_addr"]["uri"]

            if os.path.exists(f"./downloads/users/{username}/wm/{uri}.mp4"):
                print(
                    f"[!] Video Number {count} already Exists! Skipping It...")
                continue

            with open(f'./downloads/users/{username}/wm/{uri}.mp4', 'wb') as out_file:
                video_bytes = requests.get(f'{download_url}.mp4', stream=True)
                out_file.write(video_bytes.content)
                print(f"[!] Video Number {count} downloaded")
    else:
        for video in videos:
            count += 1

            download_url = video["video"]["play_addr"]["url_list"][0]
            uri = video["video"]["play_addr"]["uri"]

            if os.path.exists(f"./downloads/users/{username}/no-wm/{uri}.mp4"):
                print(
                    f"[!] Video Number {count} already Exists! Skipping It...")
                continue

            with open(f'./downloads/users/{username}/no-wm/{uri}.mp4', 'wb') as out_file:
                video_bytes = requests.get(f'{download_url}.mp4', stream=True)
                out_file.write(video_bytes.content)
                print(f"[!] Video Number {count} downloaded")

    print()
    print(f"[!] Successfully updated/downloaded all videos from {username}")


if __name__ == "__main__":
    if not os.path.exists("./downloads"):
        os.makedirs("./downloads")
    if not os.path.exists("./downloads/videos"):
        os.makedirs("./downloads/videos")
    if not os.path.exists("./downloads/thumbnails"):
        os.makedirs("./downloads/thumbnails")

import yt_dlp
import os
import time
import random


# =========================
# Anti Rate Limit Handler
# =========================
def safe_extract_info(ydl, url, max_retries=5):
    for attempt in range(max_retries):
        try:
            delay = random.uniform(1.5, 4.0)
            print(f"\n⏳ Delay sebelum request: {delay:.2f} detik")
            time.sleep(delay)

            return ydl.extract_info(url, download=False)

        except Exception as e:
            error_msg = str(e)
            print(f"\n⚠️ Error: {error_msg}")

            if "429" in error_msg or "not a bot" in error_msg.lower():
                wait_time = (2 ** attempt) + random.uniform(1, 3)

                print(f"🚫 Rate limit terdeteksi")
                print(f"🔁 Retry ke-{attempt+1} dalam {wait_time:.2f} detik...\n")

                time.sleep(wait_time)
            else:
                raise e

    raise Exception("❌ Gagal setelah beberapa retry (rate limit terus).")


# =========================
# Get format + size preview
# =========================
def get_formats(info):
    formats = info.get("formats", [])
    result = []

    for f in formats:
        if f.get("vcodec") != "none" and f.get("acodec") == "none":
            height = f.get("height")
            filesize = f.get("filesize") or f.get("filesize_approx")

            if height and height >= 360:
                size_mb = filesize / (1024 * 1024) if filesize else 0

                result.append({
                    "format_id": f["format_id"],
                    "height": height,
                    "size": size_mb
                })

    # sort by resolution
    result = sorted(result, key=lambda x: x["height"])

    return result


# =========================
# Progress Hook
# =========================
def my_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "")
        speed = d.get("_speed_str", "")
        eta = d.get("_eta_str", "")
        print(f"\r📥 {percent} | {speed} | ETA {eta}", end="")

    elif d["status"] == "finished":
        print("\n🎞️ Menggabungkan video & audio...")


# =========================
# Main Function
# =========================
def download_video():

    url = input("\nMasukkan link YouTube: ")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    download_folder = os.path.join(script_dir, "Downloads")
    cookies_path = os.path.join(script_dir, "Cookies", "cookies.txt")

    os.makedirs(download_folder, exist_ok=True)

    output_path = os.path.join(download_folder, "%(title)s.%(ext)s")

    # =========================
    # OPTIONS UNTUK EXTRACT INFO
    # =========================
    # info_opts = {
    #     "quiet": True,
    #     "cookies": cookies_path if os.path.exists(cookies_path) else None,
    #     # "js_runtimes": [r"node:C:\Program Files\nodejs\node.exe"],
    #     "js_runtimes": {    "node": {
    #     "path": r"C:\Program Files\nodejs\node.exe"
    #       }
    #     }
    # }
    info_opts = {
    "quiet": True,
    "cookies": cookies_path if os.path.exists(cookies_path) else None,

    "js_runtimes": {
        "node": {
            "path": r"C:\Program Files\nodejs\node.exe"
        }
    },

    "extractor_args": {
        "youtube": {
            "player_client": ["android"],
        }
    },
    }

    with yt_dlp.YoutubeDL(info_opts) as ydl:
        info = safe_extract_info(ydl, url)

    print(f"\n🎬 Judul: {info.get('title')}")

    formats = get_formats(info)

    if not formats:
        print("❌ Tidak ada format ditemukan")
        return

    print("\n📊 Pilih kualitas:")
    for i, f in enumerate(formats):
        print(f"{i+1}. {f['height']}p - {f['size']:.2f} MB")

    choice = int(input("Pilih nomor: ")) - 1
    selected = formats[choice]

    # =========================
    # OPTIONS UNTUK DOWNLOAD
    # =========================
    ydl_opts = {
        "format": f"{selected['format_id']}+bestaudio/best",
        "outtmpl": output_path,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "progress_hooks": [my_hook],

        # retry internal yt-dlp
        "retries": 5,
        "fragment_retries": 5,
        "sleep_interval": 1,
        "max_sleep_interval": 5,

        # cookies + JS runtime
        "cookies": cookies_path if os.path.exists(cookies_path) else None,
        "js_runtimes": [r"node:C:\Program Files\nodejs\node.exe"],

        "extractor_args": {
        "youtube": {
            "player_client": ["android"],
        }
        },
    }

    print("\n🚀 Memulai download...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("\n✅ Download selesai!")


# =========================
# LOOP
# =========================
if __name__ == "__main__":
    while True:
        download_video()

        lagi = input("\nDownload video lain? (y/n): ").lower()
        if lagi != "y":
            break
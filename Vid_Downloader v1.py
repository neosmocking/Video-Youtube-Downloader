import yt_dlp
import os


def download_video():

    url = input("Masukkan link YouTube: ")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_folder = os.path.join(script_dir, "Downloads")
    cookies_path = os.path.join(script_dir, "Cookies", "cookies.txt")

    os.makedirs(download_folder, exist_ok=True)

    output_path = os.path.join(download_folder, "%(title)s.%(ext)s")

    # opsi awal untuk mengambil info
    info_opts = {
        "quiet": True,
        "cookies": cookies_path if os.path.exists(cookies_path) else None
    }

    with yt_dlp.YoutubeDL(info_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    print("\nResolusi tersedia:")

    formats = info["formats"]

    resolutions = set()

    for f in formats:
        if f.get("height"):
            resolutions.add(f["height"])

    resolutions = sorted(resolutions)

    for r in resolutions:
        print(f"{r}p")

    choice = input("\nPilih resolusi (contoh: 720 / 1080 / 1440): ")

    format_string = f"bestvideo[height<={choice}]+bestaudio/best"

    ydl_opts = {
        "format": format_string,
        "outtmpl": output_path,
        "merge_output_format": "mp4",
        "progress_hooks": [my_hook],
        "noplaylist": True
    }

    if os.path.exists(cookies_path):
        ydl_opts["cookies"] = cookies_path
        print("Menggunakan cookies login.")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("\nMemulai download...")
        ydl.download([url])

    print("Download selesai.")


def my_hook(d):

    if d["status"] == "downloading":
        percent = d.get("_percent_str", "")
        speed = d.get("_speed_str", "")
        eta = d.get("_eta_str", "")
        print(f"\r{percent} | {speed} | ETA {eta}", end="")

    elif d["status"] == "finished":
        print("\nMenggabungkan video dan audio...")


if __name__ == "__main__":

    while True:

        download_video()

        again = input("\nDownload video lain? (y/n): ").lower()

        if again != "y":
            break
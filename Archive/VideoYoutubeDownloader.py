import yt_dlp
import os

def download_video():
    """Fungsi download menggunakan yt-dlp dengan opsi kualitas terbaik."""
    link = input("Masukkan link video YouTube: ")

    # Opsi konfigurasi untuk yt-dlp
    ydl_opts = {
        # Pilih format terbaik: video mp4 + audio m4a. Jika tidak ada, pilih mp4 terbaik.
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        # Nama file output: Judul Video.ext
        'outtmpl': '%(title)s.%(ext)s',
        # Jangan download playlist jika link adalah playlist
        'noplaylist': True,
        # Fungsi untuk menampilkan progress
        'progress_hooks': [my_hook],
    }

    # Cek keberadaan FFmpeg untuk memberi tahu user
    ffmpeg_check = os.system("ffmpeg -version")
    if ffmpeg_check == 0:
        print("✅ FFmpeg ditemukan. File akan digabungkan secara otomatis jika perlu.")
    else:
        print("⚠️ FFmpeg tidak ditemukan. Untuk kualitas tinggi, video dan audio mungkin terpisah.")
        print("Install FFmpeg untuk penggabungan otomatis: https://ffmpeg.org/download.html")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("\n--- Mengambil info video... ---")
            info_dict = ydl.extract_info(link, download=False)
            print(f"Judul: {info_dict.get('title', 'Tidak diketahui')}")
            print(f"Channel: {info_dict.get('uploader', 'Tidak diketahui')}")
            print(f"Durasi: {info_dict.get('duration', 0) // 60}:{info_dict.get('duration', 0) % 60:02d} menit")
            
            print("\n--- Memulai Download... ---")
            print("yt-dlp akan otomatis memilih format terbaik yang tersedia.")
            ydl.download([link])
            print("\n✅ Download selesai!")
            
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {e}")

def my_hook(d):
    """Fungsi untuk menampilkan progress bar dari yt-dlp."""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\r[Mengunduh] {percent} | Kecepatan: {speed} | Sisa waktu: {eta}", end="")
    elif d['status'] == 'finished':
        filename = d.get('filename', 'file')
        print(f"\n✅ Selesai mendownload: {os.path.basename(filename)}")

if __name__ == "__main__":
    while True:
        download_video()
        another = input("\nIngin mendownload video lain? (y/n): ").lower()
        if another != 'y':
            break
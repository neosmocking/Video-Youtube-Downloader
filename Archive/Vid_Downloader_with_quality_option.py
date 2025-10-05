import yt_dlp
import os

def download_with_quality_selection():
    """Fungsi download menggunakan yt-dlp dengan opsi pemilihan kualitas."""
    link = input("Masukkan link video YouTube: ")

    # Opsi dasar untuk yt-dlp
    ydl_opts_base = {
        'quiet': True, # Kurangi output log agar lebih bersih
        'no_warnings': True,
        'extract_flat': False, # Dapatkan info detail
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
            print("\n--- Mengambil info video... ---")
            info_dict = ydl.extract_info(link, download=False)
            print(f"Judul: {info_dict.get('title', 'Tidak diketahui')}")
            print(f"Channel: {info_dict.get('uploader', 'Tidak diketahui')}")
            print(f"Durasi: {info_dict.get('duration', 0) // 60}:{info_dict.get('duration', 0) % 60:02d} menit")

            # Filter format untuk ditampilkan kepada user
            # Prioritaskan format yang sudah memiliki video dan audio (progressive)
            # Lalu tampilkan juga format video-only berkualitas tinggi (DASH)
            formats = info_dict.get('formats', [])
            
            # Buat daftar format yang mudah dibaca
            readable_formats = []
            seen_resolutions = set()

            for f in formats:
                # Lewatkan format yang tidak relevan (hanya audio, atau resolusi tidak diketahui)
                if f.get('vcodec') == 'none' or not f.get('height'):
                    continue

                resolution = f"{f['height']}p"
                ext = f.get('ext', 'N/A')
                filesize_mb = f.get('filesize_mb', f.get('filesize_approx_mb', 0))
                format_id = f['format_id']
                
                # Catatan untuk user
                note = ""
                if f.get('acodec') == 'none':
                    note = " (Video saja, akan digabung dengan audio terbaik)"
                
                # Hindari duplikasi resolusi dari codec yang berbeda untuk kemudahan
                if resolution not in seen_resolutions:
                    readable_formats.append({
                        'id': format_id,
                        'res': resolution,
                        'ext': ext,
                        'size': filesize_mb,
                        'note': note
                    })
                    seen_resolutions.add(resolution)

            if not readable_formats:
                print("❌ Tidak ada format video yang cocok ditemukan.")
                return

            # Urutkan dari resolusi tertinggi ke terendah
            readable_formats.sort(key=lambda x: int(x['res'].replace('p','')), reverse=True)

            print("\n--- Pilih Kualitas Video ---")
            for i, fmt in enumerate(readable_formats):
                size_str = f"{fmt['size']:.2f} MB" if fmt['size'] > 0 else "Ukuran tidak diketahui"
                print(f"{i+1}. Resolusi: {fmt['res']:<7} | Ukuran: {size_str:<15} | {fmt['note']}")

            # Validasi input user
            choice = -1
            while True:
                try:
                    choice = int(input("\nMasukkan nomor kualitas yang diinginkan: "))
                    if 1 <= choice <= len(readable_formats):
                        break
                    else:
                        print("Pilihan tidak valid. Masukkan nomor dari daftar.")
                except ValueError:
                    print("Input tidak valid. Masukkan angka.")

            selected_format_id = readable_formats[choice - 1]['id']

            # --- Mulai Download ---
            print(f"\n--- Memulai download dengan ID format: {selected_format_id} ---")

            # Opsi final untuk download
            ydl_opts_download = {
                'format': selected_format_id,
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True,
                'progress_hooks': [my_hook],
            }
            
            # Cek FFmpeg
            if os.system("ffmpeg -version") == 0:
                print("✅ FFmpeg ditemukan. File akan digabungkan secara otomatis jika perlu.")
            else:
                print("⚠️ FFmpeg tidak ditemukan. Jika memilih 'Video saja', file tidak akan digabung.")
            
            # Buat instance YoutubeDL baru dengan opsi download
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_downloader:
                ydl_downloader.download([link])
            
            print("\n✅ Download dan proses selesai!")

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
        download_with_quality_selection()
        another = input("\nIngin mendownload video lain? (y/n): ").lower()
        if another != 'y':
            break
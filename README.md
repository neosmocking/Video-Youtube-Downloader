# 🎬 YouTube Downloader (yt-dlp + Cookies + Resolution Picker)

Script Python sederhana untuk mendownload video YouTube dengan fitur:

- ✅ Pilih resolusi (720p, 1080p, 1440p, dll)
- ✅ Support video yang butuh login (via cookies)
- ✅ Auto merge video + audio (FFmpeg)
- ✅ Output rapi ke folder `Downloads`
---
## 📁 Struktur Folder

```
project
│
├─ downloader.py
├─ Downloads
└─ Cookies
└─ cookies.txt
```
---
## ⚙️ Requirements

Pastikan sudah install:

- Python 3.x
- yt-dlp
- FFmpeg
---
### Install yt-dlp:

```bash
pip install yt-dlp
```
---
### Install FFmpeg:

Download dari:
https://ffmpeg.org/download.html

Setelah install, pastikan FFmpeg sudah masuk ke PATH.
---
### 🔑 Cara Mengambil Cookies (Login YouTube)

Script ini menggunakan cookies agar bisa download video yang:

- butuh login
- age restricted
- atau kena "Sign in to confirm you're not a bot"
---
### Cara export cookies:

Gunakan extension Chrome:

Get cookies.txt LOCALLY

Langkah:

1. Install extension di Chrome
2. Login ke YouTube
3. Klik extension
4. Export cookies
5. Simpan sebagai: Cookies/cookies.txt
---
### ⚠️ WARNING (PENTING - KEAMANAN COOKIES)

File cookies.txt SANGAT SENSITIF.

Cookies ini berisi session login akun kamu. Artinya: Siapa pun yang memiliki file ini bisa mengakses akun kamu

* Tidak perlu password
* Tidak perlu login ulang
---
### ❗ Jangan lakukan ini:

- ❌ Upload ke GitHub
- ❌ Kirim ke orang lain
- ❌ Simpan di cloud publik
---
### ✅ Best Practice:

Tambahkan ke .gitignore:
```
Cookies/
```
Dan:

Gunakan hanya untuk kebutuhan pribadi, Hapus jika sudah tidak digunakan

---
### ▶️ Cara Menjalankan

```bash
python downloader.py
```
Langkah:

1. Masukkan link YouTube
2. Pilih resolusi (contoh: 720 / 1080 / 1440)
3. Tunggu hingga selesai
---
### 🎯 Cara Kerja

Script ini menggunakan:

- yt-dlp → mengambil video & audio
- FFmpeg → menggabungkan (merge)

YouTube menyimpan video dalam bentuk terpisah:

- 🎥 Video (tanpa audio)
- 🔊 Audio

Script akan:

1. Download keduanya
2. Merge menjadi 1 file .mp4
---
### 📉 Kenapa File Bisa Besar?

Semakin tinggi resolusi, semakin besar ukuran file:
```
Resolusi	Ukuran
720p	 -> kecil
1080p	 -> sedang
1440p	 -> besar
2160p	 -> sangat besar
```
---
### 🧠 Tips

- Gunakan 720p atau 1080p untuk ukuran lebih hemat
- Pastikan FFmpeg aktif agar kualitas maksimal
- Update cookies jika terjadi error login
---
### ❌ Troubleshooting

**Error: "Sign in to confirm you're not a bot"**

Solusi:
- Export ulang cookies
- Pastikan login YouTube saat export
- Jangan gunakan cookies lama

**Video tanpa audio / resolusi rendah**

Kemungkinan:

- FFmpeg tidak terinstall
- Format fallback ke kualitas rendah

**Cookies tidak terbaca**

Pastikan:
- Path: Cookies/cookies.txt
- Format benar (Netscape format)
- File tidak rusak
---
### 🚀 Future Improvement (Opsional)

- GUI Downloader
- Auto paste link dari clipboard
- Estimasi ukuran file sebelum download
- Integrasi dengan Internet Download Manager
---
### 📌 Disclaimer

Gunakan script ini untuk keperluan pribadi.
Hormati hak cipta dan kebijakan platform YouTube.
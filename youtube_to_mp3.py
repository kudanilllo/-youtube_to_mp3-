"""
Unduh audio dari video YouTube menjadi file MP3.

Persiapan (sekali saja):
    pip install yt-dlp
    Install FFmpeg dan pastikan bisa dipanggil dari terminal (perintah: ffmpeg -version)

Cara pakai:
    python youtube_ke_mp3.py
"""

import os
import yt_dlp


def unduh_mp3(url: str, folder_tujuan: str = "unduhan_mp3") -> None:
    os.makedirs(folder_tujuan, exist_ok=True)

    opsi = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(folder_tujuan, "%(title)s.%(ext)s"),
        "noplaylist": True,  # hanya satu video, bukan seluruh playlist
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",  # kbps
            }
        ],
    }

    with yt_dlp.YoutubeDL(opsi) as ydl:
        ydl.download([url])

    print(f"\nSelesai! File tersimpan di folder: {os.path.abspath(folder_tujuan)}")


if __name__ == "__main__":
    link = input("Masukkan link YouTube: ").strip()
    if link:
        try:
            unduh_mp3(link)
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
    else:
        print("Link tidak boleh kosong.")

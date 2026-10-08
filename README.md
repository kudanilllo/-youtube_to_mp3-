# YouTube ke MP3

Skrip Python sederhana untuk mengunduh audio dari video YouTube dan menyimpannya sebagai file **MP3**, sehingga bisa diputar secara offline.

Skrip ini memakai [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) untuk mengunduh audio dan [FFmpeg](https://ffmpeg.org) untuk mengonversinya ke format MP3.

---

## Daftar Isi

- [Fitur](#fitur)
- [Kebutuhan](#kebutuhan)
- [Instalasi](#instalasi)
- [Cara Menggunakan](#cara-menggunakan)
- [Struktur Proyek](#struktur-proyek)
- [Penjelasan Kode](#penjelasan-kode)
- [Cara Kerja](#cara-kerja)
- [Kustomisasi](#kustomisasi)
- [Pemecahan Masalah](#pemecahan-masalah)
- [Catatan Penggunaan](#catatan-penggunaan)

---

## Fitur

- Mengunduh audio dari satu link video YouTube.
- Mengonversi otomatis ke format MP3 (kualitas 192 kbps secara bawaan).
- Menyimpan hasil ke folder `unduhan_mp3` dengan nama file sesuai judul video.
- Penanganan error sederhana agar program tidak langsung berhenti tanpa pesan.

---

## Kebutuhan

| Kebutuhan | Fungsi | Keterangan |
|---|---|---|
| Python 3.8+ | Menjalankan skrip | [python.org](https://www.python.org/downloads/) |
| yt-dlp | Mengunduh audio dari YouTube | Library Python, dipasang lewat `pip` |
| FFmpeg | Mengonversi audio menjadi MP3 | Program terpisah, **bukan** library Python |

> Modul `os` yang dipakai di skrip sudah bawaan Python, jadi tidak perlu dipasang.

---

## Instalasi

### 1. Pasang yt-dlp

```bash
pip install yt-dlp
```

Cek apakah library sudah terpasang:

```bash
python -c "import yt_dlp; print(yt_dlp.version.__version__)"
```

### 2. Pasang FFmpeg

**Windows** (PowerShell):

```powershell
winget install --id Gyan.FFmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt install ffmpeg
```

**macOS:**

```bash
brew install ffmpeg
```

### 3. Cek FFmpeg

```bash
ffmpeg -version
```

Jika muncul informasi versi, FFmpeg sudah siap. Pada Windows, tutup lalu buka kembali terminal setelah instalasi agar PATH terbaca.

Jika masih belum dikenali, segarkan PATH di jendela PowerShell yang sama:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

---

## Cara Menggunakan

1. Simpan file `youtube_ke_mp3.py` di sebuah folder.
2. Buka terminal di folder tersebut.
3. Jalankan skrip:

   ```bash
   python youtube_ke_mp3.py
   ```

   Di Linux atau macOS, gunakan `python3` jika `python` tidak dikenali.

4. Saat muncul tulisan `Masukkan link YouTube:`, tempel link video lalu tekan **Enter**.
5. Tunggu sampai muncul pesan `Selesai!`.
6. Hasil unduhan ada di folder `unduhan_mp3`.

Untuk membuka folder hasil di Windows:

```powershell
explorer unduhan_mp3
```

### Contoh tampilan

```
Masukkan link YouTube: https://www.youtube.com/watch?v=XXXXXXXXXXX
[youtube] Extracting URL: ...
[download] Destination: unduhan_mp3/Judul Video.webm
[ExtractAudio] Destination: unduhan_mp3/Judul Video.mp3

Selesai! File tersimpan di folder: C:\Users\nama\Documents\unduhan_mp3
```

---

## Struktur Proyek

```
.
├── youtube_ke_mp3.py   # Skrip utama
├── README.md           # Dokumentasi
└── unduhan_mp3/        # Folder hasil (dibuat otomatis saat skrip dijalankan)
```

---

## Penjelasan Kode

### Impor library

```python
import os
import yt_dlp
```

- `os` dipakai untuk membuat folder dan mengambil alamat lengkap folder tujuan.
- `yt_dlp` adalah library yang berkomunikasi dengan YouTube dan mengunduh audio.

### Fungsi `unduh_mp3`

```python
def unduh_mp3(url: str, folder_tujuan: str = "unduhan_mp3") -> None:
    os.makedirs(folder_tujuan, exist_ok=True)
```

Fungsi menerima dua parameter: `url` (link video) dan `folder_tujuan` (nama folder hasil, bawaannya `unduhan_mp3`). Baris `os.makedirs(..., exist_ok=True)` membuat folder tujuan, dan tidak akan error jika foldernya sudah ada.

### Opsi unduhan

```python
opsi = {
    "format": "bestaudio/best",
    "outtmpl": os.path.join(folder_tujuan, "%(title)s.%(ext)s"),
    "noplaylist": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}
```

| Opsi | Fungsi |
|---|---|
| `format: "bestaudio/best"` | Memilih audio dengan kualitas terbaik. Jika tidak tersedia, memakai format terbaik yang ada. |
| `outtmpl` | Pola nama file hasil. `%(title)s` diganti judul video, `%(ext)s` diganti ekstensi file. |
| `noplaylist: True` | Jika link berasal dari playlist, hanya video itu yang diunduh, bukan seluruh playlist. |
| `postprocessors` | Langkah pemrosesan setelah unduhan selesai (konversi memakai FFmpeg). |
| `FFmpegExtractAudio` | Mengambil bagian audio dari file yang diunduh. |
| `preferredcodec: "mp3"` | Format akhir yang diinginkan. |
| `preferredquality: "192"` | Kualitas audio dalam kbps. |

### Proses unduh

```python
with yt_dlp.YoutubeDL(opsi) as ydl:
    ydl.download([url])

print(f"\nSelesai! File tersimpan di folder: {os.path.abspath(folder_tujuan)}")
```

Objek `YoutubeDL` dibuat dengan opsi di atas, lalu `ydl.download([url])` menjalankan seluruh proses. Blok `with` memastikan sumber daya dibersihkan setelah selesai. Setelah itu, alamat lengkap folder hasil ditampilkan.

### Bagian utama program

```python
if __name__ == "__main__":
    link = input("Masukkan link YouTube: ").strip()
    if link:
        try:
            unduh_mp3(link)
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
    else:
        print("Link tidak boleh kosong.")
```

- `if __name__ == "__main__":` membuat bagian ini hanya berjalan jika file dijalankan langsung, bukan ketika diimpor dari file lain.
- `input(...).strip()` meminta link dari pengguna dan membuang spasi di awal atau akhir.
- `try/except` menangkap error (misalnya link salah atau tidak ada internet) lalu menampilkan pesannya, sehingga program tidak berhenti dengan tampilan error yang membingungkan.
- Jika link kosong, program menampilkan peringatan.

---

## Cara Kerja

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Pengguna     │    │ yt-dlp       │    │ FFmpeg       │    │ Folder       │
│ memasukkan   │ -> │ mengunduh    │ -> │ mengonversi  │ -> │ unduhan_mp3  │
│ link YouTube │    │ audio asli   │    │ ke MP3       │    │ (file .mp3)  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                     (.webm / .m4a)
```

1. **Input.** Pengguna memasukkan link video.
2. **Pengunduhan.** `yt-dlp` menghubungi YouTube, memilih aliran audio terbaik, lalu mengunduhnya. YouTube menyimpan audio dalam format seperti `.webm` atau `.m4a`, bukan MP3.
3. **Konversi.** Setelah unduhan selesai, `yt-dlp` memanggil FFmpeg secara otomatis untuk mengubah file audio itu menjadi MP3 dengan kualitas 192 kbps.
4. **Penyimpanan.** File MP3 disimpan di folder `unduhan_mp3` dengan nama sesuai judul video, dan file audio asli sebelum konversi dihapus otomatis.

---

## Kustomisasi

**Mengubah kualitas audio:**

```python
"preferredquality": "320",   # pilihan umum: 128, 192, 320
```

**Mengunduh seluruh playlist:**

```python
"noplaylist": False,
```

**Mengubah folder tujuan:** panggil fungsi dengan argumen kedua, misalnya:

```python
unduh_mp3(link, "musik_saya")
```

---

## Pemecahan Masalah

| Masalah | Penyebab | Solusi |
|---|---|---|
| `ModuleNotFoundError: No module named 'yt_dlp'` | Library belum terpasang di Python yang dipakai | Jalankan `pip install yt-dlp`, atau pastikan virtual environment sudah aktif |
| `ffmpeg not found` atau `ffprobe not found` | FFmpeg belum terpasang atau belum masuk PATH | Pasang FFmpeg, lalu buka ulang terminal atau segarkan PATH |
| `ffmpeg` tidak dikenali di PowerShell setelah instalasi | PATH di jendela terminal belum diperbarui | Tutup semua jendela terminal lalu buka lagi, atau jalankan perintah penyegaran PATH di atas |
| Peringatan `yt-dlp.exe ... is not on PATH` saat `pip install` | Folder `Scripts` milik Python belum masuk PATH | Tidak masalah untuk skrip ini, karena `yt-dlp` dipakai sebagai library Python |
| Error 403 atau unduhan gagal | `yt-dlp` sudah usang karena YouTube mengubah sistemnya | Jalankan `pip install -U yt-dlp` |
| `python` tidak dikenali (Linux/macOS) | Perintahnya bernama `python3` | Gunakan `python3 youtube_ke_mp3.py` |

---

## Catatan Penggunaan

Proyek ini dibuat untuk **tujuan belajar dan penggunaan pribadi**. Gunakan hanya untuk konten yang memang boleh kamu unduh, seperti video milikmu sendiri, konten berlisensi bebas, atau untuk keperluan pribadi yang diizinkan hukum di wilayahmu.

Mengunduh konten dari YouTube umumnya bertentangan dengan Ketentuan Layanan YouTube, dan konten berhak cipta dilindungi oleh hukum. Pengguna bertanggung jawab penuh atas cara ia memakai skrip ini.

---

## Lisensi

Tambahkan lisensi sesuai kebutuhan, misalnya [MIT License](https://choosealicense.com/licenses/mit/).

# Kalkulator Subnet & VLSM

## Docker

Aplikasi dan lingkungannya dibungkus menjadi satu image, sehingga berjalan sama di laptop, GitHub Actions, dan Render. Prasyarat: Docker Desktop terpasang dan menyala.

Build image:

```bash
docker build -t subnet-calculator .
```

Jalankan container (halaman terbuka di http://127.0.0.1:8000):

```bash
docker run -d --name subnet-app -p 8000:8000 subnet-calculator
```

Jalankan uji asap ke container lokal (harus menampilkan empat baris `[LULUS]`):

```bash
uv run python scripts/smoke_test.py http://127.0.0.1:8000
```

Hentikan dan hapus container setelah selesai:

```bash
docker rm -f subnet-app
```

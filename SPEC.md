# Spesifikasi Teknis: Kalkulator Subnet dan VLSM

## 1. Tujuan
Menyediakan kalkulator subnetting dan VLSM (Variable Length Subnet Mask) berbasis web untuk penggunaan akademik (terutama guru/siswa SMK TKJ). Sistem harus mampu menghitung alokasi IP IPv4 secara akurat menggunakan operasi *bitwise*, menangani kasus tepi (seperti prefix /31 dan /32), dan memberikan laporan kesalahan yang presisi atas input yang tidak valid.

## 2. Aturan Validasi
Seluruh input yang masuk ke sistem harus melewati proses validasi ketat berikut:
*   **Format IPv4:** Harus persis 4 oktet yang dipisahkan oleh titik (`.`).
*   **Nilai Oktet:** Setiap oktet harus berupa angka antara 0 hingga 255.
*   **Integritas Karakter:** 
    *   Tidak boleh ada spasi.
    *   Tidak boleh ada angka nol di depan (*leading zero*), contoh: `192.168.01.1` adalah tidak valid.
    *   Hanya menerima karakter numerik dan titik.
*   **Prefix CIDR:** Harus berupa bilangan bulat (integer) bernilai 0 hingga 32.
*   **Kebutuhan Host (VLSM):** Harus berupa array/list bilangan bulat, tidak boleh kosong, dan setiap elemen harus bernilai $\ge 1$.

## 3. Kontrak Fungsi

Logika inti berada di dalam `main.py` dan diuji melalui `test_main.py`.

### 3.1. `hitung_subnet(ip: str, prefix: int) -> dict`
Fungsi ini melakukan perhitungan subnet standar berbasis operasi *bitwise*.

*   **Logika Perhitungan:**
    *   `network` = `IP` AND `Subnet Mask`.
    *   Jumlah host standar = $2^{(32 - prefix)} - 2$ (untuk prefix 0-30).
*   **Penanganan Kasus Tepi (Edge Cases):**
    *   **Prefix /31:** Menggunakan standar *point-to-point* (RFC 3021). `usable_hosts` = 2, `first_host` = Network, `last_host` = Network + 1, `broadcast` = `None`.
    *   **Prefix /32:** Alamat host tunggal. `usable_hosts` = 1, `first_host` = `last_host` = IP itu sendiri, `network` = IP itu sendiri, `broadcast` = `None`.
*   **Return (Dictionary):**
    *   `mask` (str)
    *   `network` (str)
    *   `broadcast` (str | None)
    *   `first_host` (str)
    *   `last_host` (str)
    *   `usable_hosts` (int)
*   **Error Handling:** Menghasilkan (raise) `ValueError` jika gagal melewati Aturan Validasi.

### 3.2. `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`
Fungsi ini melakukan perhitungan fragmentasi blok IP secara dinamis berdasarkan kebutuhan host.

*   **Logika Perhitungan:**
    1.  Validasi format input `network_cidr` (misal: `192.168.1.0/24`). Pastikan IP tersebut adalah *Network Address* yang valid untuk prefix-nya.
    2.  Urutkan `kebutuhan_host` secara menurun (*descending*), dari yang terbesar ke terkecil.
    3.  Lakukan perulangan untuk setiap kebutuhan:
        *   Cari ukuran blok (pangkat 2) terkecil yang memadai (Kapasitas $\ge$ kebutuhan + 2).
        *   Batas minimum blok untuk host normal adalah /30 (4 IP).
        *   Alokasikan jaringan berurutan, mulai dari alamat `network_cidr` utama.
*   **Return:** List of dictionary. Setiap dictionary berisi:
    *   `kebutuhan` (int)
    *   `network_cidr` (str)
    *   (*serta seluruh *key* yang dikembalikan oleh fungsi `hitung_subnet`*)
*   **Error Handling (Raise `ValueError`):**
    *   Format `network_cidr` tidak valid atau bukan *Network Address*.
    *   Daftar kebutuhan kosong atau mengandung nilai $< 1$.
    *   Total kebutuhan blok melebihi kapasitas subnet induk yang diberikan.

## 4. Kontrak API

Sistem mengekspos endpoint melalui FastAPI. Setiap *exception* `ValueError` dari fungsi di atas harus ditangkap dan dikembalikan sebagai HTTP 400 Bad Request dengan format JSON: `{"detail": "<pesan error>"}`.

| Metode | Endpoint | Parameter / Body | Respons Sukses (HTTP 200) |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | *None* | Mengirimkan file `index.html`. |
| `GET` | `/api/subnet` | Query: `ip` (str), `prefix` (int) | JSON dari `hitung_subnet`. |
| `POST` | `/api/vlsm` | JSON Body: `{"network": str, "kebutuhan_host": list[int]}` | JSON list dari `alokasi_vlsm`. |

## 5. Halaman Web

Antarmuka pengguna diimplementasikan dalam satu file `index.html` tunggal (HTML/CSS/JS mandiri).
*   **Mode Antarmuka:** Terdapat navigasi/tab untuk beralih antara "Mode Subnet" dan "Mode VLSM".
*   **Tampilan Hasil:** Menggunakan format tabel yang mudah dibaca.
*   **Tampilan Error:** Menangkap HTTP status 400 dan menampilkan isi dari *field* `detail` dalam blok peringatan (alert) yang mencolok (misalnya dengan warna merah).
*   *Catatan: Validasi tetap harus dilakukan di backend, UI hanya mencegah input dasar HTML5.*

## 6. Tabel Test Case

Tabel ini digunakan sebagai acuan pembuatan fungsi *test* di `test_main.py` menggunakan framework `pytest`.

| Skenario | Input | Output / Hasil yang Diharapkan (Assertion) |
| :--- | :--- | :--- |
| **Normal Kelas B** | `172.16.5.130/25` | Network: `172.16.5.128`, Broadcast: `172.16.5.255`, Usable: 126 |
| **Blok Kecil (/30)** | `10.0.0.0/30` | Range: `10.0.0.1` - `10.0.0.2`, Broadcast: `10.0.0.3`, Usable: 2 |
| **P2P (/31)** | `192.168.1.0/31` | Range: `192.168.1.0` - `192.168.1.1`, Broadcast: `None`, Usable: 2 |
| **Loopback (/32)** | `192.168.1.5/32` | First/Last Host: `192.168.1.5`, Broadcast: `None`, Usable: 1 |
| **Oktet Melebihi Batas** | `256.1.1.1/24` | HTTP 400 Bad Request / raise ValueError |
| **Nol di Depan (Leading Zero)**| `192.168.01.1/24` | HTTP 400 Bad Request / raise ValueError |
| **Format IP Tidak Lengkap** | `192.168.1/24` | HTTP 400 Bad Request / raise ValueError |
| **Karakter Non-Numerik** | `abc.168.1.1/24` | HTTP 400 Bad Request / raise ValueError |
| **Input Kosong** | *(empty string)* | HTTP 400 Bad Request / raise ValueError |
| **Prefix Maksimal Lebar** | `192.168.1.1/33` | HTTP 400 Bad Request / raise ValueError |
| **Prefix Minus** | `192.168.1.1/-1` | HTTP 400 Bad Request / raise ValueError |
| **VLSM Berhasil** | Net: `192.168.1.0/24`<br>Host: `[100, 50, 20, 2]` | Subnet 1: `/25` (`192.168.1.0`)<br>Subnet 2: `/26` (`192.168.1.128`)<br>Subnet 3: `/27` (`192.168.1.192`)<br>Subnet 4: `/30` (`192.168.1.224`) |
| **VLSM Kapasitas Berlebih** | Net: `192.168.1.0/24`<br>Host: `[200, 100]` | HTTP 400 Bad Request / raise ValueError (kapasitas tidak muat) |

## 7. Di Luar Cakupan (Out of Scope)
Hal-hal berikut tidak diimplementasikan pada versi ini:
*   Dukungan untuk pengalamatan IPv6.
*   Sistem Autentikasi atau manajemen *user session*.
*   Penyimpanan riwayat perhitungan ke dalam *Database*.
*   Ekspor dokumen hasil ke PDF/Excel (dapat ditambahkan di pengembangan lanjutan, bukan bagian MVP).
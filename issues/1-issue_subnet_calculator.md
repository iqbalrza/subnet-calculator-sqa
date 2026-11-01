# [Feature] Kalkulator Subnet

## Deskripsi
Fitur Kalkulator Subnet IPv4 berbasis web yang ditujukan untuk pembelajaran jaringan (guru dan siswa SMK TKJ). Fitur ini menghitung parameter subnetting standar berbasis operasi bitwise, mendukung penanganan kasus tepi (/31 point-to-point RFC 3021 dan /32 host tunggal), serta validasi ketat terhadap input alamat IP dan prefix. Hasil perhitungan disediakan melalui endpoint `GET /api/subnet` dan diintegrasikan dengan antarmuka web pada `GET /`.

## Tugas
- [ ] Menyiapkan kerangka fungsi `hitung_subnet(ip: str, prefix: int) -> dict` dan endpoint API `GET /api/subnet`.
- [ ] Menulis test unit di `test_main.py` menggunakan `pytest` dan `pytest.mark.parametrize` mencakup seluruh skenario valid dan invalid (fase TDD merah).
- [ ] Mengimplementasikan logika validasi input IPv4 (tepat 4 oktet, rentang 0-255, tanpa spasi, tanpa angka nol di depan) dan prefix CIDR (bilangan bulat 0-32).
- [ ] Mengimplementasikan perhitungan subnet bitwise (`network`, `mask`, `broadcast`, `first_host`, `last_host`, `usable_hosts`).
- [ ] Mengintegrasikan endpoint API dengan antarmuka pengguna `index.html` (menampilkan hasil perhitungan dan pesan kesalahan dari field `detail`).
- [ ] Menjalankan verifikasi test hingga seluruh pengujian lulus (fase hijau).

## Kriteria Penerimaan
Berdasarkan tabel test pada `SPEC.md`:
1. **Normal Kelas B (`172.16.5.130/25`)**:
   - Network: `172.16.5.128`
   - Broadcast: `172.16.5.255`
   - First Host: `172.16.5.129`
   - Last Host: `172.16.5.254`
   - Usable Hosts: `126`
2. **Blok Kecil /30 (`10.0.0.0/30`)**:
   - Network: `10.0.0.0`
   - Broadcast: `10.0.0.3`
   - Range Host: `10.0.0.1` - `10.0.0.2`
   - Usable Hosts: `2`
3. **Point-to-Point /31 (`192.168.1.0/31`)**:
   - Standar RFC 3021: First Host `192.168.1.0`, Last Host `192.168.1.1`
   - Broadcast: `None`
   - Usable Hosts: `2`
4. **Loopback /32 (`192.168.1.5/32`)**:
   - First Host & Last Host: `192.168.1.5`
   - Broadcast: `None`
   - Usable Hosts: `1`
5. **Validasi Input Tidak Valid** (menghasilkan exception `ValueError` pada fungsi dan HTTP 400 Bad Request dengan field `detail` pada API):
   - Oktet di luar rentang 0-255 (`256.1.1.1/24`)
   - Angka nol di depan / leading zero (`192.168.01.1/24`)
   - Format IP tidak lengkap (`192.168.1/24`)
   - Karakter non-numerik (`abc.168.1.1/24`)
   - Input kosong
   - Prefix di luar rentang 0-32 (`192.168.1.1/33` dan `192.168.1.1/-1`)
6. **Endpoint API**:
   - `GET /`: Status 200 dan menyajikan `index.html`.
   - `GET /api/subnet`: Status 200 untuk input valid, Status 400 untuk input invalid.

## Alur Kerja
`issue` -> `branch` -> `test dulu` -> `implementasi` -> `commit` -> `pull request` -> `CI` -> `merge`

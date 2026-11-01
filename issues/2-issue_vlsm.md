# [Feature] Kalkulator VLSM

## Deskripsi
Fitur alokasi VLSM (Variable Length Subnet Mask) berbasis web untuk pembelajaran jaringan (guru dan siswa SMK TKJ). Pengguna memberi satu blok jaringan induk (misalnya `192.168.1.0/24`) dan daftar kebutuhan host per segmen. Sistem mengurutkan kebutuhan dari terbesar, memilih ukuran blok (pangkat 2) terkecil yang cukup, lalu mengalokasikan blok secara berurutan mulai dari alamat network induk. Hasil disediakan melalui endpoint `POST /api/vlsm` dan ditampilkan pada tab "VLSM Allocator" di `index.html`.

## Tugas
- [ ] Menulis test VLSM di `test_main.py` lebih dulu (fase TDD merah), mencakup skenario berhasil, urutan hasil, ukuran blok, kapasitas pas, kapasitas berlebih, dan input tidak valid.
- [ ] Membuat kerangka `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]` dan endpoint `POST /api/vlsm` yang belum diimplementasikan.
- [ ] Mengimplementasikan validasi `network_cidr` (format valid, dan harus alamat network untuk prefix-nya) serta `kebutuhan_host` (list bilangan bulat, tidak kosong, setiap elemen >= 1).
- [ ] Mengimplementasikan alokasi: urutkan menurun, ukuran blok = pangkat 2 terkecil >= kebutuhan + 2 (minimal /30), alokasi berurutan dari alamat network induk, tolak bila tidak muat.
- [ ] Menghubungkan tab VLSM di `index.html` ke `POST /api/vlsm` (menampilkan tabel hasil dan pesan kesalahan dari field `detail`).
- [ ] Menjalankan verifikasi test hingga seluruh pengujian lulus (fase hijau) tanpa mengubah test agar lulus.

## Kriteria Penerimaan
Berdasarkan tabel test pada `SPEC.md`:
1. **VLSM Berhasil** (`192.168.1.0/24`, kebutuhan `[100, 50, 20, 2]`):
   - Subnet 1: `/25` (`192.168.1.0`)
   - Subnet 2: `/26` (`192.168.1.128`)
   - Subnet 3: `/27` (`192.168.1.192`)
   - Subnet 4: `/30` (`192.168.1.224`)
   - Setiap hasil memuat `kebutuhan`, `network_cidr`, dan seluruh key dari `hitung_subnet`.
2. **VLSM Kapasitas Berlebih** (`192.168.1.0/24`, kebutuhan `[200, 100]`): ditolak (`ValueError` pada fungsi, HTTP 400 dengan field `detail` pada API).
3. **Validasi Input Tidak Valid** (`ValueError` / HTTP 400):
   - `network_cidr` bukan format yang valid, atau bukan alamat network untuk prefix-nya.
   - Daftar kebutuhan kosong, atau berisi nilai < 1.
4. **Endpoint API**: `POST /api/vlsm` dengan body JSON `{"network": str, "kebutuhan_host": list[int]}` mengembalikan JSON list hasil dengan status 200 untuk input valid.

## Alur Kerja
`issue` -> `branch` -> `test dulu` -> `implementasi` -> `commit` -> `pull request` -> `CI` -> `merge`

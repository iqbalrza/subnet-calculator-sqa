import pytest
from fastapi.testclient import TestClient

from main import app, hitung_subnet

client = TestClient(app)


@pytest.mark.parametrize(
    "ip,prefix,expected",
    [
        (
            "172.16.5.130",
            25,
            {
                "mask": "255.255.255.128",
                "network": "172.16.5.128",
                "broadcast": "172.16.5.255",
                "first_host": "172.16.5.129",
                "last_host": "172.16.5.254",
                "usable_hosts": 126,
            },
        ),
        (
            "10.0.0.0",
            30,
            {
                "mask": "255.255.255.252",
                "network": "10.0.0.0",
                "broadcast": "10.0.0.3",
                "first_host": "10.0.0.1",
                "last_host": "10.0.0.2",
                "usable_hosts": 2,
            },
        ),
    ],
)
def test_hitung_subnet_normal(ip, prefix, expected):
    result = hitung_subnet(ip, prefix)
    assert result == expected


@pytest.mark.parametrize(
    "ip,prefix,expected",
    [
        (
            "192.168.1.0",
            31,
            {
                "mask": "255.255.255.254",
                "network": "192.168.1.0",
                "broadcast": None,
                "first_host": "192.168.1.0",
                "last_host": "192.168.1.1",
                "usable_hosts": 2,
            },
        ),
        (
            "192.168.1.5",
            32,
            {
                "mask": "255.255.255.255",
                "network": "192.168.1.5",
                "broadcast": None,
                "first_host": "192.168.1.5",
                "last_host": "192.168.1.5",
                "usable_hosts": 1,
            },
        ),
    ],
)
def test_hitung_subnet_edge_cases(ip, prefix, expected):
    result = hitung_subnet(ip, prefix)
    assert result == expected


@pytest.mark.parametrize(
    "ip,prefix",
    [
        ("256.1.1.1", 24),
        ("192.168.01.1", 24),
        ("192.168.1", 24),
        ("abc.168.1.1", 24),
        ("", 24),
        ("192.168.1.1", 33),
        ("192.168.1.1", -1),
        ("192.168. 1.1", 24),
        ("192.168.1.1.1", 24),
    ],
)
def test_hitung_subnet_invalid(ip, prefix):
    with pytest.raises(ValueError):
        hitung_subnet(ip, prefix)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()


def test_api_subnet_success():
    response = client.get("/api/subnet", params={"ip": "172.16.5.130", "prefix": 25})
    assert response.status_code == 200
    data = response.json()
    assert data["network"] == "172.16.5.128"
    assert data["broadcast"] == "172.16.5.255"
    assert data["first_host"] == "172.16.5.129"
    assert data["last_host"] == "172.16.5.254"
    assert data["usable_hosts"] == 126
    assert data["mask"] == "255.255.255.128"

    # RFC 3021 /31 point-to-point via API
    response_31 = client.get("/api/subnet", params={"ip": "192.168.1.0", "prefix": 31})
    assert response_31.status_code == 200
    data_31 = response_31.json()
    assert data_31["network"] == "192.168.1.0"
    assert data_31["broadcast"] is None
    assert data_31["first_host"] == "192.168.1.0"
    assert data_31["last_host"] == "192.168.1.1"
    assert data_31["usable_hosts"] == 2


@pytest.mark.parametrize(
    "ip,prefix",
    [
        ("256.1.1.1", 24),
        ("192.168.01.1", 24),
        ("192.168.1.1", 33),
        ("192.168.1.1", -1),
        ("", 24),
    ],
)
def test_api_subnet_invalid(ip, prefix):
    response = client.get("/api/subnet", params={"ip": ip, "prefix": prefix})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data



# ======================= VLSM (Tahap 8) =======================

from main import alokasi_vlsm  # noqa: E402

# Tabel VLSM di SPEC.md: 192.168.1.0/24 untuk 100, 50, 20, 2 host.
VLSM_BERHASIL = [
    {
        "kebutuhan": 100,
        "network_cidr": "192.168.1.0/25",
        "mask": "255.255.255.128",
        "network": "192.168.1.0",
        "broadcast": "192.168.1.127",
        "first_host": "192.168.1.1",
        "last_host": "192.168.1.126",
        "usable_hosts": 126,
    },
    {
        "kebutuhan": 50,
        "network_cidr": "192.168.1.128/26",
        "mask": "255.255.255.192",
        "network": "192.168.1.128",
        "broadcast": "192.168.1.191",
        "first_host": "192.168.1.129",
        "last_host": "192.168.1.190",
        "usable_hosts": 62,
    },
    {
        "kebutuhan": 20,
        "network_cidr": "192.168.1.192/27",
        "mask": "255.255.255.224",
        "network": "192.168.1.192",
        "broadcast": "192.168.1.223",
        "first_host": "192.168.1.193",
        "last_host": "192.168.1.222",
        "usable_hosts": 30,
    },
    {
        "kebutuhan": 2,
        "network_cidr": "192.168.1.224/30",
        "mask": "255.255.255.252",
        "network": "192.168.1.224",
        "broadcast": "192.168.1.227",
        "first_host": "192.168.1.225",
        "last_host": "192.168.1.226",
        "usable_hosts": 2,
    },
]


def test_alokasi_vlsm_berhasil():
    assert alokasi_vlsm("192.168.1.0/24", [100, 50, 20, 2]) == VLSM_BERHASIL


def test_alokasi_vlsm_mengurutkan_dari_terbesar():
    # Urutan input diacak; hasil harus tetap dari kebutuhan terbesar.
    assert alokasi_vlsm("192.168.1.0/24", [2, 100, 20, 50]) == VLSM_BERHASIL


@pytest.mark.parametrize(
    "kebutuhan,prefix_blok",
    [
        (1, 30),    # 1 + 2 = 3  -> blok 4  (minimal /30)
        (2, 30),    # 2 + 2 = 4  -> blok 4
        (3, 29),    # 3 + 2 = 5  -> blok 8
        (6, 29),    # 6 + 2 = 8  -> blok 8
        (7, 28),    # 7 + 2 = 9  -> blok 16
        (126, 25),  # 126 + 2 = 128 -> blok 128
        (127, 24),  # 127 + 2 = 129 -> blok 256
    ],
)
def test_alokasi_vlsm_ukuran_blok(kebutuhan, prefix_blok):
    hasil = alokasi_vlsm("10.0.0.0/24", [kebutuhan])
    assert len(hasil) == 1
    assert hasil[0]["kebutuhan"] == kebutuhan
    assert hasil[0]["network_cidr"] == f"10.0.0.0/{prefix_blok}"


def test_alokasi_vlsm_kapasitas_pas():
    # Dua blok /25 mengisi /24 tepat penuh.
    hasil = alokasi_vlsm("192.168.1.0/24", [126, 126])
    assert [b["network_cidr"] for b in hasil] == ["192.168.1.0/25", "192.168.1.128/25"]


def test_alokasi_vlsm_jaringan_induk_bukan_awal_oktet():
    hasil = alokasi_vlsm("10.1.2.64/26", [30, 10])
    assert [b["network_cidr"] for b in hasil] == ["10.1.2.64/27", "10.1.2.96/28"]


@pytest.mark.parametrize(
    "network,kebutuhan",
    [
        ("192.168.1.0/24", [200, 100]),       # SPEC: kapasitas berlebih
        ("192.168.1.0/24", [126, 126, 1]),    # selisih satu blok /30
        ("192.168.1.0/30", [2, 2]),           # induk hanya muat satu blok
        ("192.168.1.0/30", [3]),              # blok /29 lebih besar dari induk
        ("192.168.1.0/32", [1]),              # induk /32 tidak bisa dibagi
        ("192.168.1.0/24", [2**40]),          # kebutuhan sangat besar
    ],
)
def test_alokasi_vlsm_tidak_muat(network, kebutuhan):
    with pytest.raises(ValueError):
        alokasi_vlsm(network, kebutuhan)


@pytest.mark.parametrize(
    "network",
    [
        "192.168.1.5/24",     # bukan alamat network untuk /24
        "192.168.1.0",        # tanpa prefix
        "192.168.1.0/",       # prefix kosong
        "192.168.1.0/33",     # prefix > 32
        "192.168.1.0/-1",     # prefix negatif
        "192.168.1.0/abc",    # prefix bukan angka
        "192.168.1.0/ 24",    # spasi
        "192.168.1.0/24/8",   # dua garis miring
        "256.1.1.0/24",       # oktet > 255
        "192.168.01.0/24",    # nol di depan
        "",                   # kosong
    ],
)
def test_alokasi_vlsm_network_tidak_valid(network):
    with pytest.raises(ValueError):
        alokasi_vlsm(network, [10])


@pytest.mark.parametrize(
    "kebutuhan",
    [[], [0], [-5], [10, 0], [True], [1.5], ["10"]],
)
def test_alokasi_vlsm_kebutuhan_tidak_valid(kebutuhan):
    with pytest.raises(ValueError):
        alokasi_vlsm("192.168.1.0/24", kebutuhan)


def test_api_vlsm_berhasil():
    response = client.post(
        "/api/vlsm",
        json={"network": "192.168.1.0/24", "kebutuhan_host": [100, 50, 20, 2]},
    )
    assert response.status_code == 200
    assert response.json() == VLSM_BERHASIL


@pytest.mark.parametrize(
    "body",
    [
        {"network": "192.168.1.0/24", "kebutuhan_host": [200, 100]},   # tidak muat
        {"network": "192.168.1.5/24", "kebutuhan_host": [10]},          # bukan network address
        {"network": "192.168.1.0/24", "kebutuhan_host": []},            # kosong
        {"network": "192.168.1.0/24", "kebutuhan_host": [0]},           # nilai < 1
        {"network": "192.168.1.0/24", "kebutuhan_host": "abc"},         # bukan list
        {"network": "192.168.1.0/24", "kebutuhan_host": [1.5]},         # bukan bilangan bulat
        {"network": "192.168.1.0/24"},                                  # field hilang
    ],
)
def test_api_vlsm_invalid(body):
    response = client.post("/api/vlsm", json=body)
    assert response.status_code == 400
    data = response.json()
    assert isinstance(data["detail"], str)
    assert data["detail"]

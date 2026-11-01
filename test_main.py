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


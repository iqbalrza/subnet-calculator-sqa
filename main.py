import re
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, StrictInt

app = FastAPI()

BASE_DIR = Path(__file__).parent

# Satu oktet: 0 atau angka 1-9 diikuti digit lain (tanpa nol di depan), hanya ASCII.
_OKTET = r"(?:0|[1-9][0-9]{0,2})"
_POLA_IPV4 = re.compile(rf"{_OKTET}(?:\.{_OKTET}){{3}}")


def _ip_ke_int(ip: str) -> int:
    """Validasi ketat string IPv4 lalu ubah menjadi bilangan 32-bit."""
    if not isinstance(ip, str) or not _POLA_IPV4.fullmatch(ip):
        raise ValueError(
            "Format IPv4 tidak valid: harus 4 oktet angka dipisah titik, "
            "tanpa spasi dan tanpa angka nol di depan (contoh: 192.168.1.1)."
        )
    hasil = 0
    for oktet in ip.split("."):
        nilai = int(oktet)
        if nilai > 255:
            raise ValueError(f"Oktet '{oktet}' di luar rentang 0-255.")
        hasil = (hasil << 8) | nilai
    return hasil


def _int_ke_ip(nilai: int) -> str:
    """Ubah bilangan 32-bit kembali menjadi string dotted-decimal."""
    return ".".join(str((nilai >> geser) & 0xFF) for geser in (24, 16, 8, 0))


def hitung_subnet(ip: str, prefix: int) -> dict:
    ip_int = _ip_ke_int(ip)
    if isinstance(prefix, bool) or not isinstance(prefix, int) or not 0 <= prefix <= 32:
        raise ValueError("Prefix harus bilangan bulat antara 0 sampai 32.")

    # Subnet mask: `prefix` bit 1 dari kiri, sisanya bit 0.
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    # Network address = IP AND subnet mask.
    network = ip_int & mask
    # Broadcast = network dengan seluruh bit host diubah menjadi 1.
    broadcast = network | (~mask & 0xFFFFFFFF)

    if prefix == 32:
        # Host tunggal: tidak ada broadcast.
        first_host = last_host = ip_int
        broadcast_str = None
        usable_hosts = 1
    elif prefix == 31:
        # Point-to-point (RFC 3021): kedua alamat dipakai sebagai host.
        first_host, last_host = network, network + 1
        broadcast_str = None
        usable_hosts = 2
    else:
        first_host, last_host = network + 1, broadcast - 1
        broadcast_str = _int_ke_ip(broadcast)
        usable_hosts = 2 ** (32 - prefix) - 2

    return {
        "mask": _int_ke_ip(mask),
        "network": _int_ke_ip(network),
        "broadcast": broadcast_str,
        "first_host": _int_ke_ip(first_host),
        "last_host": _int_ke_ip(last_host),
        "usable_hosts": usable_hosts,
    }


@app.exception_handler(RequestValidationError)
async def validasi_request(request: Request, exc: RequestValidationError):
    # Input yang salah tipe/kurang (mis. prefix=abc) juga dibalas 400 berformat {"detail": ...}.
    pesan = "; ".join(
        f"{'.'.join(str(p) for p in e['loc'][1:])}: {e['msg']}" for e in exc.errors()
    )
    return JSONResponse(status_code=400, content={"detail": pesan})


@app.get("/")
def halaman_utama():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/api/subnet")
def api_subnet(ip: str, prefix: int):
    try:
        return hitung_subnet(ip, prefix)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})


def alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]:
    raise NotImplementedError


class PermintaanVlsm(BaseModel):
    network: str
    kebutuhan_host: list[StrictInt]


@app.post("/api/vlsm")
def api_vlsm(permintaan: PermintaanVlsm):
    raise NotImplementedError

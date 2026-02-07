import requests
import json

# =========================
# SESSION
# =========================
s = requests.Session()

BASE_URL = "http://apotik.test:8080"

# =========================
# LOGIN
# =========================
login_res = s.post(f"{BASE_URL}/api/login", json={
    "username": "admin",      # sesuaikan
    "password": "admin123"    # sesuaikan
})

print("Login:", login_res.status_code, login_res.text)

if login_res.status_code != 200:
    raise Exception("Login gagal")

# =========================
# DATA PEMBELIAN
# =========================
pembelian = {
    "no_faktur": "",                # kosong → auto
    "tgl": "2026-01-13",
    "supplier_kode": "SP251225213115",      # WAJIB valid
    "pajak": 10000,
    "bayar": 0,
    "items": [
        {
            "obat_kode": "OB6524C9",  # WAJIB valid
            "batch_no": "BATCH001",
            "expired_date": "2027-01-13",
            "qty": 10,
            "harga_beli": 1500,    # HARGA SATUAN
            "cold_chain": False,
            "suhu_min": None,
            "suhu_max": None
        },
        {
            "obat_kode": "OB2B9541",
            "batch_no": "BATCH002",
            "expired_date": "2027-06-01",
            "qty": 5,
            "harga_beli": 2500,
            "cold_chain": True,
            "suhu_min": 2.0,
            "suhu_max": 8.0
        }
    ]
}

# =========================
# KIRIM PEMBELIAN
# =========================
r = s.post(
    f"{BASE_URL}/api/pembelian",
    json=pembelian
)

print("Pembelian:", r.status_code)

try:
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))
except Exception:
    print(r.text)

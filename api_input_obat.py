import requests
import pandas as pd

# =============================
# KONFIGURASI
# =============================
BASE_URL = "https://apotek.berkahsejahtera.com"
LOGIN_URL = f"{BASE_URL}/api/login"
OBAT_URL  = f"{BASE_URL}/api/obat"

USERNAME = "Ana"       # ganti sesuai user
PASSWORD = "AnaCantik14"    # ganti sesuai password

EXCEL_FILE = "daftar.xlsx"

# =============================
# SESSION LOGIN
# =============================
session = requests.Session()

login_payload = {
    "username": USERNAME,
    "password": PASSWORD
}

r = session.post(LOGIN_URL, json=login_payload)
if r.status_code != 200:
    print("❌ Login gagal:", r.text)
    exit()

print("✅ Login berhasil")

# =============================
# BACA EXCEL
# =============================
df = pd.read_excel(EXCEL_FILE)

print(f"📄 Total data: {len(df)} item")

# =============================
# KIRIM DATA PER BARIS
# =============================
for i, row in df.iterrows():
    payload = {
        "nama": str(row["nama"]).strip(),
        "produsen": str(row["produsen"]).strip(),
        "harga": int(row["harga"]),
        "stok": int(row["stok"]),
        "expired_date": row["expired_date"].strftime("%Y-%m-%d"),
        "golongan": str(row["golongan"]).strip()
    }

    res = session.post(OBAT_URL, json=payload)

    if res.status_code in (200, 201):
        print(f"✅ [{i+1}] Berhasil:", payload["nama"])
    else:
        print(f"❌ [{i+1}] Gagal:", payload["nama"])
        print("   Status:", res.status_code)
        print("   Response:", res.text)

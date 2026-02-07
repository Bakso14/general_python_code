
import requests

s = requests.Session()

# login
login_res = s.post("http://apotik.test:8080/api/login", json={
    "username": "admin",      # sesuaikan
    "password": "admin123"   # sesuaikan
})

print(login_res.status_code, login_res.text)

# kirim data setelah login
r = s.post("http://apotik.test:8080/api/obat", json={
    "nama": "Tes login Python",
    "produsen": "Depan",
    "harga": 12000,
    "stok": 7,
    "expired_date": "2026-12-12",
    "golongan": "NONE"
})

print(r.status_code, r.text)
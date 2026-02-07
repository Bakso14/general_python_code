import requests

s = requests.Session()  # PENTING

login_url = "http://apotik.test:8080/api/login"

login_payload = {
    "username": "admin",      # sesuaikan
    "password": "admin123"   # sesuaikan
}

r = s.post(login_url, json=login_payload)

print("Login status:", r.status_code)
print("Login response:", r.text)
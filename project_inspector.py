import requests
import json

PROJECT_ID = "Mh2Oa6l1"

URL = (
    f"https://summerofcode.withgoogle.com/"
    f"api/projects/{PROJECT_ID}/"
    f"?role=&program_slug=2026"
)

print("Requesting:")
print(URL)

response = requests.get(URL, timeout=30)

print("\nSTATUS:")
print(response.status_code)

print("\nCONTENT TYPE:")
print(response.headers.get("content-type"))

data = response.json()

print("\nDATA TYPE:")
print(type(data))

print("\nJSON:")
print(
    json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )
)
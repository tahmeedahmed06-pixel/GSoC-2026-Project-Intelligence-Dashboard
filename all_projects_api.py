import requests
import json

URL = (
    "https://summerofcode.withgoogle.com/"
    "api/projects/?program_slug=2026"
)

print("Requesting GSoC project API...")

response = requests.get(URL, timeout=30)
response.raise_for_status()

data = response.json()

projects = data["entities"]["projects"]

print(f"Projects received: {len(projects)}")

with open(
    "gsoc_projects.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        projects,
        file,
        indent=2,
        ensure_ascii=False
    )

print("Saved to: gsoc_projects.json")
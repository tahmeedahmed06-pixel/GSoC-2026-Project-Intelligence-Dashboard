import json

from playwright.sync_api import sync_playwright


API_URL = "https://summerofcode.withgoogle.com/api/program/2026/organizations/"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("Requesting organization API...")

    response = page.request.get(API_URL)

    print("Status:", response.status)

    data = response.json()

    print("Organizations found:", len(data))

    with open("organizations.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("Saved: organizations.json")

    browser.close()
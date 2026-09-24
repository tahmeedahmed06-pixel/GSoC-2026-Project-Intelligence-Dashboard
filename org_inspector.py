import json
from playwright.sync_api import sync_playwright


with open("organizations.json", "r", encoding="utf-8") as file:
    organizations = json.load(file)


organization = organizations[0]

name = organization["name"]
slug = organization["slug"]

URL = (
    "https://summerofcode.withgoogle.com"
    "/programs/2026/organizations/"
    + slug
)


print("Organization:", name)
print("URL:", URL)


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    response = page.goto(
        URL,
        wait_until="networkidle"
    )

    print("HTTP status:", response.status)

    # Find project-detail links
    project_links = page.locator(
        'a[href*="/programs/2026/projects/"]'
    )

    print("\nGSoC projects:", project_links.count())

    for i in range(project_links.count()):

        link = project_links.nth(i)

        text = link.inner_text().strip()

        href = link.get_attribute("href")

        print(f"{i + 1}. {text}")
        print(f"   {href}")

    browser.close()
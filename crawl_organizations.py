import json
import time

from playwright.sync_api import sync_playwright


INPUT_FILE = "organizations.json"
OUTPUT_FILE = "organization_projects.json"

BASE_URL = "https://summerofcode.withgoogle.com"


# --------------------------------------------------
# Load organizations
# --------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    organizations = json.load(file)


print(f"Organizations to crawl: {len(organizations)}")


results = []


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    for index, organization in enumerate(organizations, start=1):

        name = organization["name"]
        slug = organization["slug"]

        url = (
            f"{BASE_URL}/programs/2026/organizations/{slug}"
        )

        print(
            f"[{index}/{len(organizations)}] "
            f"{name}"
        )

        try:

            response = page.goto(
                url,
                wait_until="networkidle",
                timeout=30000
            )

            if response is None:
                print("  No response")
                continue

            project_links = page.locator(
                'a[href*="/programs/2026/projects/"]'
            )

            projects = []

            for i in range(project_links.count()):

                href = project_links.nth(i).get_attribute(
                    "href"
                )

                if href and href not in projects:
                    projects.append(href)

            result = {
                "name": name,
                "slug": slug,
                "url": url,
                "project_count": len(projects),
                "projects": projects
            }

            results.append(result)

            print(
                f"  Projects: {len(projects)}"
            )

        except Exception as error:

            print(
                f"  ERROR: {error}"
            )

        # Small delay between requests
        time.sleep(0.5)

    browser.close()


# --------------------------------------------------
# Save results
# --------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=4,
        ensure_ascii=False
    )


print("\nFinished.")
print(f"Organizations collected: {len(results)}")
print(f"Saved to: {OUTPUT_FILE}")
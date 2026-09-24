from playwright.sync_api import sync_playwright


URL = "https://summerofcode.withgoogle.com/programs/2026/organizations"


with sync_playwright() as p:

    print("Starting browser...")

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("Opening GSoC Organizations page...")

    page.goto(URL, wait_until="networkidle")

    print("Page loaded!")
    print("Page title:", page.title())

    page.screenshot(
        path="gsoc-page.png",
        full_page=True
    )

    with open("gsoc-page.html", "w", encoding="utf-8") as file:
        file.write(page.content())

    print("Saved screenshot: gsoc-page.png")
    print("Saved HTML: gsoc-page.html")

    browser.close()

    print("Browser closed.")
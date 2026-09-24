from playwright.sync_api import sync_playwright


URL = "https://summerofcode.withgoogle.com/programs/2026/organizations"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("Opening GSoC...")

    # Listen to every network response
    def handle_response(response):

        url = response.url

        if "api" in url.lower() or "organization" in url.lower():
            print("NETWORK:", response.status, url)

    page.on("response", handle_response)

    page.goto(URL, wait_until="networkidle")

    print("\nPage loaded.")
    print("Title:", page.title())

    page.wait_for_timeout(3000)

    print("\nFinished observing network requests.")

    browser.close()
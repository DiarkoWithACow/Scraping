from playwright.sync_api import sync_playwright
with sync_playwright() as p: 
    browser = p.chromium.launch(headless = True)
    context = browser.new_context(ignore_https_errors=True)
    page = browser.new_page()
    page.goto("https://scrapeme.live/shop/")
    print(page.title())
    browser.close()
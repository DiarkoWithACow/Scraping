from playwright.sync_api import sync_playwright
import pandas as pd
import time

def workua_scraping(driver):
    browser = driver.chromium.launch_persistent_context(
        user_data_dir=r"C:\playwright",
        channel="chrome",
        headless=False,
        no_viewport=True,
    )

    page = browser.new_page()
    jobs = []

    for page_count in range(1, 4):
        print(f"Scraping job list from page {page_count}...")
        page.goto(f"https://www.work.ua/jobs-data+scientist/?page={page_count}")
        page.wait_for_selector('.job-link')
        vacancies = page.locator('.job-link')
        total = vacancies.count()
        print(f"🔹 Found {total} vacancies on page {page_count}")

        for vacancy in vacancies.element_handles():
            item = {}

            link_tag = vacancy.query_selector("h2 a")
            if link_tag:
                item["Title"] = link_tag.get_attribute("title") or ""
                href = link_tag.get_attribute("href") or ""
                item["URL"] = "https://www.work.ua" + href
            else:
                continue

            salary_tag = vacancy.query_selector("div > span.strong-600")
            if salary_tag:
                salary_text = salary_tag.inner_text().replace("\u2009", "").replace("\xa0", " ").strip()
                salary_text = salary_text.replace("–", "-").replace(" - ", "-")
                item["Salary_info"] = salary_text
            else:
                item["Salary_info"] = ""

            company_tag = vacancy.query_selector(".mt-xs .strong-600")
            if company_tag:
                item["Company_Name"] = company_tag.inner_text().strip()
            else:
                item["Company_Name"] = ""

            location_tag = vacancy.query_selector(".mt-xs span:last-child")
            if location_tag:
                item["Location"] = location_tag.inner_text().strip()
            else:
                item["Location"] = ""

            print(f"  ✅ {item['Title']} | {item['Company_Name']} | {item['Salary_info']} | {item['Location']}")
            jobs.append(item)

        time.sleep(2)

    print(f"\nTotal jobs scraped: {len(jobs)}")
    browser.close()
    return jobs


with sync_playwright() as playwright:
    jobs = workua_scraping(playwright)

    if jobs:
        df = pd.DataFrame(jobs)
        df.to_excel("workua_jobs.xlsx", index=False)
        print("✅ Saved to workua_jobs.xlsx")
    else:
        print("⚠️ No jobs scraped — check your selectors or site structure.")

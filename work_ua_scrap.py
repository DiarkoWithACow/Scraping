from playwright.sync_api import sync_playwright
import pandas as pd
import time

def workua_scraping(driver):
    browser = driver.chromium.launch_persistent_context(
        user_data_dir = r"C:\playwright",
        channel = "chrome",
        headless = False,
        no_viewport = True,

    )

    page = browser.new_page()
    page_count = 0
    jobs = []
    for page_count in range(1, 4):
        print(f"Scraping job list from page {page_count}...")
        page.goto(f"https://www.work.ua/jobs-data+analyst/?page={page_count}")
        page.wait_for_selector('.card')

        vacancies = page.locator('.card')

        for vacancy in vacancies.element_handles():
            item = {}
            link_tag = vacancy.query_selector("h2 a")
            if link_tag:
                item["Title"] = link_tag.inner_text().strip()
                href = link_tag.get_attribute("href")  
                if href:
                    item["URL"] = "https://www.work.ua" + href
                else:
                    item["URL"] = ""
            else:
                item["Title"] = ""
                item["URL"] = ""

    all_items = []
    for i, job in enumerate(jobs, start=1):
        print(f"Scraping details page {i}/{len(jobs)}: {job['Title']}")
        page.goto(job['URL'])
        time.sleep(3)
        item = {}

        item["Title"] = job['Title']
        item["URL"] = job["URL"]
        item["Company_Name"] = ""
        item["Location"] = ""
        item["Salary_info"] = ""
        
        company_name = vacancy.query_selector(".strong-600")
        if company_name:
            item["CompanyName"] = company_name.inner_text().strip()
        else:
            item["CompanyName"] = ""

        company_location = vacancy.query_selector(".mt-xs span:last-child")
        if company_location:
            item["Location"] = company_location.inner_text().strip()
        else:
            item["Location"] = ""

        salaryinfo  = vacancy.query_selector("div > .strong-600")
        if salaryinfo:
            salary_text = salaryinfo.inner_text()
            salary_text = salary_text.replace("\u2009", "").replace("\xa0", " ").strip()
            salary_text = salary_text.replace("–", "-").replace(" - ", "-")
            item["Salary_info"] = salary_text
        else:
            item["Salary_info"] = ""

        all_items.append(item)
        
    browser.close()

    return all_items




with sync_playwright() as playwright:
    jobs = workua_scraping(playwright)

    df = pd.DataFrame(jobs)
    df.to_excel("workua_jobs.xlsx", index=False)
    print("✅ Saved to workua_jobs.xlsx")
from playwright.sync_api import sync_playwright
import pandas as pd
import time

def workua_scraping(driver):
    browser = driver.chromium.launch_persistent_context(
        user_data_dir = r"tmp",
        channel = "chrome",
        headless = False,
        no_viewport = True,
    )

    page = browser.new_page()
    page_count = 0
    jobs = []


    for page_count in range(1, 4):
        print(f"Scraping job list from page {page_count}...")
        page.goto(f"https://www.work.ua/jobs-data+scientist//?page={page_count}")
        
        page.wait_for_selector('.job-link')

        vacancies = page.locator('.job-link')
        total = vacancies.count()
        print(f"Found {total} vacancies on page {page_count}")

        for vacancy in vacancies.element_handles():
            item = {}

            link_tag = vacancy.query_selector("h2 a")
            if link_tag:
                item["Title"] = link_tag.get_attribute("title") or ""
                href = link_tag.get_attribute("href")  
                item["URL"] = "https://www.work.ua" + href
            else:
                 item ["URL"] = "no_link"
        
            company_name = vacancy.query_selector(".mt-xs span.strong-600")
            if company_name:
                item["Company_Name"] = company_name.inner_text().strip()
            else:
                item["Company_Name"] = "not_mentioned"

            item["Location"] = ""
            company_location = vacancy.query_selector(".mt-xs > span:not([class])")
            if company_location:
                loc_text = company_location.inner_text().strip().replace(",", "")
                item["Location"] = loc_text
            else:
                spans = vacancy.query_selector_all(".mt-xs span")
                loc_text = ""
                for s in spans:
                    cls = s.get_attribute("class") or ""
                    if cls.strip() == "":
                        loc_text = s.inner_text().strip().replace(",", "")
                item["Location"] = loc_text

            salaryinfo  = vacancy.query_selector(":scope > div > span.strong-600")
            if salaryinfo:
                salary_text = salaryinfo.inner_text().replace("\u2009", "").replace("\xa0", " ").strip()
                salary_text = salary_text.replace("–", "-").replace(" - ", "-")
                item["Salary_info"] = salary_text
            else:
                item["Salary_info"] = "not_mentioned"
        
            print(f"  ✅ {item['Title']} | {item['URL']} | {item['Company_Name']} | {item['Location']} | {item['Salary_info']}")
            jobs.append(item)
        
        time.sleep(3)

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
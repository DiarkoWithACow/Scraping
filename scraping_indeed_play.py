from playwright.sync_api import sync_playwright
import pandas as pd
import time

def indeed_scraping(driver):
    browser = driver.chromium.launch_persistent_context(
        user_data_dir = r"C:\playwright",
        channel = "chrome",
        headless = False,
        no_viewport = True,

    )

    page = browser.new_page()
    page_count = 0
    jobs = []
    while page_count <2:
        print(f"Scraping job list from page number {page_count + 1}...")
        time.sleep(3)
        page.goto('https://www.indeed.com/jobs?q=data+analyst&start='+str(page_count * 10))
        vacancies = page.locator('.cardOutline')


        for vacancy in vacancies.element_handles():
            item = {}
            item ['Title'] = vacancy.query_selector("h2").inner_text()
            item ['URL'] = "https://www.indeed.com"+vacancy.query_selector("a").get_attribute("href")
            jobs.append(item)
        page_count +=1

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
        
        company_name = page.get_by_test_id("inlineHeader-companyName")
        if company_name.count()>0:
            item["Company_Name"] = company_name.inner_text()

        company_location = page.get_by_test_id("inlineHeader-companyLocation")
        if company_location.count() > 0:
            item["Location"] = company_location.inner_text()

        salaryinfo = page.get_by_test_id("jobsearch-OtherJobDetailsContainer")
        if(salaryinfo.count() > 0):
            item["Salary_info"] = salaryinfo.inner_text()

        all_items.append(item)
        
    browser.close()

    return all_items



with sync_playwright() as playwright:
    jobs = indeed_scraping(playwright)

    df = pd.DataFrame(jobs)
    df.to_excel("jobs.xlsx", index = False)
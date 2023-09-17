
#! https://kr.indeed.com 에서 python과 관련된 일들을 검색해서 엑셀파일로 정리할 것
#! Beautifulsoup : 웹사이트의 데이터(HTML, XML)를 받아올 수 있게 해줌
from requests import get
from bs4 import BeautifulSoup
from wwr import extract_jobs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_page_count(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)

    base_url = "https://kr.indeed.com/jobs?q="
    search_term = keyword
    browser.get(f"{base_url}{search_term}")

    response = browser.page_source
    soup = BeautifulSoup(response, "html.parser")
    pagination = soup.find("nav", class_="ecydgvn0")
    pages = pagination.find_all("div", recursive=False)
    count = len(pages)
    if count == 0:
        return 1
    elif count >= 5:
        return 5
    else :
        return count

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    for page in range(pages):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        browser = webdriver.Chrome(options=options)

        base_url = "https://kr.indeed.com/jobs?q="
        search_term = keyword
        browser.get(f"{base_url}{search_term}")

        response = browser.page_source

        soup = BeautifulSoup(response)
        job_list = soup.find("ul", class_="css-zu9cdh")
        jobs = job_list.find_all("li", recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    'link': f"https://kr.indeed.com{link}",
                    'company': company.string,
                    'location': location.string,
                    'position': title,
                }
                print(job_data)
                print("////////////////")


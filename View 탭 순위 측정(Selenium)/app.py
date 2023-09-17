import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

search_keywords = ["파이썬 Selenium", "python flask"]
target_blog_links = ["https://blog.naver.com/allop24/223055754557",
                     "https://blog.naver.com/lread90"]

for search_keyword, target_blog_link in zip(search_keywords, target_blog_links):
    search_link = f"https://search.naver.com/search.naver?where=view&sm=top_hty&fbm=0&ie=utf8&query={search_keyword}"
    driver.get(search_link)
    time.sleep(2)

    link_selector = f'a[href="{target_blog_link}"]'

    current_rank = -1
    BLOG_FOUND = False
    for _ in range(7):  # * 최대 7번 하위 랭크 블로그 글을 불러오겠음
        try:
            element = driver.find_element(By.CSS_SELECTOR, link_selector)
            print(element.text)
            while True:
                #** element.find_element(By.XPATH, "./..") : 나 바로 위에 있는 태그 전달해줘
                new_element = element.find_element(By.XPATH, "./..")
                current_rank = new_element.get_attribute("data-cr-rank")
                if current_rank != None:
                    print("현재랭크 찾음 : ", current_rank)
                    BLOG_FOUND = True
                    break
                element = new_element
                print("못찾음")
            if BLOG_FOUND:          #* 찾았으면 스크롤 멈춰줌
                break
        except:
            print("타겟 블로그를 못 찾음 -> 스크롤하겠습니다.")
            driver.execute_script("window.scrollBy(0,10000);")
            time.sleep(3)                                           #* 새로운 데이터 로딩하는데 시간 기다려줌
    print(f"{search_keyword} / {current_rank} : 타겟 블로그의 랭크를 찾았습니다.")

input()
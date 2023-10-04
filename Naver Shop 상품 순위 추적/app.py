import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

# 1. URL로 1페이지 방문
page_index = 1
search_keyword = "꿀사과"
shopping_link = f"https://msearch.shopping.naver.com/search/all?query={search_keyword}&frm=NVSHSRC&vertical=search"
driver.get(shopping_link)
# 2. 페이지를 4-5번 밑으로 내리기 (상품 더 불러오기)

# 3. 타겟 상품이 페이지에 노출되고 있는지 확인하기
# 4. 없다면? -> URL로 Next Page 방문

input()
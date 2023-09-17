import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller


chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
#* 1. Navigation 관련 툴

#* 1-1. get() - 원하는 페이지로 이동하는 함수
driver.get("https://google.com")
time.sleep(1)
driver.get("https://www.naver.com")
#* 1-2. back() - 뒤로가기
driver.back()
time.sleep(1)
#* 1-3. forward() - 앞으로가기
driver.forward()
time.sleep(1)
#* 1-4. refresh() - 새로고침
driver.refresh()
time.sleep(1)

#* 2. browser information
#* 2-1. title : 웹 사이트의 타이틀을 가지고 옴
title = driver.title
print(title, "타이틀")

#* 2-2. current_url : 주소차을 그대로 가지고 옴
url = driver.current_url
print(url, "현재 url")

#* 3. Driver Wait < time보다 효율적
# command (selector에 해당하는 태그가 나올 때까지 최대 30초 기다려라, 넘어가면 에러 터짐)
try:    
    selector = "#shortcutArea > ul"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        By.CSS_SELECTOR, selector
    ))
except Exception as e:
    print("30초가 지났지만 태그 찾지 못했음")

print("동작 끝")

input()
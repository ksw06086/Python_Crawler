from classes.scrollCrawler import ScrollCrawler
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NaverPost(ScrollCrawler):
    def scrolling(self, distance='end'):
        super().scrolling(distance)
        if distance=='end':
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="더보기"]'))).send_keys(Keys.ENTER)

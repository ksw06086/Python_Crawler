from classes.scrollCrawler import ScrollCrawler
from time import sleep
from random import randrange
from datetime import timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Twitter(ScrollCrawler):
    def __init__(self, osp, platform, selector_dic, search_url, post_selector, data, date_format_string=None,
                 add_domain=None, max_post=50):
        super().__init__(osp, platform, selector_dic, search_url, post_selector, data, date_format_string, add_domain)
        self.max_post = max_post

    # 로그인 되어 있는지 확인
    def login_check(self):
        self.driver.get('https://twitter.com/home')
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: 'login' in driver.current_url)
            return False
        except:
            return True

    def login(self):
        while True:
            try:
                if self.login_check():
                    break
                self.send_and_click(['//input[@autocomplete="username"]', 'pibesay232@aramask.com'], '//span[text()="다음"]')
                try:
                    self.send_and_click(['//input[@name="text"]', 'board_man_'], '//span[text()="다음"]')
                except:
                    pass
                self.send_and_click(['//input[@name="password"]', 'forcrawling'], '//span[text()="로그인하기"]')
                WebDriverWait(self.driver, 10).until(lambda driver: driver.current_url == "https://twitter.com/home")
                break
            except:
                slack_send('Twitter 로그인 함수 에러로 무한 루프를 빠져나가지 못합니다')
                pass

    def send_and_click(self, input, button):
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH, input[0]))).send_keys(input[1])
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, button))).click()
        sleep(randrange(2, 6))

    def parsing_data(self):
        super().parsing_data()
        self.data.write_date = self.data.write_date + timedelta(hours=9)
        self.data.writer = self.data.writer.replace('/', '')

    def search(self):
        super().search()
        for i in range(0, 11):
            self.scrolling('end')
            sleep(randrange(1, 5))
            self.driver.find_element(By.CSS_SELECTOR, 'a[role="tab"][aria-selected="true"]').click()
            sleep(randrange(1, 5))

    def get_post_list(self):
        post_list = set()
        self.search()
        while len(post_list) < self.max_post:
            sleep(1)
            self.set_soup(self.driver.page_source)
            [post_list.add(ele) for ele in self.crawl_data(self.post_selector)]
            self.scrolling(500)
        return post_list

    def start_crawling(self):
        self.login()
        super().start_crawling()

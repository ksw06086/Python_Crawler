import string
from random import choice, randrange
from time import sleep

from classes.scrollCrawler import ScrollCrawler
from datetime import datetime


class Tiktok(ScrollCrawler):
    def __init__(self, osp, platform, selector_dic, search_url, post_selector, data, date_format_string=None,
                 add_domain=None):
        super().__init__(osp, platform, selector_dic, search_url, post_selector, data, date_format_string, add_domain)

    def format_date(self):
        if self.data.write_date.find("-") == 1:
            self.data.write_date = f"{datetime.today().year}-{self.data.write_date}"
        super().format_date()

    def check_captcha(self):
        captcha = True
        while captcha:
            random_title = ''.join(choice(string.ascii_letters) for _ in range(randrange(5,12)))
            link = f'https://www.tiktok.com/search?q={random_title}'
            self.driver.get(link)
            sleep(randrange(3, 7))
            self.set_soup(self.driver.page_source)
            check = self.soup.select_one('div.tiktok-1soki6-DivItemContainerForSearch')
            if check:
                captcha = False

    def start_crawling(self):
        self.check_captcha()
        super().start_crawling()

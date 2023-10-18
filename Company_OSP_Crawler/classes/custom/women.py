from classes.error.selenium_error import SeleniumError
from classes.pageCrawler import PageCrawler
from bs4 import BeautifulSoup
from random import randrange
from time import sleep


class Women(PageCrawler):
    def add_domain_in_url(self, url):
        post_id = url.split('fldid=')[1].split('&')[0]
        data_num = url.split('datanum=')[1].split('&')[0]
        return f'https://cafe.daum.net/subdued20club/{post_id}/{data_num}'
    
    def get_data(self):
        if self.data.url == 'limitted_post':
            return
        super().get_data()

    def content_insert(self):
        if self.data.url == 'limitted_post':
            return
        super().content_insert()

    def load_detail_page(self, url):
        url = self.add_domain_in_url(url)
        self.selenium_bs(url)
        self.data.url = 'limitted_post' if self.soup.select('span.btn_txt.bt02.w08.b') else url

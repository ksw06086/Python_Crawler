from classes.error.selenium_error import SeleniumError
from classes.pageCrawler import PageCrawler
from bs4 import BeautifulSoup
from random import randrange
from time import sleep
import urllib.parse


class Remonterrace(PageCrawler):
    def parsing_search_url(self):
        self.search_url = self.search_url.replace('{Keyword}', urllib.parse.quote(self.data.keyword.encode('euc-kr')))
    
    def add_domain_in_url(self, url):
        post_id = url.split('clubid=')[1].split('&')[0]
        data_num = url.split('articleid=')[1].split('&')[0]
        return f'https://cafe.naver.com/remonterrace/ca-fe/ArticleRead.nhn?clubid={post_id}&articleid={data_num}'
    
from classes.pageCrawler import PageCrawler


class NaverNews(PageCrawler):
    def set_page(self, page):
        self.search_url = self.search_url.replace('{Page}', str((page*10)+1))

    def format_date(self):
        self.data.write_date = self.data.write_date.replace('오후', 'PM').replace('오전', 'AM')
        super().format_date()
    
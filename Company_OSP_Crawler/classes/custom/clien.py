from classes.pageCrawler import PageCrawler


class Clien(PageCrawler):
    def format_date(self):
        if '수정일' in self.data.write_date:
            self.data.write_date = self.data.write_date.split('수정일 : ')[1]
        super().format_date()
            
    def set_page(self, page):
        self.search_url = self.search_url.replace('{Page}', str(page - 1))
    
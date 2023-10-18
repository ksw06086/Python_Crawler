from classes.pageCrawler import PageCrawler


class NaverKin(PageCrawler):
    def set_page(self, page):
        self.search_url = self.search_url.replace('{Page}', str((page*10)+1))
    
from classes.pageCrawler import PageCrawler


class Instiz(PageCrawler):
    def add_domain_in_url(self, url):
        return url.replace('..', self.add_domain)

    def content_insert(self):
        if '죄송합니다, 회원에게만 공개된 글입니다' in self.data.contents:
            return
        super().content_insert()
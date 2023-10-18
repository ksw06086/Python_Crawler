from classes.pageCrawler import PageCrawler


class Ppomppu(PageCrawler):
    def format_date(self):
        if '등록일:' in self.data.write_date:
            self.data.write_date = self.data.write_date.split('등록일: ')[1].split('조회수')[0]
        super().format_date()
        
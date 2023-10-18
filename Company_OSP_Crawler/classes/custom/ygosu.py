from classes.pageCrawler import PageCrawler


class Ygosu(PageCrawler):
    def format_date(self):
        self.data.write_date = self.data.write_date.split(' / ')[0].split(' : ')[1]
        super().format_date()
        
    def parsing_data(self):
        super().parsing_data()
        self.data.title = ' '.join(self.data.title.split()[1:-1])

            
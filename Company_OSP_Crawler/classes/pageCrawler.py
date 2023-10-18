from classes.crawler import Crawler

#* 특정 웹페이지를 크롤링(페이지 기반의 크롤링 로직을 추가적으로 구현)
class PageCrawler(Crawler):
    #* PageCrawler 클래스를 초기화
    def __init__(self, osp, platform, selector_dic, search_url, post_selector, data, date_format_string='%Y-%m-%d %H:%M:%S', add_domain='', max_page=3, iframe_id=None):
        super().__init__(osp, platform, selector_dic, search_url, post_selector, data, date_format_string, add_domain, iframe_id)
        # variable - max_page: 크롤링할 최대 페이지 수(default 3)
        self.max_page = max_page

    #* 검색 URL의 {Page} 부분을 입력받은 페이지 번호로 대체
    def set_page(self, page):
        self.search_url = self.search_url.replace('{Page}', str(page))

    #* 여러 페이지에 걸친 포스트 목록을 크롤링
    def get_post_list(self):
        # variable - result : 크롤링된 포스트 URL들을 저장할 집합 초기화
        result = set()
        # variable - search_url : 원래의 검색 URL을 저장합니다. 이는 각 페이지마다 {Page} 부분을 새로운 값으로 대체하기 위해 사용(원본 수정 X)
        search_url = self.search_url
        # 해석 : 1페이지부터 self.max_page까지 순회
        for page in range(1, self.max_page + 1):
            self.search_url = search_url
            # 해석 : 위에 set_page 함수, 페이지 번호 URL에 넣어주는 거
            self.set_page(page)
            # 해석 : 현재 페이지의 포스트 목록(URLs)을 가져옴
            urls = super().get_post_list()
            if not urls: break
            result.update(urls) # 해석 : 가져온 포스트 URL들을 result 집합에 추가
        return result 

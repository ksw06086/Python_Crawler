from time import sleep
from classes.crawler import Crawler
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#* 스크롤 페이지를 크롤링(스크롤을 통해 웹페이지를 이동하면서 데이터를 크롤링하는 로직을 추가적으로 구현)
class ScrollCrawler(Crawler):
    #* ScrollCrawler 클래스를 초기화
    def __init__(self, osp, platform, selector_dic, search_url, post_selector, data, date_format_string='%Y-%m-%d %H:%M:%S', add_domain='', iframe_id=None):
        super().__init__(osp, platform, selector_dic, search_url, post_selector, data, date_format_string, add_domain, iframe_id)

    #* 웹페이지를 스크롤하는 함수
    # variable - distance: 스크롤 방향과 거리를 결정
    # variable             기본값은 'end'로, 페이지의 맨 아래로 스크롤 / 'start'는 페이지의 맨 위로 스크롤 
    # variable             숫자를 전달하면 현재 위치에서 해당 숫자만큼 스크롤
    def scrolling(self, distance='end'):
        if distance=='end':
            # function(find_element) : 웹 드라이버를 사용하여 웹페이지의 body 요소를 찾음.
            # function(send_keys(Keys.END/HOME)): END 또는 HOME 키를 보내서 페이지를 맨 아래나 맨 위로 스크롤
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        elif distance=='start':
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
        else:
            # function(driver.execute_script()): 웹 드라이버를 사용하여 자바스크립트를 실행하여 웹페이지를 스크롤
            # event handler(window.pageYOffset): 웹페이지의 맨 위에서 현재 보이는 화면의 시작 지점까지의 거리(픽셀 단위)를 반환
            current = self.driver.execute_script('return window.pageYOffset;')
            # 해석 : 현재 스크롤된 거리에 사용자가 지정한 추가 스크롤 거리를 더함
            # variable - distance: scrolling 함수의 입력 인자
            distance = current + distance
            # 해석 :  웹페이지를 distance에 지정된 거리만큼 수직으로 스크롤
            # event handler(window.scrollTo(x-coord, y-coord)) : 웹페이지를 특정 좌표로 스크롤
            self.driver.execute_script(f'window.scrollTo(0, {distance});')
        sleep(1)

    #* 스크롤하면서 포스트 목록을 크롤링
    def get_post_list(self):
        # 해석 : 웹페이지 로딩
        self.search()
        # 해석 : 10번 스크롤하여 웹페이지의 맨 아래로 이동
        for i in range(0, 10):
            self.scrolling('end')
        # 해석 : 스크롤 후의 페이지 내용을 BeautifulSoup 객체로 변환
        self.set_soup(self.driver.page_source)
        # 해석 : 스크롤된 페이지에서 포스트 목록을 크롤링하고 반환
        return self.crawl_data(self.post_selector)
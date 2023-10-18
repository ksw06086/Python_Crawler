
# variable - datetime : 날짜와 시간을 처리하고 조작
# variable - timedelta : 두 날짜 또는 시간 간의 차이를 계산
# variable - randrange : 범위(시작, 중지, 단계)에서 무작위로 선택된 요소를 반환
# variable - sleep : 지정된 시간(초) 동안 프로그램을 일시 중지
# variable - sub : 패턴 발생을 지정된 문자열로 바꾸는 데 사용(문자열을 정리하거나 서식을 지정)
# variable - etree : XML 및 HTML 문서를 트리 구조로 읽고 쓰며, 쿼리하고 수정(BeautifulSoup과 비슷 Element를 생성하고 수정까지 할 수 있고, 새로운 문서 작성까지 가능)
# variable - deepcopy : 원본과 참조를 공유하지 않는 컬렉션(예: 목록 또는 사전)의 새 복사본을 만드는 데 사용
# variable - Chrome : 일부 웹사이트에서 봇이나 자동화된 스크립트를 차단하기 위해 사용하는 감지 메커니즘을 방지하도록 설계된 수정된 버전의 Selenium Chrome 드라이버
# variable - ChromeOptions : Chrome 브라우저가 시작되기 전에 다양한 옵션을 설정
# variable - Service : Selenium을 통해 Chrome 브라우저를 제어하는 ​​데 필요한 ChromeDriver 서버와 상호작용
# variable - InsertError, ParsingError, SeleniumError : 사용자 정의 예외 클래스입니다. 크롤러의 특정 오류 시나리오를 처리
# variable - mongo_client : MongoDB 데이터베이스와 상호 작용하는 인터페이스인 것 같습니다. 아마도 데이터베이스를 삽입, 업데이트 및 쿼리하는 기능을 제공
# variable - SELECTOR : 웹페이지에서 요소를 선택하는 방법(CSS 선택기 또는 XPath 사용)을 지정하는 상수를 나타내는 것

from datetime import datetime, timedelta
from random import randrange
from time import sleep
from re import sub
import requests
from lxml import etree
from copy import deepcopy
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from classes.error.insert_error import InsertError
from classes.error.parsing_error import ParsingError
from classes.error.selenium_error import SeleniumError
from db.mongo_service import mongo_client
from constant import SELECTOR


class Crawler:
    #* 검색 URL, 데이터 객체, 스크래핑을 위한 선택기 등 다양한 매개변수로 크롤러를 초기화
    def __init__(self, osp, platform, selector_dic, search_url, post_selector, data, date_format_string = '%Y-%m-%d %H:%M:%S', add_domain = '', iframe_id = None):
        #* 검색이나 데이터 수집을 시작할 웹사이트의 URL
        self.search_url = search_url
        #* 데이터를 저장하거나 관리하기 위한 객체
        self.data = data
        #* 스크레이핑 할 웹사이트
        self.data.osp = osp
        #* 데이터를 스크레이핑할 특정 플랫폼(분류하기 위한 값)
        self.data.platform = platform
        #* 게시물과 관련된 선택자
        self.post_selector = post_selector
        #* 웹 페이지에 내장된 iframe의 ID(웹 페이지 내에 다른 웹 페이지를 임베드하기 위해 사용)
        self.iframe_id = iframe_id
        #* selector_dic에서 전달받은 선택자들을 저장
        self.elements = {k: v for k, v in selector_dic.items()}
        #* 날짜 및 시간을 파싱하거나 출력하기 위한 형식 문자열
        self.date_format_string = date_format_string if isinstance(date_format_string, list) else [date_format_string]
        #* 도메인을 추가해야 할 경우 사용하는 문자열
        self.add_domain = add_domain
        #* 웹페이지와 상호작용하기 위한 웹 드라이버
        self.driver = self.get_driver()
        #* 로그 정보를 저장
        self.log = dict()
        #* Selenium 옵션
        self.selenium_options = None
        #* 필수 키워드
        self.essential_keywords = None
        #* 제외 키워드
        self.except_keywords = None
        #* BeautifulSoup 객체
        self.soup = None

    #* 객체 내의 log 딕셔너리를 설정하는 메서드
    # variable - self : 객체 자신을 참조하는 변수(클래스 내부에서 객체의 속성이나 메서드에 접근할 때 사용)
    # variable - type : 로그의 타입을 나타내는 문자열. 예를 들면, 오류 유형, 알림 유형 등의 로그 카테고리를 나타냄
    # variable - position : 로그가 발생한 위치나 상황을 설명하는 문자열
    # variable - log : 로그의 실제 내용을 나타내는 문자열
    def set_log(self, type, position, log):
        # 해석 : log라는 이름의 빈 딕셔너리를 객체의 속성으로 초기화
        self.log = dict()
        self.log['type'] = type
        self.log['position'] = position
        self.log['log'] = log

    #* log 딕셔너리에 일부 추가 정보를 설정한 다음 MongoDB 데이터베이스에 해당 로그를 삽입하는 메서드
    def log_insert(self):
        # 해석 : 현재의 날짜와 시간 정보를 log 딕셔너리의 'created_at' 키에 할당
        self.log['created_at'] = datetime.now()
        # 해석 : data 객체의 url 속성 값을 log 딕셔너리의 'url' 키에 할당
        self.log['url'] = self.data.url
        # 해석 : deepcopy(self.log)를 사용하여 log 딕셔너리의 깊은 복사본을 생성
        #        그 다음 mongo_client의 log_insert 메서드를 호출하여 로그 정보를 MongoDB 데이터베이스에 삽입
        #        깊은 복사본을 사용하는 이유는 원본 log 딕셔너리의 데이터를 변경하지 않기 위해서
        mongo_client.log_insert(deepcopy(self.log))

    #* Selenium에서 사용되는 Chrome 웹 드라이버의 설정을 정의(get_driver에서 사용)
    def set_chrome_options(self):
        # 해석 : ChromeOptions() 객체를 생성하여 selenium_options 속성에 할당
        self.selenium_options = ChromeOptions()
        # self.selenium_options.headless = True
        # 해석 : Chrome 웹 브라우저를 GUI 없이 실행하도록 하는 headless 모드를 설정
        self.selenium_options.add_argument('--headless=new')
        # 해석 : 사용자 에이전트(User Agent) 문자열을 설정(브라우저가 웹 서버에게 자신을 어떤 브라우저로 소개하는지를 결정)
        #        브라우저를 마치 다른 브라우저처럼 보이게 할 수 있음
        #        문자열 - Windows 10 64비트 운영 체제에서 실행되는 Chrome 브라우저 버전 112.0.0.0을 나타냄
        # 사용 이유 : 제한을 우회하기 위해 자동화 스크립트에서는 일반 브라우저에서 사용되는 User-Agent 문자열을 사용하여 웹 서버를 속일 수 있음
        self.selenium_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
        # 해석 : Chrome에서 특정 스위치를 비활성화
        self.selenium_options.add_argument('--excludeSwitches=enable-automation,enable-logging')
        # 해석 : SSL/TLS 인증서 오류를 무시하도록 합니다. 보안에 관한 경고가 나타나지 않도록 설정
        self.selenium_options.add_argument("--ignore-certificate-errors")
        # 해석 : Chrome의 보안 모드인 sandbox를 비활성화
        self.selenium_options.add_argument('--no-sandbox')
        # 해석 : /dev/shm을 사용하지 않도록 설정(Docker와 같은 일부 환경에서 메모리 문제를 피하기 위해 사용)
        self.selenium_options.add_argument('--disable-dev-shm-usage')
        # 해석 : 브라우저를 최대화된 상태로 시작
        self.selenium_options.add_argument('--start-maximized')
        # 해석 : 팝업 차단 기능을 비활성화
        self.selenium_options.add_argument('--disable-popup-blocking')
        # 해석 : 브라우저를 익명 모드(시크릿 모드)로 시작
        self.selenium_options.add_argument('--incognito')
        # 해석 : GPU 하드웨어 가속을 비활성화(일부 시스템에서 그래픽 문제를 방지)
        self.selenium_options.add_argument('--disable-gpu')
        # 컨테이너 환경용(Chrome 브라우저의 바이너리 위치를 지정)
        # self.selenium_options.binary_location = '/usr/bin/chromium'

    #* 웹 스크래핑 작업을 위해 Selenium이 제어하는 ​​Chrome 웹 브라우저를 가져옴(초기화 할 때 사용)
    def get_driver(self):
        self.set_chrome_options()
        # 컨테이너 환경용
        # variable - driver_executable_path : Chrome 드라이버의 실행 경로를 지정
        # variable - version_main : 사용하고자 하는 Chrome의 메인 버전을 지정
        # variable - options : set_chrome_options에서 설정한 옵션들을 웹 드라이버에 전달
        self.driver = Chrome(driver_executable_path='C:/BackDev/chromedriver_118/chromedriver',
                             version_main=115,
                             options=self.selenium_options)

        # 로컬 환경용 ( yunjae 맥)
        # self.driver = Chrome(service=Service('/usr/local/bin/google-chrome-stable'),
        #                      version_main=114,
        #                      options=self.selenium_options)

        # 해석 : 웹 드라이버가 웹 요소를 찾을 때 최대 10초 동안 기다리게 됩니다. 웹 요소가 그 시간 안에 발견되면 실행을 계속하고, 그렇지 않으면 오류를 발생시킴
        self.driver.implicitly_wait(10)
        return self.driver

    #* 브라우저에서 해당 URL을 렌더링하여 웹 페이지를 가져옴
    def request_bs(self, url):
        response = requests.get(url)
        self.set_soup(response.content)

    #* Selenium을 사용하여 웹 페이지를 불러온 후, BeautifulSoup을 이용해 페이지의 소스를 파싱(search, load_detail_page에서 사용)
    def selenium_bs(self, url):
        try:
            # 해석 : Selenium의 웹 드라이버를 사용하여 주어진 URL에 접근
            self.driver.get(url)
            # 해석 : 페이지가 완전히 로드될 때까지 1~2초 동안 대기합니다. randrange를 사용하여 무작위로 대기 시간을 결정하므로 웹 사이트의 anti-bot 시스템을 피할 수 있음
            sleep(randrange(1, 3))
            # 해석 : 웹 드라이버로부터 가져온 웹 페이지의 소스코드를 set_soup 메서드를 사용하여 BeautifulSoup 객체로 파싱
            self.set_soup(self.driver.page_source)
            # 해석 : 웹 페이지 내에 특정 iframe이 있는지 검사
            if self.iframe_id and self.soup.select_one(f'iframe#{self.iframe_id}') != None :
                # 해석 : iframe으로 전환해 소스코드를 가져와 BeautifulSoup 객체로 파싱
                self.driver.switch_to.frame(self.iframe_id)
                self.set_soup(self.driver.page_source)
        except Exception as e:
            # 해석 : 오류 관련 정보를 self.log에 저장하고, SeleniumError라는 사용자 정의 예외를 발생시킴
            self.log['position'] = 'SeleniumError'
            self.log['type'] = 'Error'
            raise SeleniumError(e)
    #* 해당 페이지에서 원하는 데이터를 가져올 수 있는 객체를 만듦 (request_bs, selenium_bs에서 사용)
    def set_soup(self, response):
        self.soup = BeautifulSoup(response, "html.parser")

    #* 스크래핑할 콘텐츠에 대한 주어진 메타데이터를 객체의 속성과 로그에 설정
    def set_metadata(self, keyword, company, cp_id, essential_keywords, except_keywords):
        # variable - keyword : 검색 또는 분류에 사용되는 키워드
        self.data.keyword = keyword
        # variable - movie  : 특정 영화나 프로그램의 이름 또는 정보
        self.data.company = company
        # variable - cp_id  : 콘텐츠 제공업체(Content Provider)의 ID 또는 식별자
        self.data.cp_id = cp_id
        # variable - essential_keywords  : 필수 키워드(어떤 콘텐츠를 선택하거나 검색할 때 반드시 포함되어야 하는 키워드)
        self.essential_keywords = essential_keywords
        # variable - except_keywords  : 제외 키워드(어떤 콘텐츠를 선택하거나 검색할 때 반드시 제외되어야 하는 키워드)
        self.except_keywords = except_keywords
        # 해석 : 로그에 저장함
        self.log['keyword'] = keyword
        self.log['company'] = company
        self.log['cp_id'] = cp_id
        self.log['osp'] = self.data.osp

    #* 주어진 post 인자를 기반으로 상세 페이지를 로드
    def load_detail_page(self, post):
        # 해석 : post가 URL이라면 이 조건문 내의 코드를 실행
        if isinstance(post, str):
            # 해석 : 'http' in post - post 문자열에 'http'가 포함되어 있는지 확인
            # 해석 : self.add_domain_in_url(post) - 만약 post에 'http'가 포함되어 있지 않다면, 이는 완전한 URL이 아닐 가능성이 있으므로, 도메인을 추가
            self.data.url = self.add_domain_in_url(post) if not 'http' in post else post
            self.selenium_bs(self.data.url)
        else:
            # 해석 : post 객체를 직접 self.soup에 저장, post가 이미 웹 페이지의 내용을 파싱한 BeautifulSoup 객체라는 것을 의미
            self.soup = post

    #* 웹 페이지에서 데이터를 추출하고 파싱
    def get_data(self):
        try:
            # self.elements는 딕셔너리 구조로, 각 키와 관련된 선택자 정보를 포함, 각 아이템에 대해 순회
            for key, element in self.elements.items():
                # self.data 객체의 속성 중 이름이 key인 속성에 크롤링한 데이터를 설정합니다. 이렇게 함으로써 웹 페이지에서 추출한 여러 데이터들을 self.data 객체에 저장
                self.data.__setattr__(key, self.crawl_data(element))
            # 해석 : 웹 페이지에서 추출한 원시 데이터를 필요한 형태나 포맷으로 변환
            self.parsing_data()
            # 해석 : 데이터가 생성된 시점을 기록
            self.data.created_at = datetime.now()
        except Exception as e:
            self.log['position'] = 'ParsingError'
            self.log['type'] = 'Error'
            # 해석 : 해당 예외가 데이터 파싱 과정에서 발생했음을 명시적으로 표시하고, 예외 처리
            raise ParsingError(e)
    #* 웹 페이지 요소의 선택자(element)를 기반으로 데이터를 크롤링하는 역할(get_data, get_post_list에서 사용)
    def crawl_data(self, element):
        # variable - element.what : 선택자와 속성의 튜플 리스트
        for selector, attr in element.what:
            try:
                # 해석 : just라는 속성 값이 주어진 경우, 선택자 자체(selector)를 그대로 반환
                if attr == 'just':
                    return selector
                # variable - element.how : 데이터를 선택하는 방식을 나타내는 값
                # variable - SELECTOR : BeautifulSoup의 CSS 선택자를 나타낼 수 있는 상수
                elif element.how == SELECTOR:
                    # 해석 : BeautifulSoup의 select 메서드를 사용하여 데이터를 선택
                    selected_elements = self.soup.select(selector)
                else:
                    # 해석 : lxml의 xpath를 사용하여 데이터를 선택
                    selected_elements = etree.HTML(str(self.soup)).xpath(selector)
                # 해석 : 선택된 요소가 없으면, 다음 선택자와 속성의 튜플로 반복을 계속
                if not selected_elements:
                    continue
                # 해석 : 여러 요소를 선택해야하는 경우(element.many가 True일 때), 여러 요소의 데이터를 가져옴
                if element.many:
                    if isinstance(selected_elements[0], str):
                        return [ele.strip() for ele in selected_elements]
                    return [ele.text.strip() if attr == 'text' else ele if attr == 'element' else ele[
                        attr].strip() if element.how == SELECTOR else ele.get(attr).strip() for ele in
                            selected_elements]
                # 해석 : 단일 요소의 데이터만 필요한 경우, 첫 번째 선택된 요소의 데이터를 가져옴
                else:
                    ele = selected_elements[0]
                    if isinstance(ele, str):
                        return ele.strip()
                    return ele.text.strip() if attr == 'text' else ele if attr == 'element' else ele[
                        attr].strip() if element.how == SELECTOR else ele.get(attr).strip()
            except:
                continue
    #* 추출된 데이터, 특히 날짜를 정리(parsing_data에서 사용)
    def format_date(self):
        # 해석 : 날짜 문자열 내에 줄바꿈 문자가 있는지 확인합니다. 있다면, 줄바꿈 문자를 제거
        if '\n' in self.data.write_date: # 처리되어야 하는 날짜 정보를 포함
            self.data.write_date = sub('\n', '', self.data.write_date)

        # 해석 : 날짜가 상대적인 시간 형식(예: "3분 전", "2일 전")으로 주어졌는지 확인합니다.
        #        해당 경우에는, 상대적인 시간을 절대적인 datetime 객체로 변환
        if '전' in self.data.write_date:
            self.data.write_date = sub(r'(\d+)(?!\s)', r'\1 ', self.data.write_date)
            # 해석 : 날짜 문자열을 공백으로 분할하여 토큰으로 만듦
            tokens = self.data.write_date.split(' ')
            # 해석 : 토큰을 기반으로 상대적인 시간의 단위(초, 분, 시간, 일, 주, 개월, 년)를 파악하고, 해당 단위에 따라 timedelta 객체를 생성
            #        timedelta는 현재 시간에서 빼거나 더해서 절대적인 날짜를 얻음
            if tokens[1] == '초':
                delta = timedelta(seconds=int(tokens[0]))
            elif tokens[1] == '분':
                delta = timedelta(minutes=int(tokens[0]))
            elif tokens[1] == '시간':
                delta = timedelta(hours=int(tokens[0]))
            elif tokens[1] == '일':
                delta = timedelta(days=int(tokens[0]))
            elif tokens[1] == '주':
                delta = timedelta(weeks=int(tokens[0]))
            elif tokens[1] == '개월':
                delta = timedelta(days=30 * int(tokens[0]))  # 1개월은 30일로 가정
            elif tokens[1] == '년':
                delta = timedelta(days=365 * int(tokens[0]))  # 1년은 365일로 가정
            now = datetime.now()
            self.data.write_date = now - delta
        else:
            # 해석 : 날짜가 상대적인 형식이 아닌 경우, 다양한 날짜 형식 문자열을 사용하여 날짜 문자열을 파싱하려고 시도
            for format in self.date_format_string:
                try:
                    # 해석 : strptime 함수를 사용하여 주어진 날짜 형식 문자열과 일치하는지 확인
                    #        일치하는 형식이 발견되면, 해당 형식을 사용하여 날짜 문자열을 datetime 객체로 변환
                    self.data.write_date = datetime.strptime(self.data.write_date, format)
                    break
                except:
                    continue

    #* 웹 페이지에서 추출한 원시 데이터를 필요한 형태나 포맷으로 변환(get_data에서 사용)
    def parsing_data(self):
        # 해석 : 위 함수를 사용해 self.data.write_date에 저장된 날짜 데이터를 포맷팅
        self.format_date()
        # variable - self.data.url : 현재 인스턴스의 data 객체 내의 URL 정보
        # 해석 : URL이 'http'를 포함하고 있지 않은 경우, 도메인을 추가
        self.data.url = self.add_domain_in_url(self.data.url) if not 'http' in self.data.url else self.data.url
        # variable - self.data.title : 현재 인스턴스의 data 객체 내의 제목 정보
        # 해석 : 줄바꿈 문자(\n)와 탭 문자(\t)를 제거하여 제목을 정규화
        self.data.title = self.data.title.replace('\n', '').replace('\t', '')
        # variable - self.data.contents : 현재 인스턴스의 data 객체 내의 내용 정보
        if self.data.contents:
            # 해석 : 내용에 포함된 연속적인 줄바꿈, 탭, 또는 공백 문자를 단일 공백으로 치환(re 모듈의 sub 함수 활용)
            self.data.contents = sub(r'[\n\t ]{2,}', ' ', self.data.contents)
    #* 주어진 URL에 도메인을 추가(load_detail_page, parsing_data에서 사용)
    def add_domain_in_url(self, url):
        return self.add_domain + url

    #* 필수 키워드가 포함되어 있고, 제외 키워드가 포함되어 있지 않은 경우에만 데이터를 MongoDB에 삽입
    def content_insert(self):
        try:
            # function(is_in_essential_keyword) :  필수 키워드가 제목 또는 내용에 포함되어 있는지 확인
            # function(is_in_except_keyword) :  제외 키워드가 제목 또는 내용에 포함되어 있는지 확인
            if not self.is_in_essential_keyword() or self.is_in_except_keyword():
                return
            mongo_client.content_insert(self.data.to_dict(), deepcopy(self.log))
        except Exception as e:
            self.log['position'] = 'InsertError'
            self.log['type'] = 'Error'
            raise InsertError(e)

    #* 제목과 내용에 필수 키워드가 있는지 확인 
    def is_in_essential_keyword(self):
        title_contents = self.data.title + self.data.contents if self.data.contents else self.data.title
        title_contents = sub(r'\s', '', title_contents)
        for essential_keyword in self.essential_keywords:
            if essential_keyword in title_contents:
                return True
        self.log['type'] = 'info'
        self.log['position'] = '필수키워드'
        self.log['log'] = f'필수키워드({self.essential_keywords})가 검색되지 않아 데이터 삽입 불가'
        self.log_insert()
        return False

    #* 제목과 내용에 제외 키워드가 있는지 확인
    def is_in_except_keyword(self):
        title_contents = self.data.title + self.data.contents if self.data.contents else self.data.title
        for except_keyword in self.except_keywords:
            if except_keyword in title_contents:
                self.log['type'] = 'info'
                self.log['position'] = '제외키워드'
                self.log['log'] = f'제외키워드({except_keyword})가 있어서 데이터 삽입 불가'
                self.log_insert()
                return True
        return False
    
    #* 검색 URL 내의 {Keyword} 부분을 실제 검색어로 대체
    def parsing_search_url(self):
        self.search_url = self.search_url.replace('{Keyword}', self.data.keyword)

    #* 검색을 수행하기 위해 검색 URL을 파싱하고, 해당 URL로 Selenium을 통해 웹 페이지에 접속
    def search(self):
        self.parsing_search_url() # 검색 URL 가져옴
        self.selenium_bs(self.search_url) # selenium_bs로 웹페이지 가져옴

    #* 검색을 수행한 후에 포스트 목록을 가져옴
    def get_post_list(self):
        self.search() # 검색 수행
        # 해석 : 포스트 목록을 크롤링하기 위해 crawl_data 함수를 호출하며, 그 결과(포스트 목록)를 반환
        # variable - post_selector : 포스트 목록을 선택하기 위한 CSS 선택자나 XPath 등의 선택기
        return self.crawl_data(self.post_selector)

    #* 게시물을 검색하고, 각 게시물을 로드하고, 데이터를 추출하고, 해당 데이터를 데이터베이스에 삽입
    def start_crawling(self):
        for post in self.get_post_list():
            try:
                #* 주어진 post 인자를 기반으로 상세 페이지를 로드
                self.load_detail_page(post)
                #* 웹 페이지에서 데이터를 추출하고 파싱
                self.get_data()
                #* 필수 키워드가 포함되어 있고, 제외 키워드가 포함되어 있지 않은 경우에만 데이터를 MongoDB에 삽입
                self.content_insert()
            except InsertError as e:
                self.log['log'] = e.message
                self.log_insert()
            except SeleniumError as e:
                self.log['log'] = e.message
                self.log_insert()
            except ParsingError as e:
                self.log['log'] = e.message
                self.log_insert()

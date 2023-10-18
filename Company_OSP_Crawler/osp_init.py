from classes.pageCrawler import PageCrawler
from classes.scrollCrawler import ScrollCrawler
from classes.dto.data import Data
from classes.dto.element import Element

from classes.custom.remonterrace import Remonterrace
from classes.custom.dvdprime import Dvdprime
from classes.custom.ppomppu import Ppomppu
from classes.custom.instiz import Instiz
from classes.custom.clien import Clien
from classes.custom.ygosu import Ygosu
from classes.custom.women import Women
from classes.custom.twitter import Twitter
from classes.custom.tiktok import Tiktok
from classes.custom.naver_kin import NaverKin
from classes.custom.naver_news import NaverNews
from classes.custom.naver_post import NaverPost

from constant import *


def init_by_osp(osp):
    result = {
        # 커뮤니티
        '디시인사이드': init_dcinside,
        # '네이트판': init_natepann,
        'DVD프라임': init_dvdprime, 
        '인스티즈': init_instiz,
        '에펨코리아': init_fmkorea,
        'MLB파크': init_mlbpark,
        '뽐뿌': init_ppomppu,
        # '개드립': init_dogdrip,
        # '일베': init_ilbe,
        # '루리웹': init_ruliweb,
        '더쿠': init_theqoo,
        # '클리앙': init_clien,
        # '와이고수': init_ygosu,
        # '여성시대': init_women,
        '익스트림무비': init_extmovie,
        # '레몬테라스': init_remonterrace,
        # SNS
        '트위터': init_twitter,
        # '틱톡': init_tiktok,
        '유튜브': init_youtube,
        # 포탏
        '네이버_블로그': init_naver_blog,
        '네이버_카페': init_naver_cafe,
        # '네이버_지식in': init_naver_kin,
        '네이버_포스트': init_naver_post,
        '다음_카페': init_daum_cafe,
        # '티스토리': init_tistory, # 보류
        # news
        '네이버_뉴스': init_naver_news,
        '다음_뉴스': init_daum_news,
    }
    return result[osp]


# what은 무조건 이중 리스트로 입력해야함!
def init_natepann():
    return PageCrawler(
        osp='네이트판',
        platform=COMMUNITY,
        search_url='https://pann.nate.com/search/talk?q={Keyword}&sort=DD&page={Page}',
        # variable - post_selector: 검색 결과에서 개별 게시물의 URL을 크롤링하기 위한 셀렉터 정보
        # variable                  Element 클래스를 사용하여, h2>a라는 CSS 셀렉터로 찾아낸 요소의 href 속성값을 가져옴
        post_selector=Element(how=SELECTOR, what=[['h2>a', 'href']], many=True),
        # variable - add_domain : href의 URL이 상대 URL이라면 그 앞에 붙여줄 도메인 URL
        add_domain='https://pann.nate.com',
        # variable - selector_dic : 개별 게시물의 내용을 크롤링하기 위한 셀렉터들의 딕셔너리
        selector_dic={
            # 해석 : 각 키에 대해서 어떻게(셀렉터)와 무엇을(텍스트나 속성 값) 크롤링할 것인지를 정의
            'title': Element(how=SELECTOR, what=[['div.post-tit-info>h1', 'text']]),
            'writer': Element(how=SELECTOR, what=[['a.writer', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['span.date', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div#contentArea', 'text']]),
        },
        # variable - date_format_string: 날짜와 시간 정보를 파싱하기 위한 포맷 문자열
        date_format_string='%Y.%m.%d %H:%M',
        # variable - data : 클래스의 인스턴스로, 크롤링된 데이터를 저장하기 위한 데이터 구조
        data=Data(),
    )


def init_dvdprime():
    return Dvdprime(
        osp='DVD프라임',
        platform=COMMUNITY,
        search_url='https://dprime.kr/g2/bbs/search.php?#gsc.tab=0&gsc.q={Keyword}&gsc.page={Page}',
        post_selector=Element(how=SELECTOR, what=[['div.gsc-thumbnail-inside:first-child a[href]', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['h1', 'text']]),
            'writer': Element(how=SELECTOR, what=[['div#view_nickname', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['div#view_datetime', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div#resContents', 'text']]),
        },
        data=Data(),
    )


def init_dcinside():
    return PageCrawler(
        osp='디시인사이드',
        platform=COMMUNITY,
        search_url='https://search.dcinside.com/post/p/{Page}/sort/latest/q/{Keyword}',
        post_selector=Element(how=SELECTOR, what=[['ul.sch_result_list a[href*="&no"]', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['span.title_subject', 'text']]),
            'writer': Element(how=SELECTOR, what=[['div.fl > span.ip', 'text'], ['header div.gall_writer.ub-writer', 'data-nick']]),
            'write_date': Element(how=SELECTOR, what=[['span.gall_date', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div.writing_view_box', 'text']]),
        },
        date_format_string='%Y.%m.%d %H:%M:%S',
        data=Data(),
    )


def init_instiz():  
    return Instiz(
        osp='인스티즈',
        platform=COMMUNITY,
        search_url='https://www.instiz.net/name?page={Page}&category=1&k={Keyword}&stype=1',
        post_selector=Element(how=SELECTOR, what=[['tr#topboard~tr#detour a:not([class]):nth-child(1)', 'href']], many=True),
        add_domain='https://www.instiz.net',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['span#nowsubject', 'text']]),
            'writer': Element(how=SELECTOR, what=[['익명', 'just']]),
            'write_date': Element(how=SELECTOR, what=[['span[title][itemprop]', 'title']]),
            'contents': Element(how=SELECTOR, what=[['div.memo_content', 'text']]),
        },
        date_format_string='%Y.%m.%d %H:%M:%S',
        data=Data(),
    )


def init_fmkorea():
    return PageCrawler(
        osp='에펨코리아',
        platform=COMMUNITY,
        search_url='https://www.fmkorea.com/search.php?act=IS&is_keyword={Keyword}&where=document&page={Page}',
        post_selector=Element(how=SELECTOR, what=[['li > dl> dt > a', 'href']], many=True),
        add_domain='https://www.fmkorea.com',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['h1 > span', 'text']]),
            'writer': Element( how=SELECTOR, what=[['div.side > a', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['span.date', 'text']]),
            'contents': Element(how=SELECTOR, what=[['article > div', 'text']]),
        },
        date_format_string='%Y.%m.%d %H:%M',
        data=Data(),
    )


def init_mlbpark():
    return PageCrawler(
        osp='MLB파크',
        platform=COMMUNITY,                             # 페이지 아니고 offset (30개 씩) (1-> 31 -> 61)
        search_url='https://mlbpark.donga.com/mp/b.php?p={Page}&m=search&b=bullpen&query={Keyword}&select=sct&user=',
        post_selector=Element(how=SELECTOR, what=[['div.tit > a[alt]', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['div.titles', 'text']]),
            'writer': Element( how=SELECTOR, what=[['ul.view_head span.nick', 'text']]),
            'write_date': Element(how=XPATH, what=[['//span[@class="val"][contains(text(), ":")]', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div#contentDetail', 'text']]),
        },
        date_format_string='%Y-%m-%d %H:%M',
        data=Data(),
    )


def init_ppomppu():
    return Ppomppu(
        osp='뽐뿌',
        platform=COMMUNITY,
        search_url='https://www.ppomppu.co.kr/search_bbs.php?search_type=sub_memo&page_no={Page}&keyword={Keyword}&page_size=50&order_type=date&bbs_cate=2',
        post_selector=Element(how=SELECTOR, what=[['span.title > a', 'href']], many=True),
        add_domain='https://www.ppomppu.co.kr',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['font.view_title2', 'text']]),
            'writer': Element( how=SELECTOR, what=[['span[title] > a > font', 'text'], ['span[title] img[alt]', 'alt'], ['비회원', 'just']]),
            'write_date': Element(how=SELECTOR, what=[['div.sub-top-text-box', 'text']]),
            'contents': Element(how=SELECTOR, what=[['tr > td.board-contents', 'text']]),
        },
        date_format_string='%Y-%m-%d %H:%M',
        data=Data(),
    )


def init_dogdrip():
    return PageCrawler(
        osp='개드립',
        platform=COMMUNITY,
        search_url='https://www.dogdrip.net/dogdrip?_filter=search&search_target=title_content&search_keyword={Keyword}&page={Page}',
        post_selector=Element(how=SELECTOR, what=[['tr:not([class="notice"]) td.title a.link-reset', 'href']], many=True),
        add_domain='https://www.dogdrip.net',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['h4 > a', 'text']]),
            'writer': Element( how=SELECTOR, what=[['span > a[class*="member"]', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['span~span.text-xsmall', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div#article_1', 'text']]),
        },
        date_format_string='%Y.%m.%d',
        data=Data(),
    )


def init_ilbe():
    return PageCrawler(
        osp='일베',
        platform=COMMUNITY,
        search_url='https://www.ilbe.com/search?docType=doc&searchType=title_content&page={Page}&q={Keyword}',
        post_selector=Element(how=SELECTOR, what=[['a.title', 'href']], many=True),
        add_domain='https://www.ilbe.com',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['h3 > a', 'text']]),
            'writer': Element( how=SELECTOR, what=[['h3~span.nick > a', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['span.comment-num~span.date', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div.post-content', 'text']]),
        },
        data=Data(),
    )


def init_ruliweb():
    return PageCrawler(
        osp='루리웹',
        platform=COMMUNITY,
        search_url='https://bbs.ruliweb.com/search?q={Keyword}#gsc.tab=0&gsc.page={Page}',
        post_selector=Element(how=SELECTOR, what=[['div.result>div:not(#comment_search) li a:first-child', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['h4.subject', 'text'], ['td.m1 > a', 'text']]),
            'writer': Element( how=XPATH, what=[['//a[@class="nick"] | //div[@class="mypiNick"]/text()[1]', 'text']]),
            'write_date': Element(how=XPATH, what=[['//span[@class="regdate"] | //td[@class="m1"]/text()', 'text']]),
            'contents': Element(how=SELECTOR, what=[['article > div', 'text'],['div.story', 'text']]),
        },
        date_format_string=['%Y.%m.%d (%H:%M:%S)', '%Y/%m/%d %p %I:%M'],
        data=Data(),
    )


def init_theqoo():
    return PageCrawler(
        osp='더쿠',
        platform=COMMUNITY,
        search_url='https://theqoo.net/total?_filter=search&search_target=title_content&search_keyword={Keyword}&page={Page}',
        post_selector=Element(how=SELECTOR, what=[['tr:not(.notice) td.title>a:first-child', 'href']], many=True),
        add_domain='https://theqoo.net',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['span.title', 'text']]),
            'writer': Element( how=SELECTOR, what=[['익명', 'just']]),
            'write_date': Element(how=SELECTOR, what=[['div.fr > span', 'text']]),
            'contents': Element(how=SELECTOR, what=[['article > div', 'text']]),
        },
        date_format_string='%Y.%m.%d %H:%M',
        data=Data(),
    )


def init_clien():
    return Clien(
        osp='클리앙',
        platform=COMMUNITY,
        search_url='https://www.clien.net/service/search?boardCd=&isBoard=false&sort=recency&q={Keyword}&p={Page}',
        post_selector=Element(how=SELECTOR, what=[['button~a', 'href']], many=True),
        add_domain='https://www.clien.net',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['h3 > span', 'text']]),
            'writer': Element( how=SELECTOR, what=[['span.nickname > span', 'title']]),
            'write_date': Element(how=SELECTOR, what=[['div.post_author > span:first-child', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div.post_article', 'text']]),
        },
        data=Data(),
    )


def init_ygosu():
    return Ygosu(
        osp='와이고수',
        platform=COMMUNITY,
        search_url='https://ygosu.com/all_search/?keyword={Keyword}&current_page={Page}',
        post_selector=Element(how=SELECTOR, what=[['li.default_body dt > a', 'href']], many=True),
        add_domain='https://ygosu.com',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['div.tit > h3', 'text']]),
            'writer': Element( how=SELECTOR, what=[['div.nickname > a', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['div.date', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div.container', 'text']]),
        },
        data=Data(),
    )


def init_extmovie():
    return PageCrawler(
        osp='익스트림무비',
        platform=COMMUNITY,
        search_url='https://extmovie.com/index.php?mid=home&act=IS&search_target=title_content&where=document&is_keyword={Keyword}&page={Page}',
        post_selector=Element(how=SELECTOR, what=[['a.document_link', 'href']], many=True),
        add_domain='https://extmovie.com',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['a.atc_title', 'text']]),
            'writer': Element(how=SELECTOR, what=[['span.atc_nickname > a', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['span > time', 'datetime']]),
            'contents': Element(how=SELECTOR, what=[['div.atc_body > div:first-child', 'text']]),
        },
        date_format_string='%Y-%m-%dT%H:%M:%S+09:00',
        data=Data(),
    )


def init_women():
    return Women(
        osp='여성시대',
        platform=COMMUNITY,
        iframe_id='down',
        search_url='https://cafe.daum.net/_c21_/cafesearch?grpid=1IHuH&listnum=20&item=subject&sorttype=0&query={Keyword}&pagenum={Page}',
        post_selector=Element(how=SELECTOR, what=[['td.searchpreview_subject > a:nth-of-type(1)', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['strong.tit_info', 'text']]),
            'writer': Element(how=SELECTOR, what=[['a[data-nickname]', 'data-nickname']]),
            'write_date': Element(how=SELECTOR, what=[['span.txt_item:nth-child(4)', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div#user_contents', 'text']]),
        },
        date_format_string='%y.%m.%d %H:%M',
        data=Data(),
    )


def init_remonterrace():
    return Remonterrace(
        osp='레몬테라스',
        platform=COMMUNITY,
        iframe_id='cafe_main',
        search_url='https://cafe.naver.com/ArticleSearchList.nhn?search.clubid=10298136&search.media=0&search.searchdate=all&search.defaultValue=1&userDisplay=50&search.option=0&search.sortBy=date&search.searchBy=1&search.viewtype=title&search.query={Keyword}&search.page={Page}',
        post_selector=Element(how=SELECTOR, what=[['a.article', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['div.tit-box span', 'text']]),
            'writer': Element(how=SELECTOR, what=[['div.etc-box td.p-nick>a', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['div.tit-box td.date', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div.se-main-container', 'text'], ['div#tbody', 'text']]),
        },
        date_format_string='%Y.%m.%d. %H:%M',
        data=Data(),
    )


def init_twitter():
    return Twitter(
        osp='트위터',
        platform=SNS,
        search_url='https://twitter.com/search?q={Keyword} -filter:replies&src=typed_query&f=live',
        post_selector=Element(how=SELECTOR, what=[['article[data-testid="tweet"]', 'element']], many=True),
        add_domain='https://twitter.com',
        selector_dic={
            'url': Element(how=SELECTOR, what=[['div>a[dir="ltr"]', 'href']]),
            'title': Element(how=SELECTOR, what=[['div[data-testid="User-Name"] a', 'text']]),
            'writer': Element(how=SELECTOR, what=[['div[data-testid="User-Name"] a', 'href']]),
            'write_date': Element(how=SELECTOR, what=[['time', 'datetime']]),
            'contents': Element(how=SELECTOR, what=[[' div[data-testid="tweetText"]', 'text']]),
        },
        date_format_string='%Y-%m-%dT%H:%M:%S.000Z',
        data=Data(),
    )


def init_tiktok():
    return Tiktok(
        osp='틱톡',
        platform=SNS,
        search_url='https://www.tiktok.com/search?q={Keyword}',
        post_selector=Element(how=SELECTOR, what=[['div.tiktok-1soki6-DivItemContainerForSearch', 'element']], many=True),
        selector_dic={
            'url': Element(how=SELECTOR, what=[['div.e1cg0wnj0 a', 'href']]),
            'writer': Element(how=SELECTOR, what=[['div.tiktok-dq7zy8-DivUserInfo > p', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['div.tiktok-842lvj-DivTimeTag', 'text']]),
            'title': Element(how=SELECTOR, what=[['div.etrd4pu0 > div > div > div.ejg0rhn0', 'text']]),
        },
        date_format_string='%Y-%m-%d',
        data=Data(),
    )


def init_youtube():
    return ScrollCrawler(
        osp='유튜브',
        platform=SNS,
        search_url='https://www.youtube.com/results?search_query={Keyword}&sp=CAI%253D',
        post_selector=Element(how=SELECTOR, what=[['a#video-title:not([href*="/shorts/"])', 'href']], many=True),
        add_domain='https://www.youtube.com',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['#title > h1 > yt-formatted-string', 'text']]),
            'writer': Element(how=SELECTOR, what=[['div#upload-info > #channel-name a', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['#info > span:nth-child(3)', 'text']]),
            'contents': Element(how=SELECTOR, what=[['#bottom-row > #description', 'text']]),
        },
        date_format_string='%Y-%m-%dT%H:%M:%S.000Z',
        data=Data(),
    )


def init_naver_blog():
    return ScrollCrawler(
        osp='네이버_블로그',
        platform=PORTAL,
        iframe_id='mainFrame',
        search_url='https://search.naver.com/search.naver?where=blog&query={Keyword}',
        post_selector=Element(how=SELECTOR, what=[['a.total_tit[href*="blog.naver"]', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['div.pcol1 span', 'text']]),
            'writer': Element(how=SELECTOR, what=[['span.nick>a', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['span.se_publishDate', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div.se-main-container', 'text']]),
        },
        date_format_string='%Y. %m. %d. %H:%M',
        data=Data(),
    )


def init_naver_cafe():
    return ScrollCrawler(
        osp='네이버_카페',
        platform=PORTAL,
        iframe_id='cafe_main',
        search_url='https://search.naver.com/search.naver?where=articleg&query={Keyword}',
        post_selector=Element(how=SELECTOR, what=[['a.total_tit[href*="cafe.naver"]', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['h3.title_text', 'text']]),
            'writer': Element(how=SELECTOR, what=[['button.nickname', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['span.date', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div.se-main-container', 'text']]),
        },
        date_format_string='%Y.%m.%d. %H:%M',
        data=Data(),
    )


def init_naver_kin():
    return NaverKin(
        osp='네이버_지식in',
        platform=PORTAL,
        search_url='https://search.naver.com/search.naver?where=kin&query={Keyword}&kin_start={Page}',
        post_selector=Element(how=SELECTOR, what=[['a[data-url*="kin.naver"]', 'data-url']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['div.question-content div.title', 'text']]),
            'writer': Element(how=XPATH, what=[['//div[@class="question-content"]//span[@class="c-userinfo__author"]/text()', 'text']]),
            'write_date': Element(how=XPATH, what=[['//div[@class="question-content"]//span[@class="c-userinfo__info"][1]/text()', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div.question-content div.c-heading__content', 'text']]),
        },
        date_format_string='%Y.%m.%d',
        data=Data(),
    )


def init_naver_post():
    return NaverPost(
        osp='네이버_포스트',
        platform=PORTAL,
        search_url='https://post.naver.com/search/post.naver?sortType=createDate.dsc&term=all&navigationType=current&keyword={Keyword}',
        post_selector=Element(how=SELECTOR, what=[['div.text_area>a:last-child', 'href']], many=True),
        add_domain='https://post.naver.com',
        selector_dic={
            'title': Element(how=SELECTOR, what=[['h3.se_textarea', 'text']]),
            'writer': Element(how=SELECTOR, what=[['span.se_author', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['span.se_publishDate', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div.__se_component_area', 'text']]),
        },
        date_format_string='%Y.%m.%d. %H:%M',
        data=Data(),
    )


def init_daum_cafe():
    return PageCrawler(
        osp='다음_카페',
        platform=PORTAL,
        iframe_id='down',
        search_url='https://top.cafe.daum.net/_c21_/search/cafe-table?searchOpt=CAFE_ARTICLE&articleSortType=RECENCY&q={Keyword}&p={Page}',
        post_selector=Element(how=SELECTOR, what=[['strong.tit_list a[href*="cafe.daum.net"]', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['strong.tit_info', 'text']]),
            'writer': Element(how=SELECTOR, what=[['a[data-nickname]', 'data-nickname']]),
            'write_date': Element(how=SELECTOR, what=[['span.txt_item:nth-child(4)', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div#user_contents', 'text']]),
        },
        date_format_string='%y.%m.%d %H:%M',
        data=Data(),
    )


# 보류
def init_tistory():
    return PageCrawler(
        osp='티스토리',
        platform=PORTAL,
        iframe_id='down',
        search_url='https://top.cafe.daum.net/_c21_/search/cafe-table?searchOpt=CAFE_ARTICLE&articleSortType=RECENCY&q={Keyword}&p={Page}',
        post_selector=Element(how=SELECTOR, what=[['strong.tit_list a[href*="cafe.daum.net"]', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['.category~h1', 'text'],['.title_post', 'text']]),
            'writer': Element(how=SELECTOR, what=[['a[data-nickname]', 'data-nickname']]),
            'write_date': Element(how=SELECTOR, what=[['span.txt_item:nth-child(4)', 'text']]),
            'contents': Element(how=SELECTOR, what=[['div#user_contents', 'text']]),
        },
        date_format_string='%y.%m.%d %H:%M',
        data=Data(),
    )


def init_naver_news():
    return NaverNews(
        osp='네이버_뉴스',
        platform=NEWS,
        search_url='https://search.naver.com/search.naver?where=news&query={Keyword}&sort=1&start={Page}',
        max_page=10,
        post_selector=Element(how=SELECTOR, what=[['span.info~a', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['.media_end_head_title', 'text'],['h2.end_tit', 'text']]),
            'writer': Element(how=SELECTOR, what=[
                ['.media_end_head_journalist_name', 'text'], 
                ['.journalistcard_summary_name', 'text'], 
                ['.media_end_head_top img[alt][title]:first-child', 'title'], 
                ['a.press_logo>img', 'alt']
            ]),
            'write_date': Element(how=SELECTOR, what=[
                ['span[data-modify-date-time]', 'text'], 
                ['span[data-date-time]', 'text'], 
                ['span.author:last-of-type em', 'text']
            ]),
            'contents': Element(how=SELECTOR, what=[['#dic_area', 'text'], ['.article_body', 'text']]),
        },
        date_format_string='%Y.%m.%d. %p %I:%M',
        data=Data(),
    )


def init_daum_news():
    return PageCrawler(
        osp='다음_뉴스',
        platform=NEWS,
        iframe_id='down',
        search_url='https://search.daum.net/search?w=news&show_dns=1&sort=recency&q={Keyword}&p={Page}',
        post_selector=Element(how=SELECTOR, what=[['li[data-docid] strong>a', 'href']], many=True),
        selector_dic={
            'title': Element(how=SELECTOR, what=[['.tit_view', 'text']]),
            'writer': Element(how=SELECTOR, what=[['.info_view>span:first-child', 'text']]),
            'write_date': Element(how=SELECTOR, what=[['.info_view span.num_date', 'text']]),
            'contents': Element(how=SELECTOR, what=[['.article_view>section', 'text']]),
        },
        date_format_string='%Y. %m. %d. %H:%M',
        data=Data(),
    )
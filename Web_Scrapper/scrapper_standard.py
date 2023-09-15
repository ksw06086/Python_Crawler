import sys, os
import urllib3

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common import *

urllib3.disable_warnings()

#! 크롤링 사이트의 도메인 Path 
osp_path = 'doramy.tv/'
#! 크롤링 사이트의 도메인 id
osp_id = 'doramy.tv'
osp_data = check_osp(osp_id)[0] #* osp_data ((connect_state 값, country 값))
"""
def check_osp(osp_id)
    #command master_conn -> 크롤링할 도메인의 값이 들어있는 MySQL DB
    #command with open(파일 경로, 모드) as 파일 객체 : 파일을 열고 해당 구문이 끝나면 자동으로 닫히게 됨, open된 파일을 파일객체(=변수)가 받음
    with master_conn.cursor() as master_curs:                                       #* MySQL DB의 값을 가져와 master_curs에 넣음
        master_conn.ping(reconnect=True)                                            #* MySQL DB 서버에 연결 가능한지 확인
        try:
            sql = "SELECT connect_state, country FROM global_osp_list where id=%s;" #* id에 해당하는 connect_state(현재 상태), country(해당 지역) 값 가져오는 SQL문
            master_curs.execute(sql, osp_id)                                        #* SQL문 실행
            result = master_curs.fetchall()                                         #* result 변수에 쿼리 결과 집합의 모든(또는 나머지 모든) 행을 가져오고 튜플 목록 반환. 더 이상 사용할 수 있는 행이 없으면 빈 목록을 반환
        except Exception as e:
            print(e)
        finally:
            if result == ():                                                        #* result가 빈 값일 때 -> 데이터 '1'을 넣어서 반환해줌
                result = [['1']]
            return result
"""


check_del = osp_data[0]     #* connect_state 값
country = osp_data[1]       #* country 값

FULL_PAGE = False           #* Pagenation이 꽉 찼는지


def start_crawling(c):
    max_page = {
        'mnogoserijnye-doramy': 258,    #* 드라마 시리즈 페이지
        'tok-shou': 3,                  #* 토크쇼 페이지
        'polnometrazhnye-doramy': 67,   #* 영화 드라마 페이지
    }[c] + 1 if FULL_PAGE else 4        #* FULL_PAGE가 False면 각 카테고리의 max_page+1 출력, True면 4 출력

    for i in range(1, max_page):
        link = f'https://doramy.tv/{c}/page/{i}/'               #? link : 소스 가져올 도메인 주소
        soup = requests_bs(link)
        """
        def requests_bs(url, types='get'):                      #? user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                                                                #?              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
            if types == 'get':                                  #? header = {'User-Agent': user_agent}
                r = requests.get(url, headers=header)           #* url 페이지에 get 요청 보내서 페이지 내용 가져오기
            elif types == 'post':
                r = requests.post(url, headers=header)          #* url 페이지에 post 요청 보내기 페이지 내용 가져오기
            else:
                return TypeError
            time.sleep(0.5)
            c = r.content                                       #* 내가 배웠던 text 역할을 함
            soup = BeautifulSoup(c, "html.parser")

            return soup                                         #* BeautifulSoup html 소스 가져오기
        """
        li = soup.select('a.short-item')                        #* class가 short-item인 a태그 선택
        for item in li:                                         #* a 태그 1개씩 item으로 가져오기
            try:
                data_list = []                                  #* data 담는 리스트
                title_sub = item.find('img')['alt'].strip()     #* 제목 값 가져오기
                title_check = title_null(title_sub)             #* 제목 값 못쓰는 text가 제목에 있으면 바꿔줌

                # 키워드 체크
                get_key = return_key()                          #* mysql DB에 있는 k.title, k.cnt_id, k.idx 리스트 보내줌
                """
                def return_key(korean=False):
                    try:
                        result = get_keyword(korean)            #* result에 mysql DB에 있는 k.title, k.cnt_id, k.idx 리스트 값 넣기
                        return_value = {}
                        for i in range(len(result)):            #* result 리스트의 크기만큼 돈다
                            key = result[i][0]                  #* k.title 값 가져와서 key에 넣기
                            if key in return_value:             #* k.title이 return_value에 들어갔다면 해당 key 값에 추가하기
                                return_value[key].append(result[i][1])
                                return_value[key].append(result[i][2])
                            else:                               #* k.title이 return_value에 없다면 update로 새로 넣기
                                return_value.update({key: [result[i][1], result[i][2]]})
                    finally:
                        return return_value
                """
                key_check = check_title(title_check, get_key)
                if key_check['m'] is None:
                    continue
                # 이미지 체크
                image_url = 'https://doramy.tv'+item.find('img')['data-src']        #* 우리가 찾던 드라마라면 링크 image_url에 넣기
                if get_img_base_compare(base_img, image_url, osp_path):             #? osp_path : 크롤링 사이트의 도메인 Path 
                    continue
                cnt_id = key_check['i']
                cnt_keyword = key_check['k']

                site_url = item['href'].strip()                                     #* 회차 정보 알 수 사이트 url 가져오기
                soup = requests_bs(site_url)                                        #* site_url에 대한 페이지 가져오기
                episodes = soup.select('a.b-simple_episode__item')                  #* 에피소드 a 태그 리스트 가져옴
                if not episodes:                                                    #* 에피소드 못 가져옴
                    if check_host_url(site_url):                                    #* 메인 DB에 있는 값인지 확인
                        print('중복 HOST URL !')                                    
                        continue
                    _data = data(cnt_id, osp_id, title_sub, title_check, site_url, site_url, cnt_keyword, country)      #* 에피소드 없는 화면이라서 hosturl에 siteurl을 넣음
                    data_list.append(_data)
                else:                                                               #* 에피소드 가져옴
                    for episode in episodes:
                        host_url = episode['href'].strip()                          #* 에피소드 링크 가져옴
                        if check_host_url(host_url):                                #* 메인 DB에 있는 값인지 확인
                            print('중복 HOST URL !')
                            continue
                        title = episode['title'].strip()                            #* 에피소드 명 가져와서 title 쓸 수 있는 String 문자열로 변환
                        _title_null = title_null(title)

                        _data = data(cnt_id, osp_id, title, _title_null, host_url, site_url, cnt_keyword, country)      
                        data_list.append(_data)

                if len(data_list) != 0:
                    insert_result = mongo_db_insert_many_result(data_list)
                    print(f'데이터 삽입 결과 : {insert_result}')
                else:
                    print('데이터 없음 !')

            except Exception as e:
                print(e)
                continue


if check_del:
    print('삭제된 osp!!!!')
    sys.exit()

print("doramy.tv 크롤링 시작")
base_img = get_base_img()
"""
def get_base_img():
    with master_conn.cursor() as master_curs:                           #* MySQL DB의 값을 가져와 master_curs에 넣음
        master_conn.ping(reconnect=True)                                #* MySQL DB 서버에 연결 가능한지 확인
        try:
            sql = "SELECT image " \                                     #* content_list Table에 main_cp가 sbs이고, image 컬럼이 null, '', '%undef%' 아닐 때
                  "FROM content_list " \
                  "WHERE main_cp = 'sbs' " \
                  "AND image IS NOT NULL " \
                  "AND image <> '' " \
                  "AND image NOT LIKE '%undef%' "
            # 출력 예시  -> ['abcd.jpg', 'abccde.jpg/efdg.jpg', '']
            master_curs.execute(sql)                                    #* SQL문 실행
            result = master_curs.fetchall()                             #* result 변수에 쿼리 결과 집합의 모든(또는 나머지 모든) 행을 가져오고 튜플 목록 반환. 더 이상 사용할 수 있는 행이 없으면 빈 목록을 반환

            query_result = [item[0] for item in result]                 #* query_result에 image 파일명 넣기

            return query_result
        except Exception as e:
            print(e)
"""
download_base_img(base_img, osp_path)   #? base_img : 이미지 명 / osp_path : 크롤링 사이트의 도메인 Path
for c in ['mnogoserijnye-doramy', 'tok-shou', 'polnometrazhnye-doramy']:
    start_crawling(c)
remove_osp_dir_image(osp_path)          #? osp_path : 크롤링 사이트의 도메인 Path
"""
def remove_osp_dir_image(osp_path):
    if os.path.exists(file_path + osp_path):                            #* file_path: 'C:/autogreen_crawler/crawler/global/image/', 해당 파일이 그 경로에 존재하는지 확인하는 메서드
        for file in os.scandir(file_path + osp_path):                   #* 지정된 경로에 의해 제공된 디렉토리의 항목에 해당하는 os.DirEntry 객체 의 반복자를 가져옴
            os.remove(file.path)                                        #* 가져온 os.DirEntry 객체 삭제
"""
print("doramy.tv 크롤링 끝")

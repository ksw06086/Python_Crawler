import sys, os
import urllib3

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from needDef import *

urllib3.disable_warnings()

osp_path = 'yyxx.tv/'
osp_id = 'yyxx.tv'
osp_data = check_osp(osp_id)[0]
check_del = osp_data[0]
country = osp_data[1]

FULL_PAGE = False


def start_crawling(c):
    max_page = {                                    #* 해당 사이트 카테고리 별 페이지
        '1': 982,
        '2': 413
    }[c] if FULL_PAGE else 4
    for i in range(1, max_page):
        link = f'https://yyxx.tv/vodshow/id/{c}/page/{i}'   #* 해당 사이트
        soup = requests_bs(link)
        li = soup.select('a.aplus-exp')            #* 해당 사이트 영화 목록 리스트
        for item in li:
            try:
                data_list = []
                title_sub = item['title'].strip()         #* 이미지 태그(제목)
                title_check = title_null(title_sub)

                # 키워드 체크
                get_key = return_key()
                key_check = check_title(title_check, get_key)
                if key_check['m'] is None:
                    continue
                # 이미지 체크
                # image_url = 'https://doramy.tv'+item.find('img')['data-src']
                # if get_img_base_compare(base_img, image_url, osp_path):
                #     continue
                cnt_id = key_check['i']
                cnt_keyword = key_check['k']

                site_url = item['href'].strip()                                     #* 영화 상세 링크
                soup = requests_bs(f"https://yyxx.tv{site_url}")
                hotline = soup.find('div.daoxu')                  #* 에피소드 링크
                episodes = hotline.select('a.t-u')
                if not episodes:
                    if check_host_url(site_url):
                        print('중복 HOST URL !')
                        continue
                    _data = data(cnt_id, osp_id, title_sub, title_check, site_url, site_url, cnt_keyword, country)
                    data_list.append(_data)
                else:
                    for episode in episodes:
                        host_url = episode['href'].strip()
                        if check_host_url(host_url):
                            print('중복 HOST URL !')
                            continue
                        title = episode['title'].strip()
                        _title_null = title_null(title)

                        _data = data(cnt_id, osp_id, title, _title_null, host_url, site_url, cnt_keyword, country)
                        data_list.append(_data)

                if len(data_list) != 0:
                    print(f'데이터 삽입 결과 : {data_list}')
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
download_base_img(base_img, osp_path)
for c in ['1', '2']:
    start_crawling(c)
remove_osp_dir_image(osp_path)
print("doramy.tv 크롤링 끝")

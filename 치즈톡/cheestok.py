import sys, os, time
import urllib3
import requests

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
header = {'User-Agent': user_agent}

osp_path = 'cheestok/'
osp_id = 'cheestok'
# osp_data = check_osp(osp_id)[0]
# check_del = osp_data[0]
# country = osp_data[1]

# FULL_PAGE = len(sys.argv)==2 and sys.argv[1]=='full'

def start_crawling():
    for i in range(1, 1240):
        link = f"https://api.cheestalk.com/recruit?page={i}"
        response = requests.get(link)
        time.sleep(2)
        data = response.json()
        print(data)
        # soup = requests_bs(link)
        # li = soup.select('a.aplus-exp')                         #* 목록 image 있는 곳의 anchor 태그 리스트 가져옴
        # for item in li:
        #     try:
        #         data_list = []
        #         title_sub = item['title'].strip()               
        #         title_check = title_null(title_sub)

        #         # 키워드 체크
        #         get_key = return_key()
        #         key_check = check_title(title_check, get_key)
        #         if key_check['m'] is None:
        #             continue
        #         # 이미지 체크
        #         image_url = item.select_one('div.eclazy')['data-original']
        #         if get_img_base_compare(base_img, image_url, osp_path):                 #* base_img : DB 이미지, image_url : html 코드에서 가져온 image_url, osp_path : 사이트(yyxx.tv/)
        #             continue
        #         cnt_id = key_check['i']
        #         cnt_keyword = key_check['k']

        #         site_url = f"https://yyxx.tv{item['href'].strip()}"
        #         soup = requests_bs(site_url)
        #         episode_boxs = soup.select('div.play_list_box')
        #         for episode_box in episode_boxs:
        #             episodes = episode_box.select('a.t-u')
        #             if not episodes:
        #                 if check_host_url(site_url):
        #                     print('중복 HOST URL !')
        #                     continue
        #                 _data = data(cnt_id, osp_id, title_sub, title_check, site_url, site_url, cnt_keyword, country)
        #                 data_list.append(_data)
        #             else:
        #                 for episode in episodes:
        #                     host_url = f"https://yyxx.tv{episode['href'].strip()}"
        #                     if check_host_url(host_url):
        #                         print('중복 HOST URL !')
        #                         continue
        #                     title = f"{title_sub} {episode.get_text().strip()}"
        #                     _title_null = title_null(title)

        #                     _data = data(cnt_id, osp_id, title, _title_null, host_url, site_url, cnt_keyword, country)
        #                     data_list.append(_data)

        #         if len(data_list) != 0:
        #             insert_result = mongo_db_insert_many_result(data_list)
        #             print(f'데이터 삽입 결과 : {insert_result}')
        #         else:
        #             print('데이터 없음 !')

        #     except Exception as e:
        #         print(e)
        #         continue


# if check_del:
#     print('삭제된 osp!!!!')
#     sys.exit()

print("cheestok 크롤링 시작")
start_crawling()
print("cheestok 크롤링 끝")

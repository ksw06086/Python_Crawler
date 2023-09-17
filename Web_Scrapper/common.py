import math
import os.path
import requests, re, pymysql, time, datetime, random
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input
import keras.utils as image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import uuid

master_conn = pymysql.connect(host='203.234.214.163',
                              port=3309,
                              user='unionUser',
                              password='Uni1975!!',
                              db='autogreen',
                              charset='utf8mb4',
                              autocommit=True,
                              connect_timeout=3600)

client = MongoClient(host='203.234.214.163',
                     port=27017,
                     username='unionUser',
                     password='UnionContents2020!@',
                     directConnection=True)
db = client.autogreen
main_data = db.global_main_data
# main_data = db.img_test

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
header = {'User-Agent': user_agent}

# file_path = '/Users/yunsmac/autogreen_crawler/crawler/global/image/'
file_path = 'C:/autogreen_crawler/crawler/global/image/'
base_img_link = "http://web.autogreen.co.kr/images/"


def requests_bs(url, types='get'):
    if types == 'get':
        r = requests.get(url, headers=header)
    elif types == 'post':
        r = requests.post(url, headers=header)
    else:
        return TypeError
    time.sleep(0.5)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    return soup


def requests_status_code(url):
    r = requests.get(url, headers=header, verify=False)
    random_sleep(1, 2)
    return r.status_code


def chrome_driver(headless=True, images_enabled=True, max_screen=False, mobile=False):
    global user_agent
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    if images_enabled:
        options.add_argument('--blink-settings=imagesEnabled=false')
    if max_screen:
        options.add_argument("--start-maximized")
    if mobile:
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone 12 Pro"})
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('user-agent=' + user_agent)
    options.add_argument("disable-gpu")
    options.add_argument('--incognito')
    try:
        driver = webdriver.Chrome(options=options)
    except FileNotFoundError as err:
        print(err)
    finally:
        return driver


def selenium_bs(driver, url):
    driver.get(url)
    driver.implicitly_wait(3)
    time.sleep(2)
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')

    return soup


def random_time_selenium_bs(driver, url, sleep_time):
    start = sleep_time[0]
    end = sleep_time[1]
    driver.get(url)
    driver.implicitly_wait(5)
    random_sleep(start, end)
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')

    return soup


def title_null(title):
    title = re.sub('[\[\]()\-,\'\"!─+?_~\/:★\. ]', '', title)
    title = re.sub('mp4|avi|mkv|NEXT|720p|1080p', '', title)
    title = title.strip()
    title = title.lower()

    return title


def numbers_only(string):
    return re.sub(r'[^0-9]', '', string)


def random_sleep(first, end):
    random_time = random.randint(first, end)
    time.sleep(random_time)


def data(cnt_title, osp, title, _title_null, host_url, site_url, keyword, country, is_google=False,
         is_twitter=False):
    now = datetime.datetime.now()
    if not is_twitter:
        cnt_title = get_cnt_title(cnt_title)[0]
    if not is_google:
        keyword = get_keyword_title(keyword)[0]
    _data = {
        'cntTitle': cnt_title,
        'osp': osp,
        'title': title,
        'titleNull': _title_null,
        'hostUrl': host_url,
        'siteUrl': site_url,
        'cpId': 'sbscp',
        'keyword': keyword,
        'country': country,
        'regdate': now,
        'state': '0',
        'mailCount': 0
    }
    print(_data)
    return _data


def mongo_db_find(where, select):
    field = {}
    for c in select.split(' '):
        field[c] = 1
    return main_data.find(where, field).sort("regdate")


def mongo_db_insert_one_result(_data):
    result = main_data.insert_one(_data)
    if 'InsertOneResult' in str(result):
        return True
    else:
        return False


def mongo_db_insert_many_result(data_list):
    result = main_data.insert_many(data_list, ordered=False)
    if 'InsertManyResult' in str(result):
        return True
    else:
        return False


def mongo_db_update_one(where, query):
    result = main_data.update_one(where, {"$set": query})
    if 'UpdateResult' in str(result):
        return True
    else:
        return False


def mongo_db_update_many(where, query):
    result = main_data.update_many(where, {"$set": query})
    if 'UpdateResult' in str(result):
        return True
    else:
        return False


def mailed_update(site_url, history):
    query = {"siteUrl": {"$in": site_url}}
    result = main_data.update_many(query, {"$set": {"mailSendDate": history['sendDate']},
                                           "$push": {"mailHistory": history},
                                           "$inc": {"mailCount": 1}})
    if 'UpdateResult' in str(result):
        return True
    else:
        return False


def check_osp(osp_id):
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT connect_state, country FROM global_osp_list where id=%s;"
            master_curs.execute(sql, osp_id)
            result = master_curs.fetchall()
        except Exception as e:
            print(e)
        finally:
            if result == ():
                result = [['1']]
            return result


def osp_url():
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT id, url FROM global_osp_list ORDER BY regdate DESC"
            # sql = "SELECT id, url FROM global_osp_list where id not in (SELECT osp_id FROM similar_web)"
            master_curs.execute(sql)
            result = master_curs.fetchall()
        except Exception as e:
            print(e)
        finally:
            return result


def inset_osp_global_rank(args):
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "INSERT INTO " \
                  "similar_web (`osp_id`, `url`, `global_rank`, `country_rank`, `category_rank`, `total_visits`, `top_countries`, `regdate`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            master_curs.execute(sql, (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]))
            master_conn.commit()
            print(f'similar_web: {args[0]} 업데이트 완료!')
        except Exception as e:
            print(e)
            master_conn.connect()


def check_similar_pk(osp_id, date):
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT COUNT(*)as count FROM autogreen.similar_web WHERE osp_id = %s and regdate = %s"
            master_curs.execute(sql, (osp_id, date))
            result = master_curs.fetchall()
            return result[0][0]
        except Exception as e:
            print(e)
            master_conn.connect()


def get_domain(osp_id):
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT url FROM autogreen.global_osp_list where id = %s"
            master_curs.execute(sql, (osp_id))
            result = master_curs.fetchall()
            return result[0][0]
        except Exception as e:
            print(e)
            master_conn.connect()


def check_host_url(host_url):
    result = main_data.find_one({"hostUrl": host_url})
    return result


def check_host_url_with_regex(reg, osp):
    result = main_data.find_one({'$and': [{"hostUrl": {"$regex": reg + '$'}}, {"osp": osp}]})
    return result


def replace_data(data):
    main_data.replace_one({"_id": data['_id']}, data)


def check_compare_image(compare_image):
    result = main_data.find_one({"compareImage": compare_image})
    return result


def get_cnt_title(cnt_id):
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT title FROM content_list WHERE idx = %s"
            master_curs.execute(sql, cnt_id)
            result = master_curs.fetchall()
            _result = [i[0] for i in result]
        finally:
            return _result


def get_all_cnt_title():
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT title FROM content_list WHERE main_cp = 'sbs'"
            master_curs.execute(sql)
            result = master_curs.fetchall()
            _result = [i[0] for i in result]
        finally:
            return _result


def get_keyword_title(key_id):
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT title FROM keyword WHERE idx = %s"
            master_curs.execute(sql, key_id)
            result = master_curs.fetchall()
            _result = [i[0] for i in result]
        finally:
            return _result


def cheap_query():
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        sql = "SELECT *" \
              "FROM whitelist " \
              "limit 1"
        master_curs.execute(sql)


def except_key(cnt_id):
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT k.title " \
                  "FROM keyword as k join content_list as c on c.idx = k.cnt_id " \
                  "WHERE k.state = 1 and k.type = 0 and c.main_cp = 'sbs' and k.cnt_id = %s"
            master_curs.execute(sql, cnt_id)
            result = master_curs.fetchall()
            _result = [i[0] for i in result]
        except:
            master_conn.connect()
        finally:
            return _result


def include_key(cnt_id, country):
    if ',' in country:
        country = country.split(',')[0]
    country_query = "('" + "', '".join(country) + "')"
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT k.title " \
                  "FROM keyword as k join content_list as c on c.idx = k.cnt_id " \
                  "WHERE k.state = 1 and k.type = 1 and c.main_cp = 'sbs' and k.cnt_id = %s and " \
                  f"language IN {country_query}"
            master_curs.execute(sql, cnt_id)
            result = master_curs.fetchall()
            _result = [i[0] for i in result]
        except:
            master_conn.connect()
        finally:
            return _result


def all_except_key():
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT keyword FROM except_keyword"
            master_curs.execute(sql)
            result = master_curs.fetchall()
            _result = [i[0] for i in result]
        finally:
            return _result


def get_keyword(korean=False):
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT k.title, k.cnt_id, k.idx " \
                  "FROM keyword as k join content_list as c on c.idx = k.cnt_id " \
                  "WHERE k.state = 1 and k.type = 1 and c.main_cp = 'sbs'"
            if not korean:
                sql += " and k.language != 'KR'"
            sql += " ORDER BY LENGTH(k.title) DESC"
            master_curs.execute(sql)
            result = master_curs.fetchall()
        finally:
            return result


def get_google_keyword(offset):
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT c.title, kg.cnt_id, kg.start, kg.end " \
                  "FROM keyword_google kg " \
                  "JOIN content_list c " \
                  "ON kg.cnt_id = c.idx order " \
                  "by c.regdate desc " \
                  "limit 5 offset %s"
            master_curs.execute(sql, offset)
            result = master_curs.fetchall()
        finally:
            return result


def get_google_search():
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT title FROM google_search"
            master_curs.execute(sql)
            result = master_curs.fetchall()
        finally:
            return result


def get_google_url():
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        sql = "SELECT url FROM google_check_url"
        master_curs.execute(sql)
        result = master_curs.fetchall()
        a = [i[0] for i in result]
        return a


def check_google_url(url, get_url):
    return_value = {
        'm': None
    }

    for u in get_url:
        if url.find(u) != -1:
            return_value['m'] = u

    return return_value


def google_check_title(title, keyword, cnt_id):
    return_value = ''
    a = 0
    title = title.replace(' ', '')
    keyword = keyword.replace(' ', '')

    if title.find(keyword) != -1:
        return_value = keyword
        get_del_key = except_key(cnt_id)
        if not get_del_key:
            return_value = keyword
        else:
            for d in get_del_key:
                d = d.replace(' ', '')
                if title.find(d) != -1:
                    a = a + 1
        if a != 0:
            return_value = ''

        return return_value


def return_key(korean=False):
    try:
        result = get_keyword(korean)
        return_value = {}
        for i in range(len(result)):
            key = result[i][0]
            if key in return_value:
                return_value[key].append(result[i][1])
                return_value[key].append(result[i][2])
            else:
                return_value.update({key: [result[i][1], result[i][2]]})
    finally:
        return return_value

#* 검색하지 말아야 할 키워드가 제목에 포함되어 있는지 확인함(한국거 더빙 드라마만 가져오고 싶음 아닌건 다 True)
def check_all_except_key(title):
    all_except = all_except_key()  #* mySQL DB 속 카테고리 키워드를 다 가져옴
    _list = []
    for ex in all_except:
        if title.find(ex) != -1:   #* title에 해당 키워드가 있는지 확인 -> 맞으면 True 아니면 False를 _list에 넣어 반환
            print('검출 : ' + title)
            print('전체 제외 : ' + ex)
            _list.append(True)
        else:
            _list.append(False)
    return _list


def check_title(title, keyword, match_print=True):
    return_value = {
        'm': None,
        'i': None,
        'k': None,
    }
    a = 0

    #? check_all_except_key(title) : 해당 title에 우리가 찾아야하는 keyword중 어떤 것들이 포함되었는지 True, False 값이 들어있는 리스트를 반환
    if any(check_all_except_key(title)):   #* 한국거 드라마 아닌 것들은 None으로 반환시켜줌
        return_value['m'] = None
        return return_value

    for s, p in keyword.items():           #* s = key(k.title) / p = value(k.cnt_id, k.idx)를 가져옴
        s = title_null(s)
        if title.find(s) != -1:            #* 웹사이트에서 가져온 title 제목에 keyword에 있는 title 값 있는지 확인
            if match_print:
                print('\n제목 : ' + title)
                print('검출 : ' + s)
            return_value['m'] = s          #* m : 타이틀 제목
            return_value['i'] = p[0]       #* i : cnt_id(해당 드라마 번호)
            return_value['k'] = p[1]       #* k : idx(해당 드라마 id) 
            get_except_key = except_key(p[0])       #* keyword 테이블의 cnt_id를 가지고 content_list 테이블의 idx와 비교해서 content_list 테이블의 title 값 가져옴
            if not get_except_key:         #* keyword.cnt_id == content_list.idx 인 title이 없다.
                return_value['m'] = s
                return_value['i'] = p[0]
                return_value['k'] = p[1]
            else:                          #* keyword.cnt_id == content_list.idx 인 title이 있다.
                for e in get_except_key:
                    e = e.replace(' ', '').replace('-', '').lower()     #* title ' ', '-' 제외시키기
                    if title.find(e) != -1:                             #* 웹사이트에서 가져온 title 제목에 ' ', '-' 제외한 title 값 있는지 확인 그럼 'm' None 반환
                        print('제외 : ' + e)                            
                        return_value['m'] = None
                        return return_value
            return return_value
    return return_value


def get_next_mail_type(explanation):
    if '최초 경고 메일' in explanation:
        explanation = explanation.replace('최초 경고 메일', '미응답 1회')
    elif '미응답 1회' in explanation:
        explanation = explanation.replace('1회', '2회')
    else:
        return None

    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = f"SELECT idx, explanation, title, body FROM mail_type WHERE explanation = '{explanation}'"
            master_curs.execute(sql)
            result = master_curs.fetchall()[0]
        except Exception as e:
            print(e)
        finally:
            return {
                'idx': result[0],
                'explanation': result[1],
                'title': result[2],
                'body': result[3],
            }


def get_twitok_keyword():
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT kg.cnt_id, c.title " \
                  "FROM keyword_google as kg join content_list as c on c.idx = kg.cnt_id " \
                  "WHERE kg.cp = 'sbs'"
            master_curs.execute(sql)
            result = master_curs.fetchall()
        finally:
            return result


def get_twitter_whitelist():
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT id " \
                  "FROM whitelist " \
                  "WHERE osp = 'twitter'"
            master_curs.execute(sql)
            result = master_curs.fetchall()
        finally:
            return list(map(lambda e: e[0], result))


def check_title_twitok(cnt_id, title):
    _title = title_null(title)
    catch = None
    include_keys = include_key(cnt_id, ['KR'])
    for key in include_keys:
        key = title_null(key)
        if key in _title:
            catch = key
    if not catch:
        print(_title + '\n포함 키워드 포함X')
        return False

    except_keys = except_key(cnt_id)
    for key in except_keys:
        key = title_null(key)
        if key in _title:
            print(_title + '\n제외 키워드 포함')
            return False
    return True


def get_base_img():
    with master_conn.cursor() as master_curs:
        master_conn.ping(reconnect=True)
        try:
            sql = "SELECT image " \
                  "FROM content_list " \
                  "WHERE main_cp = 'sbs' " \
                  "AND image IS NOT NULL " \
                  "AND image <> '' " \
                  "AND image NOT LIKE '%undef%' "
            # 출력 예시  -> ['abcd.jpg', 'abccde.jpg/efdg.jpg', '']
            master_curs.execute(sql)
            result = master_curs.fetchall()

            query_result = [item[0] for item in result]

            return query_result
        except Exception as e:
            print(e)


# 이미지 유사도 검사
def check_similarity(base, compare):
    # Load the VGG16 model
    model = VGG16(weights='imagenet', include_top=False)
    # Load the first image and preprocess it

    img1 = image.load_img(base, target_size=(224, 224))
    img1 = image.img_to_array(img1)
    img1 = np.expand_dims(img1, axis=0)
    img1 = preprocess_input(img1)

    # Load the second image and preprocess it
    img2 = image.load_img(compare, target_size=(224, 224))
    img2 = image.img_to_array(img2)
    img2 = np.expand_dims(img2, axis=0)
    img2 = preprocess_input(img2)

    # Extract features from the images using the VGG16 model
    features1 = model.predict(img1)
    features2 = model.predict(img2)

    # reshape the feature to be 1d
    features1 = features1.reshape(1, -1)
    features2 = features2.reshape(1, -1)

    # Calculate cosine similarity

    similarity = cosine_similarity(features1, features2)

    print("Cosine similarity:", similarity[0][0])

    return similarity[0][0]


def download_base_img(base_img, osp_path):
    if not os.path.exists(file_path + osp_path):
        os.makedirs(file_path + osp_path)
    # 포스터 다운로드
    for base in base_img:
        split_list = base.split('/')
        for split in split_list:
            r = requests.get(base_img_link + split, verify=False)

            with open(file_path + osp_path + split, 'wb') as f:
                f.write(r.content)


def get_img_base_compare(base_img, images, osp_path):
    # 수집 이미지 다운로드
    if 'http' in str(images):                           #* image 태그 src에 http가 포함 되어 있는가?
        img = requests.get(images, verify=False)        #* 있으면 그 이미지 경로를 열어서 페이지 값 가져오기
        img_value = str(uuid.uuid1())                   #* uuid를 image 이름으로 하고
        with open(file_path + osp_path + img_value + '.png',        #* 기본파일경로/크롤링사이트명/파일명.png로 생성
                  'wb') as f1:
            f1.write(img.content)                                   #* 속의 내용을 페이지 값으로 넣기
    else:
        return                                          #* 없으면 이미지 가져오지 않기
    # 이미지 유사도 검사
    for base in base_img:                               #* DB에 있는 이미지 파일 하나씩 가져오기
        split_list = base.split('/')                    #* split_list에 /로 나눈 리스트 넣기
        for split in split_list:                        
            print(f'검사 베이스 : {split}')
            print(f'비교 대상 : {images}')
            similarity = check_similarity(              #* 이미지 유사도 검사
                file_path + osp_path + split,
                file_path + osp_path + img_value + '.png') * 100
            if similarity > 40:                         #* 해당 이미지랑 맞는거 같다 그럼 해당 포스터 보내줌
                return similarity
            else:
                continue


def remove_osp_dir_image(osp_path):
    if os.path.exists(file_path + osp_path):
        for file in os.scandir(file_path + osp_path):
            os.remove(file.path)

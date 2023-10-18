from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
from copy import deepcopy
from common import get_sentiment_by_aws
from datetime import datetime

#? MongoDB와 연동하여 로그 및 콘텐츠 데이터를 관리하는 기능
class Mongo:
    #* MongoDB 서버와 연결하고, 특정 데이터베이스와 그 안의 컬렉션들에 연결
    def __init__(self, connection_string, db):
        # variable - MongoClient : pymongo 라이브러리에서 제공하는 MongoDB 서버 연결 클래스
        # variable - connection_string : MongoDB 서버에 연결하기 위한 문자열 정보(ex 서버 주소, 포트, 인증 등)
        # variable - self.client : 생성된 MongoClient 객체
        self.client = MongoClient(connection_string)
        
        # variable - self.db : DB 참조 객체
        # variable - self.client[db] : 해당 db명의 데이터베이스에 접근함
        self.db = self.client[db]

        # variable - self.log_collection : log라는 컬렉션을 참조하는 변수 선언
        # variable - self.client[db]['log'] : 해당 db에서 log라는 컬렉션 접근
        self.log_collection = self.client[db]['log']
        self.content_collection = self.client[db]['content_all']
        self.unimportant_log_collection = self.client[db]['unimportant_log']

    #* 콘텐츠 데이터를 삽입하는 기능.
    #* 중복 URL 및 키워드를 체크하여 중복이면 unimportant_log_collection에 로그를 남김.
    #* 중복이 아니면 감정 분석 결과를 추가하여 content_collection에 데이터를 삽입.
    def content_insert(self, data, log):
        # variable - prev_data : content_collection에서 주어진 URL과 키워드를 가진 데이터를 참조하는 변수(중복 URL 체크)
        prev_data = self.content_collection.find_one({'url': data['url'], 'keyword': data['keyword']})
        if prev_data:   #* prev_data가 None이 아니면
            log['type'] = 'common'
            log['position'] = '중복값 발생'
            log['log'] = '(키워드, URL)의 중복으로 값이 삽입되지 않음'
            log['created_at'] = datetime.now()
            log['url'] = data['url']
            # function : 중복된 값에 대한 로그 정보를 'unimportant_log' 컬렉션에 삽입
            # function - deepcopy : log 딕셔너리의 복사본을 생성하여 원본 log의 변경 없이 사용할 수 있게 합
            self.unimportant_log_insert(deepcopy(log))
            return
        # variable - text : 제목(title)과 내용(contents)을 합친 문자열을 생성합니다. 만약 contents가 없다면 제목만을 사용
        text = data['title'] + data['contents'] if data['contents'] else data['title']
        
        #? get_sentiment_by_aws 함수 : text의 첫 500자에 대한 감정 분석 결과를 가져옵니다.
        # variable - data['sentiment'] : 감정분석 결과 저장
        data['sentiment'] = get_sentiment_by_aws(text[:500])
        self.content_collection.insert_one(data)

    #* 중요한 로그를 log_collection에 삽입
    def log_insert(self, data):
        try:
            print(data)
            self.log_collection.insert_one(data)
        except Exception as e:
            print(e)

    #* 중요하지 않은 로그를 unimportant_log_collection에 삽입
    def unimportant_log_insert(self, data):
        try:
            self.unimportant_log_collection.insert_one(data)
        except Exception as e:
            print(e)

#* 실행 환경(env)에 따라 적절한 MongoDB 연결 문자열을 가져와서 Mongo 객체를 생성하고 반환
def get_mongo_client(env):
    if env == 'test':
        connection_string = getenv('MONGO_TEST_CONNECTION') #! 테스트용 몽고DB 반환
    else:
        connection_string = getenv('MONGO_CONNECTION') #! 실제 프로젝트 몽고DB 반환

    return Mongo(connection_string=connection_string, db='companyboard')


# 배포할 때 여기 수정 # .env 파일에서 환경 변수를 로드
load_dotenv()
# 테스트 환경 : test
# 실제 환경 : test 아닌 아무거나 deploy
mongo_client = get_mongo_client(getenv('MODE'))
print('현재의 MODE:', getenv('MODE'))

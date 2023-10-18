
# variable - datetime : 날짜와 시간 관련 기능 제공
# variable - load_dotenv, getenv : 환경 변수를 로드하고 조회
from db.mysql_interface import MysqlInterface
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

#* MySQL 데이터베이스와의 상호 작용을 처리
class CompanyBoardMysql(MysqlInterface):

    #* 주어진 영화 제목(content)에 대한 예외 키워드 리스트를 데이터베이스에서 가져와 반환
    def get_except_keyword(self, content):
        # variable - connection_object : 데이터베이스 연결 풀에서 연결 객체를 가져와 MySQL 데이터베이스에 연결을 생성하는 객체
        connection_object = self.connection_pool.get_connection()
        # variable - cursor : SQL 쿼리를 실행하고 결과를 가져오는 데 사용되는 커서 객체
        cursor = connection_object.cursor() # 새 커서 객체를 생성
        # 해석 : except_keyword 테이블에서 movie 열 값이 주어진 content 값과 일치하는 keyword를 선택하는 SQL 쿼리
        sql = "SELECT keyword FROM except_keyword WHERE company = %s"

        # function: sql 변수에 저장된 SQL 쿼리를 실행하며, %s 플레이스홀더는 content 값으로 대체
        cursor.execute(sql, [content])
        # function: cursor.fetchall()를 호출하여 SQL 쿼리의 결과를 모두 가져와 result에 저장
        result = cursor.fetchall()

        # function: 커서와 데이터베이스 연결을 종료
        cursor.close()
        connection_object.close()

        #* 각 결과 튜플의 첫 번째 항목(키워드)만을 추출하여 리스트로 변환
        return list(map(lambda x: x[0], result))

    #* 키워드 인덱스를 기반으로 필수 키워드를 조회
    def get_essential_keyword(self, keyword_idx):
        # variable - connection_object : 데이터베이스 연결 풀에서 연결 객체를 가져와 MySQL 데이터베이스에 연결을 생성하는 객체
        connection_object = self.connection_pool.get_connection()
        # variable - cursor : SQL 쿼리를 실행하고 결과를 가져오는 데 사용되는 커서 객체
        cursor = connection_object.cursor()
        # 해석 : essential_keyword 테이블에서 주어진 keyword_idx 값과 일치하는 keyword 값을 조회
        sql = "SELECT keyword FROM essential_keyword WHERE keyword_idx = %s"
        
        # function: sql 변수에 저장된 SQL 쿼리를 실행하며, %s 플레이스홀더는 keyword_idx 값으로 대체
        cursor.execute(sql, [keyword_idx])
        # function: cursor.fetchall()를 호출하여 SQL 쿼리의 결과를 모두 가져와 result에 저장
        result = cursor.fetchall()

        # function: 커서와 데이터베이스 연결을 종료
        cursor.close()
        connection_object.close()

        #* 각 결과 튜플의 첫 번째 항목(키워드)만을 추출하여 리스트로 변환
        return list(map(lambda x: x[0], result))

    #* 현재 날짜가 시작 날짜와 종료 날짜 사이에 있는 영화의 키워드를 조회, 페이징 기능 제공
    # variable - size: 조회하려는 레코드의 개수를 나타냅니다.
    # variable - offset: 어디서부터 레코드를 조회할 것인지의 시작점을 나타내는 값
    def get_keyword_limit(self, size, offset):
        # variable - connection_object : 데이터베이스 연결 풀에서 연결 객체를 가져와 MySQL 데이터베이스에 연결을 생성하는 객체
        connection_object = self.connection_pool.get_connection()
        # variable - cursor : SQL 쿼리를 실행하고 결과를 가져오는 데 사용되는 커서 객체
        # variable            dictionary=True 옵션은 결과를 사전 형태로 반환하도록 합니다.
        cursor = connection_object.cursor(dictionary=True)

        # 해석 : 현재 시간이 start_date와 end_date 사이에 있는 레코드만을 size만큼 결과 제한하고, offset만큼 시작점 건너뜀
        sql = """
        SELECT idx, company, cp_id, keyword
        FROM keyword k
        JOIN company c ON k.company = c.company_name
        LIMIT %s offset %s
        """
        # function: sql 변수에 저장된 SQL 쿼리를 실행하며, size와 offset * size를 플레이스홀더에 전달
        cursor.execute(sql, [size, offset * size])
        # function: cursor.fetchall()를 호출하여 SQL 쿼리의 결과를 모두 가져와 result에 저장
        result = cursor.fetchall()

        # function: 커서와 데이터베이스 연결을 종료
        cursor.close()
        connection_object.close()

        #* 결과 반환
        return result

    #* 특정 OSP(Online Service Provider)의 마지막 크롤링 날짜를 현재 시간으로 업데이트
    def update_osp_crawling_date(self, osp):
        connection_object = self.connection_pool.get_connection()
        cursor = connection_object.cursor()
        sql = """
        UPDATE osp_list 
        SET osp_end_date = %s
        WHERE osp = %s
        """
        cursor.execute(sql, [datetime.now(), osp])
        cursor.close()
        connection_object.close()


# mysql
load_dotenv()
companyBoardMysql = CompanyBoardMysql(pool_name='companyboardtest',
                                    pool_size=5,
                                    host=getenv('MYSQL_HOST'),
                                    port=getenv('MYSQL_PORT'),
                                    database=getenv('MYSQL_NAME'),
                                    user=getenv('MYSQL_USER'),
                                    password=getenv('MYSQL_PASSWORD'))

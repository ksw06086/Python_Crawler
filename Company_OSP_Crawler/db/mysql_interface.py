# variable - Error : 데이터베이스 연결시 발생할 수 있는 에러 클래스
# variable - pooling : 연결 풀링(pooling)에 관련된 클래스
# variable - abc : 추상 베이스 클래스를 정의하기 위한 모듈
from mysql.connector import Error
from mysql.connector import pooling
import abc

#* 추상 베이스 클래스(abc.ABCMeta를 메타클래스로 사용)
class MysqlInterface(metaclass=abc.ABCMeta):

    # function - constructor : MySQL 연결 풀을 초기화
    def __init__(self, pool_name, pool_size, host, port, database, user, password):

        # variable - pool_name : 연결 풀을 구별하는 데 사용
        # variable - pool_size : 동시에 몇 개의 연결을 풀에서 사용할 수 있는지를 결정
        # variable - host : 데이터베이스 서버의 호스트 이름 또는 IP 주소
        # variable - port : 데이터베이스 서버의 포트 번호
        # variable - database : 연결할 데이터베이스의 이름
        # variable - user : 데이터베이스에 연결하기 위한 사용자 이름
        # variable - password : 데이터베이스에 연결하기 위한 사용자의 비밀번호
        try:
            # variable - self.connection_pool : 객체의 연결 풀을 나타내는 속성
            self.connection_pool = pooling.MySQLConnectionPool(pool_name=pool_name,
                                                               pool_size=pool_size,
                                                               pool_reset_session=True,
                                                               host=host,
                                                               port=port,
                                                               database=database,
                                                               user=user,
                                                               password=password)
            print("Printing connection pool properties ")
            print("Connection Pool Name - ", self.connection_pool.pool_name)
            print("Connection Pool Size - ", self.connection_pool.pool_size)

        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    @abc.abstractmethod
    def get_except_keyword(self, content):
        """Osp_list select 구현"""
        raise NotImplemented

    @abc.abstractmethod
    def get_essential_keyword(self, keyword_idx):
        """cp_id select 구현"""
        raise NotImplemented

    @abc.abstractmethod
    def get_keyword_limit(self, size, offset):
        """keyword select 구현"""
        raise NotImplemented

    @abc.abstractmethod
    def update_osp_crawling_date(self, osp):
        """Osp 마지막 크롤링 날짜 구현"""
        raise NotImplemented






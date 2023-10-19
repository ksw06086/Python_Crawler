from sys import argv

from osp_init import init_by_osp
from db.mysql_service import companyBoardMysql
import traceback
osp_name = "유튜브"#argv[1]
try:
    size = argv[2]
    offset = argv[3]
except:
    size = 20
    offset = 1


def main(crawler):
    print(companyBoardMysql.get_keyword_limit(size=20, offset=0))
    for row in companyBoardMysql.get_keyword_limit(size=20, offset=0):
        print(companyBoardMysql.get_except_keyword(row['company']))
        print(companyBoardMysql.get_essential_keyword(row['idx']))
        crawler.set_metadata(keyword=row['keyword'], company=row['company'], cp_id=row['cp_id'],
                             except_keywords=companyBoardMysql.get_except_keyword(row['company']),
                             essential_keywords=companyBoardMysql.get_essential_keyword(row['idx']))
        crawler.start_crawling()
    
    # companyBoardMysql.update_osp_crawling_date(osp_name)


if __name__ == '__main__':
    osp = init_by_osp(osp_name)()
    print(f'==<{osp_name}>==')
    # while True:
    try:
        main(osp)
    except Exception as e:
        print(f'{osp_name} 크롤러 메인 이슈 발생!\n{e}\n{traceback.format_exc()}')

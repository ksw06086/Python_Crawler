from classes.pageCrawler import PageCrawler


class Dvdprime(PageCrawler):
    def format_date(self):
        # 해석 : write_date 값 내에 'at' 문자열이 포함되어 있는지 확인
        if 'at' in self.data.write_date:
            # 해석 : write_date 값을 ' at ' 문자열을 기준으로 분리하고, 그 결과로 얻은 리스트의 두 번째 요소(인덱스 1)를 write_date 값으로 다시 설정
            #        'at' 앞의 날짜 정보는 제거되고 시간 정보만 남게 됨
            self.data.write_date = self.data.write_date.split(' at ')[1]
        # 해석 : 바뀐 날짜 데이터로 포멧팅함
        super().format_date()
            
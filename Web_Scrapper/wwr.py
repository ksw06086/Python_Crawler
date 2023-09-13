
from requests import get
from bs4 import BeautifulSoup

def extract_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?utf8=✓&term="
    search_term = keyword

    response = get(f"{base_url}{search_term}")
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        #? class_="jobs" => 함수에서 매개변수 값 넣는 순서 신경 안쓰기 위해 매개변수명 앞에 붙여줌(ex> class_가 4번째 매개변수여도 이름 지정 해주면 작동함)
        jobs = soup.find_all('section', class_ = "jobs")
        for job_section in jobs:
            #? job_section 텍스트 중에서 li태그이고 class="feature" 인 텍스트를 가져와라
            job_posts = job_section.find_all('li', class_="feature")
            for post in job_posts:
                #? post 텍스트에서 <a> 태그 추출
                anchors = post.find_all('a')
                #? <a> 태그 중 직업 관련 텍스트만 있는 <a>태그만 가져옴
                anchor = anchors[1]
                #? 가져온 <a> 태그의 href 속성 URL 가져옴
                link = anchor['href']
                #* anchor 리스트에 3개가 들어있어서 아래처럼 하면 3개의 변수에 순서대로 들어감(단, 변수의 개수와 리스트 내용의 개수가 같아야 함)
                company, kind, region = anchor.find_all('span', class_="company")
                title = anchor.find('span', class_="title")
                job_data = {
                    'link' : f"https://weworkremotely.com{link}",
                    'company': company.string,
                    'region': region.string,
                    'position': title.string
                }
                results.append(job_data)
        return results

    
from bs4 import BeautifulSoup

# 예시 HTML 코드
html = """
<html>
<head>
    <title>Beautiful Soup 예제</title>
</head>
<body>
    <a href="https://example.com">
        <font>
            <font>
                이 텍스트를 가져옵니다.
            </font>
        </font>
    </a>
</body>
</html>
"""

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(html, 'html.parser')

# 모든 <a> 태그를 찾습니다.
a_tag = soup.find('a')

# 중첩된 <font> 태그 안의 텍스트를 가져옵니다.
print(a_tag.get_text().strip())
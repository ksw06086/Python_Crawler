
# * 웹사이트에 request 요청을 보내는 모듈
from requests import get

# * URL Formatting
websites = (
    "https://google.com",
    "https://airbnb.com",
    "https://twitter.com",
    "https://facebook.com"
)

results = {}

for website in websites:
    if not website.startswith("https://"):
        website = f"https://{website}"

    #? response를 return 해줌
    response = get(website)
    if response.status_code >= 500:
        results[website] = "ERROR"
    if response.status_code >= 400:
        results[website] = "FAILED"
    if response.status_code >= 300:
        results[website] = "REDIRECT"
    elif response.status_code >= 200:
        results[website] = "OK"
    else:
        results[website] = "FAILED"

print(results)
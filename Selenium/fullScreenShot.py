import time, os, pyglet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time_def import *
from PIL import Image, ImageFont, ImageDraw

# 현재 파일 경로
current_path = os.path.dirname(os.path.abspath(__file__))

def getResource(url):
    pyglet.resource.path.append(os.path.join(current_path, 'resource', 'font', 'black_font', 'url_font.fnt').replace('\\', '\\\\'))

    utckTime = DateHelper.UTCKTime()
    windowTime = DateHelper.windowTime()

    print(os.path.join(current_path, 'resource', 'font', 'black_font', 'url_font.fnt').replace('\\', '\\\\'))

    # 브라우저 바
    urlBar = Image.open(os.path.join(current_path, 'resource', 'url_bar.png'))
    # 브라우저 바 폰트 로드
    urlFont = pyglet.font.load('Segoe UI Variable Text')
    
    # Draw 객체 생성
    urlDraw = ImageDraw.Draw(urlBar)
    # URL 수정
    modified_url = url.replace('https://', '').replace('http://', '').replace('www.', '').replace('com//', 'com/')
    # 이미지 위에 텍스트 인쇄
    urlDraw.text((270, 28), modified_url, font=urlFont, fill="black")

    #윈도우 바
    windowBar = Image.open(os.path.join(current_path, 'resource', 'window_bar.png'))
    windowFont = ImageFont.truetype(os.path.join(current_path, 'resource', 'font', 'white_font', 'time_font.fnt'))
    # Draw 객체 생성
    windowDraw = ImageDraw.Draw(windowBar)
    # 이미지 위에 세 번 텍스트 인쇄
    windowDraw.text((windowBar.width - 125, 14), windowTime[0], font=windowFont, fill="white")
    windowDraw.text((windowBar.width - 74, 12), windowTime[1], font=windowFont, fill="white")
    windowDraw.text((windowBar.width - 145, 37), windowTime[2], font=windowFont, fill="white")

    #UTCK 시계
    utck = Image.open(os.path.join(current_path, 'resource', 'utck.png'))
    utckDateFont = ImageFont.truetype(os.path.join(current_path, 'resource', 'font', 'green_font', 'date_font.fnt'))
    utckTimeFont = ImageFont.truetype(os.path.join(current_path, 'resource', 'font', 'green_font', 'time_font.fnt'))
    # Draw 객체 생성
    utckDraw = ImageDraw.Draw(utck)
    # 이미지 위에 두 번 텍스트 인쇄
    utckDraw.text((120, 155), utckTime[0], font=utckDateFont, fill="green")
    utckDraw.text((150, 173), utckTime[1], font=utckTimeFont, fill="green")

    return {
        'urlBar': urlBar,
        'windowBar': windowBar,
        'utck': utck,
    }

def editImage(resourceImage, fileName, utckUp):
    # 스크린샷 이미지 로드
    page = Image.open(os.path.join(current_path, 'screenshot.png'))

    # 리사이즈
    resourceImage['urlBar'] = resourceImage['urlBar'].resize((page.width, int(page.height * (resourceImage['urlBar'].height / resourceImage['urlBar'].width))), Image.ANTIALIAS)
    resourceImage['windowBar'] = resourceImage['windowBar'].resize((page.width, int(page.height * (resourceImage['windowBar'].height / resourceImage['windowBar'].width))), Image.ANTIALIAS)
    resourceImage['utck'] = resourceImage['utck'].resize((int(page.width / 4), int(page.height * (resourceImage['utck'].height / resourceImage['utck'].width))), Image.ANTIALIAS)

    # 새로운 이미지 생성
    newImage = Image.new("RGB", (page.width, page.height + resourceImage['urlBar'].height + resourceImage['windowBar'].height), (255, 255, 255))
    
    # 이미지 합성
    newImage.paste(page, (0, resourceImage['urlBar'].height))
    utck_y = 50 if utckUp else resourceImage['urlBar'].height + page.height - 210
    newImage.paste(resourceImage['utck'], (page.width - resourceImage['utck'].width - 5, utck_y), resourceImage['utck'])
    newImage.paste(resourceImage['urlBar'], (0, 0), resourceImage['urlBar'])
    newImage.paste(resourceImage['windowBar'], (0, newImage.height - resourceImage['windowBar'].height), resourceImage['windowBar'])

    # 이미지 저장
    output_path = os.path.join(current_path, f"{DateHelper.fileName(False)}", f"{fileName}.png")
    newImage.save(output_path, quality=100)

    return fileName + '.png'

def full_screenshot(driver, url, output_path):
    driver.get(url)
    time.sleep(1)  # Give the page some time to load
    
    total_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script(f"window.scrollTo(0, {total_height});")
        time.sleep(0.5)
        print(f"total_height : {total_height}");
        print(f"driver_height : {driver.execute_script('return document.documentElement.scrollHeight')}");
        if total_height == driver.execute_script("return document.documentElement.scrollHeight"):
            break
        total_height = driver.execute_script("return document.documentElement.scrollHeight")
        

    driver.set_window_size("1520", total_height)

    time.sleep(1)
    driver.save_screenshot(output_path)

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

cp = 'sbs'
url = "https://m.blog.naver.com/ppongmangchi/223216997947"
output_path = "screenshot.png"
full_screenshot(driver, url, output_path)
resource = getResource(url)
filenameURL = editImage(resource, f"{'blog'}_{DateHelper.fileName}", cp == 'sbs')
print(filenameURL)
driver.quit()
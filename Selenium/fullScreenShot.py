import time, os, pyglet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time_def import *
from PIL import Image
from fntParse import parse_fnt, render_text_to_image

# 현재 파일 경로
current_path = os.path.dirname(os.path.abspath(__file__))

def getResource(url):
    pyglet.resource.path.append(os.path.join(current_path, 'resource', 'font', 'black_font', 'url_font.fnt').replace('\\', '\\\\'))

    utckTime = DateHelper.UTCKTime()
    windowTime = DateHelper.windowTime()

    print(os.path.join(current_path, 'resource', 'font', 'black_font', 'url_font.fnt').replace('\\', '\\\\'))

    #* 브라우저 바
    urlBar = Image.open(os.path.join(current_path, 'resource', 'url_bar.png'))
    
    # URL 수정
    modified_url = url.replace('https://', '').replace('http://', '').replace('www.', '').replace('com//', 'com/')

    # 브라우저 바 폰트 로드
    url_fnt_path = os.path.join(current_path, 'resource', 'font', 'black_font', 'url_font.fnt')
    url_png_path = os.path.join(current_path, 'resource', 'font', 'black_font', 'url_font_0.png')
    # 브라우저 바 폰트 파싱
    url_char_data = parse_fnt(url_fnt_path)
    # 브라우저 바 text 이미지 변환
    url_text_img = render_text_to_image(modified_url, url_char_data, url_png_path)

    # 브라우저 바 png, 브라우저 바 폰트 png 병합
    urlBar.paste(url_text_img, (265, 32), url_text_img)  # (270, 28)은 텍스트를 배치할 좌표입니다.
    
    # #* 윈도우 바
    # windowBar = Image.open(os.path.join(current_path, 'resource', 'window_bar.png'))

    # # 윈도우 바 폰트 로드
    # window_fnt_path = os.path.join(current_path, 'resource', 'font', 'white_font', 'time_font.fnt')
    # window_png_path = os.path.join(current_path, 'resource', 'font', 'white_font', 'time_font_0.png')
    # # 윈도우 바 폰트 파싱
    # window_char_data = parse_fnt(window_fnt_path)
    # # 윈도우 바 text 이미지 변환
    # windowTime0_text_img = render_text_to_image(windowTime[0], window_char_data, window_png_path)
    # windowTime1_text_img = render_text_to_image(windowTime[1], window_char_data, window_png_path)
    # windowTime2_text_img = render_text_to_image(windowTime[2], window_char_data, window_png_path)

    # # 윈도우 바 png, 윈도우 바 폰트 png 병합
    # windowBar.paste(windowTime0_text_img, (windowBar.size[0] - 135, 12), windowTime0_text_img)
    # windowBar.paste(windowTime1_text_img, (windowBar.size[0] - 84, 16), windowTime1_text_img)
    # windowBar.paste(windowTime2_text_img, (windowBar.size[0] - 145, 43), windowTime2_text_img)

    #* UTCK 시계
    utck = Image.open(os.path.join(current_path, 'resource', 'utck.png'))

    # UTCK 시계 폰트 로드
    utckDate_fnt_path = os.path.join(current_path, 'resource', 'font', 'green_font', 'date_font.fnt')
    utckDate_png_path = os.path.join(current_path, 'resource', 'font', 'green_font', 'date_font_0.png')
    utckTime_fnt_path = os.path.join(current_path, 'resource', 'font', 'green_font', 'time_font.fnt')
    utckTime_png_path = os.path.join(current_path, 'resource', 'font', 'green_font', 'time_font_0.png')
    # UTCK 시계 폰트 파싱
    utckDate_char_data = parse_fnt(utckDate_fnt_path)
    utckTime_char_data = parse_fnt(utckTime_fnt_path)
    # UTCK 시계 text 이미지 변환
    utckDate_text_img = render_text_to_image(utckTime[0], utckDate_char_data, utckDate_png_path, 3)
    utckTime_text_img = render_text_to_image(utckTime[1], utckTime_char_data, utckTime_png_path, 10)

    # UTCK 시계 png, UTCK 시계 폰트 png 병합
    utck.paste(utckDate_text_img, (120, 161), utckDate_text_img)
    utck.paste(utckTime_text_img, (135, 205), utckTime_text_img)

    return {
        'urlBar': urlBar,
        'utck': utck,
        # 'windowBar': windowBar,
    }

def editImage(resourceImage, fileName):
    # 스크린샷 이미지 로드
    page = Image.open(os.path.join(current_path, 'screenshot.png'))

    # 리사이즈
    resourceImage['urlBar'] = resourceImage['urlBar'].resize((page.width, int(page.height * (resourceImage['urlBar'].height / resourceImage['urlBar'].width))), Image.LANCZOS)
    resourceImage['utck'] = resourceImage['utck'].resize((int(page.width / 4), int(page.height * (resourceImage['utck'].height / resourceImage['utck'].width) / 4)), Image.LANCZOS)
    # resourceImage['windowBar'] = resourceImage['windowBar'].resize((page.width, int(page.height * (resourceImage['windowBar'].height / resourceImage['windowBar'].width))), Image.LANCZOS)
    
    # 새로운 이미지 생성
    # newImage = Image.new("RGB", (page.width, page.height + resourceImage['urlBar'].height + resourceImage['windowBar'].height), (255, 255, 255))
    newImage = Image.new("RGB", (page.width, page.height + resourceImage['urlBar'].height), (255, 255, 255))
    
    # 이미지 합성
    newImage.paste(page, (0, resourceImage['urlBar'].height))
    utck_y = resourceImage['urlBar'].height + page.height - 140
    newImage.paste(resourceImage['utck'], (page.width - resourceImage['utck'].width, utck_y), resourceImage['utck'])
    newImage.paste(resourceImage['urlBar'], (0, 0), resourceImage['urlBar'])
    # newImage.paste(resourceImage['windowBar'], (0, newImage.height - resourceImage['windowBar'].height), resourceImage['windowBar'])

    # 디렉토리 있는지 확인 후 없으면 생성
    directory_path = current_path.replace('\\', '/') + f"/{DateHelper.fileName(False)}"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # 이미지 저장
    output_path = directory_path + f"/{fileName}.png"
    # newImage.show() 
    newImage.save(output_path, quality=100)

    return fileName + '.png'

def full_screenshot(driver, url, output_path):
    driver.get(url)
    time.sleep(1)  # Give the page some time to load
    
    # total_height = driver.execute_script("return document.documentElement.scrollHeight")
    # while True:
    #     driver.execute_script(f"window.scrollTo(0, {total_height});")
    #     time.sleep(0.5)
    #     print(f"total_height : {total_height}");
    #     print(f"driver_height : {driver.execute_script('return document.documentElement.scrollHeight')}");
    #     if total_height == driver.execute_script("return document.documentElement.scrollHeight"):
    #         break
    #     total_height = driver.execute_script("return document.documentElement.scrollHeight")
        

    driver.set_window_size("884", "984")

    # time.sleep(1)
    driver.save_screenshot(output_path)


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.xigayy.com/dianshiju/hanju/243868/"
output_path = current_path.replace('\\', '/') + "/screenshot.png"
full_screenshot(driver, url, output_path)
resource = getResource(url)
filenameURL = editImage(resource, f"{'blog'}_{DateHelper.fileName()}")
driver.quit()
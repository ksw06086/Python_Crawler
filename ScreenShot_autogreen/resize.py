import time, os, pyglet, subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time_def import *
from PIL import Image
from fntParse import parse_fnt, render_text_to_image
from io import BytesIO

# 현재 파일 경로
current_path = os.path.dirname(os.path.abspath(__file__))

def compress_with_pngquant(pil_image):
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    buffer.seek(0)
    
    # pngquant subprocess with stdin and stdout
    process = subprocess.Popen(["C:\\BackDev\\pngquant-windows\\pngquant\\pngquant.exe", '-', '--quality', '60-80'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = process.communicate(buffer.getvalue())
    
    compressed_buffer = BytesIO(stdout)
    compressed_image = Image.open(compressed_buffer)
    return compressed_image

directory_path = current_path.replace('\\', '/') + f"/{DateHelper.fileName(False)}"
filenames = [
    "148c_20231006145218VL.png",
    "148c_20231006150339WK.png",
    "doramasqueen_20231006150330eC.png",
    "heibobo_20231006150314Fi.png",
    "heibobo_20231006150332hQ.png",
    "heibobo_20231006150336bG.png",
    "heibobo_20231006150344uq.png",
    "koredizileri.tv_20231006145222vu.png",
    "koredizileri.tv_20231006145225bC.png",
]
for filename in filenames:
    print("파일명 : " + filename)
    output_path = directory_path + f"/0_{filename}"
    newImage = Image.open(os.path.join(current_path, filename))
    newImage = compress_with_pngquant(newImage)
    newImage.save(output_path, optimize=True)
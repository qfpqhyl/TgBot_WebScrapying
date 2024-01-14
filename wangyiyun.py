from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import requests


def download_music(music_link, music_name):
    # 发送GET请求
    response = requests.get(music_link)

    # 如果请求成功，将内容写入文件
    if response.status_code == 200:
        with open(music_name, 'wb') as f:
            f.write(response.content)
        print(f"音乐 {music_name} 下载成功！")
    else:
        print(f"音乐 {music_name} 下载失败！")


def get_music_link(music_name):
    # 设置Selenium
    s = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")  # 如果你不需要浏览器界面，可以启用无头模式
    driver = webdriver.Chrome(service=s, options=options)

    url = f"https://dev.iw233.cn/Music1/?name={music_name}&type=kugou"
    driver.get(url)

    try:
        # 显式等待，等待页面上出现.mp3链接
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href$='.mp3']")))
    except TimeoutException:
        print("未找到")
        return None, None

    # 获取页面源代码
    page_source = driver.page_source

    # 使用正则表达式匹配.mp3链接和音乐名称
    music_link_and_name = re.search(
        r'(http.*\.mp3)" download="(.*\.mp3)', page_source)

    driver.quit()

    # 如果找到了链接和音乐名称，返回链接和音乐名称，否则返回None
    if music_link_and_name:
        music_link = music_link_and_name.group(1)
        music_name = music_link_and_name.group(2)
        return music_link, music_name
    else:
        return None, None

# music_link, music_name = get_music_link("秋风飘起黄叶落")
# if music_link and music_name:
#     print("音乐链接：", music_link)
#     print("音乐名称：", music_name)
#     download_music(music_link, music_name)

import base64
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle
import time

# 初始化浏览器
driver = webdriver.Chrome()

def fetch_item_info(driver, item_element):
    # 初始化一个字典来存储信息
    item_info = {}
    title_element = item_element.find_element(By.CSS_SELECTOR, '[class*="Title--title"] span')
    title_str = title_element.text
    item_info['title'] = title_str

    img_elements = item_element.find_elements(By.CSS_SELECTOR, '[class*="MainPic--mainPicWrapper"] img')
    img_src = None
    for img_element in img_elements:
        img_url = img_element.get_attribute('src')
        if img_url:
            img_src = img_url
            break
    if img_src:
        item_info['img_src'] = img_src

    return item_info

def scroll_down():
    for i in range(0, driver.execute_script("return document.body.scrollHeight"), 10):
        driver.execute_script(f"window.scrollTo(0, {i});")

try:
    # 打开淘宝首页
    driver.get("https://www.taobao.com")

    # 加载cookie
    with open("cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

    # 刷新页面以确保cookie生效
    driver.refresh()
    time.sleep(1) 

    # 继续执行你的爬虫任务
    search_box = driver.find_element(By.CSS_SELECTOR, "input.rax-textinput")
    search_box.send_keys("手机")
    search_box.send_keys(Keys.RETURN)

    time.sleep(5)
    scroll_down()
    items = driver.find_elements(By.CSS_SELECTOR, '[class*="Card--doubleCardWrapper"]')

    for i, item in enumerate(items):
        print(f"处理商品 {i + 1}")
        try:
            item_info = fetch_item_info(driver, item)
            # TODO: download images
            # if 'img_src' in item_info:
            #     img_data = requests.get(item_info['img_src']).content
            #     filename = item_info['title']
            #     _, ext = os.path.splitext(item_info['img_src'])
            #     img_name = f"{filename}{ext}"
            #     if not os.path.exists('images'):
            #         os.mkdir('images')
            #     with open(f'images/{img_name}', 'wb') as f:
            #         f.write(img_data)
            #     item_info['image'] = img_name
            print(item_info)
        except Exception as e:
            print(f"Error fetching item info: {e}")
finally:
    driver.quit()
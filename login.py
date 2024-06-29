from selenium import webdriver
import pickle
import time

# 初始化浏览器
driver = webdriver.Chrome()

try:
    # 打开淘宝首页
    driver.get("https://login.taobao.com")

    # 手动登录淘宝，等待用户完成登录
    print("请手动登录淘宝...")
    time.sleep(60)  # 等待用户登录，调整时间让用户有足够的时间登录

    # 登录完成后保存cookie到本地文件
    cookies = driver.get_cookies()
    with open("cookies.pkl", "wb") as file:
        pickle.dump(cookies, file)
    print("Cookie已保存到文件")

finally:
    driver.quit()
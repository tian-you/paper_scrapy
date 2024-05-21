"""
selenium版本论文下载测试版本，测试阶段中，暂未完全实现所有功能。
"""
import re
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import TimeoutException
from selenium.webdriver import ChromeOptions, Keys
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from colorama import Fore, Back, Style, init
import random
import os

# 使用代理
# PROXY = "172.21.6.98:20170"  # 代理IP地址
option = ChromeOptions()
# option.add_argument(f'--proxy-server={PROXY}')

"""
禁用GPU加速外，还添加了--log-level=3参数来禁用控制台输出。
--log-level=3参数将日志级别设置为最低，从而减少控制台输出。
"""
cookie = 'ipCheck=221.221.237.26; fp=1f515014881b2bc503cff913553c2554; AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg=1; s_ecid=MCMID%7C79311360846624169561888550810218726611; AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg=359503849%7CMCIDTS%7C19672%7CMCMID%7C79311360846624169561888550810218726611%7CMCAAMLH-1700234732%7C11%7CMCAAMB-1700234732%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1699637132s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.1; s_cc=true; cto_bundle=lRGThV9JSVh6MFJtWjVPTWUwOHclMkJRcFRSWmJEdjhaN2VkdEdCMGNMdWJQQSUyRkV1bG1PcWtXNnlIeUdBcDN4N1JSWXZkSXRwTENvUVhnQmVEWDFrV3lvVHdJamlseGNBTkk2Wkd5UDBTRW9nSHFuN3pxRW1qY2o4WklJQ21MSjZDbmFYJTJCZlVOVU4lMkI0cHpmbjdrUTdGSnJMSklVZyUzRCUzRA; TS01b03060=012f350623f7c080611b82d3dbaa2f4385b2d580ac8c128528e92bf3861ed216869f6d9bc7ee77f21aeee084faf4c8af6f143eb75d; JSESSIONID=An-5276FsnNkbZv5DI9c_xlI5Q6IlbEuRyOpp611c-8iP1-66SCU!630652578; ERIGHTS=b7f5RorcrKUA7TYW9CEuNpFtA2VfFcx2Bj-18x2dE5Irby2nYqrUqsfwLWyUjgx3Dx3Ddc0WnjoaWzE2Kd8QrHx2FsVAx3Dx3D-gdpPDF74rjhVhbSezWo23Ax3Dx3D-hAF6CbSbyWBiTg9Gw04M9Ax3Dx3D; WLSESSION=203580044.20480.0000; ipList=221.221.237.26; __gads=ID=5fdd2cf21c045246:T=1699629931:RT=1699630270:S=ALNI_Ma_y1sw5JT_Hh_fgQqeYUOzZNRePQ; s_sq=%5B%5BB%5D%5D; xpluserinfo=eyJpc0luc3QiOiJ0cnVlIiwiaW5zdE5hbWUiOiJCRUlKSU5HIFVOSVZFUlNJVFkgT0YgVEVDSE5PTE9HWSIsInByb2R1Y3RzIjoiSUVMfFZERXxOT0tJQSBCRUxMIExBQlN8In0=; seqId=12601; TSaeeec342027=080f8ceb8aab200021fba01b53350c54869224d0de0000ee56b24480b5ccddf8461dc9a6ac596a530837aa6cc11130003d564816ebae3f0e5978155b67df160e2668631771ec421e2094bd3b9062497ad0c2def5a7e3e465357ca25384e95bd4; utag_main=v_id:018bb9d69c97003c10601a3b02a80506f002b06700aee$_sn:1$_se:7$_ss:0$_st:1699632094083$ses_id:1699629931672%3Bexp-session$_pn:4%3Bexp-session$vapi_domain:ieeexplore.ieee.org'

# 将Cookie字符串转换为字典
cookie_dict = {}
items = cookie.split('; ')
for item in items:
    key, value = item.split('=')
    cookie_dict[key] = value
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
option.add_experimental_option('prefs', {
    "download.default_directory": r'G:\PyCharm Community Edition 2023.2.1\project\paper',  # Change default directory for downloads
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
})
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument("--disable-blink-features")
option.add_argument("--disable-blink-features=AutomationControlled")
option.add_argument('--disable-gpu')  # 似乎能避免一些bug
option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片提升运行速度
option.add_argument('log-level=3')  # 禁用大量日志信息滚动输出
# option.add_argument("--headless")  # 启用无头模式
# option.add_argument('--window-size=1920x1080')  # or whatever resolution you want
driver = webdriver.Chrome(options=option)
# driver.maximize_window()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

# 原始文件名列表，另一个是新文件名列表
original_names = []

# 进入springer期刊官网，
driver.get('https://lib.bjut.edu.cn/info/1210/1216.htm')
driver.find_element(By.XPATH, '//*[@id="vsb_content_2"]/div/div/p[10]/a').click()
# 输入账号
sleep(2)
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys('S202374132')
sleep(2)
# 输入密码
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('Zhang123456789!')
# 点击登录
driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/form/div[5]/button').click()
# 点击同意
driver.find_element(By.XPATH, '/html/body/form/div/div[2]/p[2]/input[2]').click()
# 点击广告
# driver.find_element(By.XPATH, '//*[@id="home-page"]/section/div/div[2]/button[1]').click()
list1 = ['Fast Large-Scale Honest-Majority MPC for Malicious Adversaries. ',
         'Oblivious RAM with Worst-Case Logarithmic Overhead',
         'No-Signaling Linear PCPs.']
for i in range(len(list1)):
    # 输入信息
    # ele = driver.find_element(By.XPATH, '//*[@id="query"]')
    que = None
    while que is None:
        try:
            que = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="query"]'))
            )
            # el[i].click()
        except TimeoutException:
            print("Element not found! Refreshing the page1...")
            driver.refresh()
    que.clear()
    que.send_keys(list1[i])
    que.send_keys(Keys.ENTER)
    # 找到下载按钮进行点击下载
    sleep(3)
    # 这个按钮上面还有别的东西覆盖，后来将代码改成
    # next_btn = driver.find_element(By.XPATH, '//a[@class="webtrekk-track pdf-link"]')
    next_btn = None
    while next_btn is None:
        try:
            next_btn = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[@class="webtrekk-track pdf-link"]'))
            )
        except TimeoutException:
            print("Element not found! Refreshing the page2...")
            driver.refresh()
    url = next_btn.get_attribute('href')
    # 正则表达式用于查找匹配的子字符串
    pattern = re.compile(r"F(.*?)\?")

    # 搜索URL以找到匹配项
    match = pattern.search(url)

    # 如果找到匹配项，则提取匹配的子字符串
    if match:
        result = match.group(1)  # group(1) 返回括号()中匹配的部分
        original_names.append(result)
    else:
        print("No match found")
    driver.execute_script("arguments[0].click();", next_btn)

sleep(20)
# 指定文件夹路径
folder_path = r'G:\PyCharm Community Edition 2023.2.1\project\paper'

# 为新文件名添加.pdf后缀
new_names = [name + ".pdf" for name in list1]

# 创建包含文件夹路径的完整文件路径
original_filepaths = [os.path.join(folder_path, fname) for fname in original_names]
new_filepaths = [os.path.join(folder_path, fname) for fname in new_names]

# 使用zip函数创建原始文件路径和新文件路径的映射字典
rename_map = dict(zip(original_filepaths, new_filepaths))

while True:
    # 检查所有原始文件是否存在
    missing_files = [f for f in original_filepaths if not os.path.exists(f)]
    if not missing_files:
        # 如果所有文件都存在，则进行重命名
        for original, renamed in rename_map.items():
            os.rename(original, renamed)
        print("文件重命名完成。")
        break
    else:
        # 如果有文件缺失，则打印缺失的文件名
        print(f"以下文件不存在: {', '.join(missing_files)}")


input()

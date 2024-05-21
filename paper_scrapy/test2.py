"""
selenium版本论文下载测试版本，测试阶段中，暂未完全实现所有功能。
无头模式排错用截图driver.save_screenshot('a.jpg')
"""
import re
from selenium.webdriver.support import expected_conditions as ec, wait
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

option = ChromeOptions()

"""
禁用GPU加速外，还添加了--log-level=3参数来禁用控制台输出。
--log-level=3参数将日志级别设置为最低，从而减少控制台输出。
"""
cookie = 'ipCheck=221.221.237.26; fp=1f515014881b2bc503cff913553c2554; AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg=1; s_ecid=MCMID%7C79311360846624169561888550810218726611; s_cc=true; cto_bundle=lRGThV9JSVh6MFJtWjVPTWUwOHclMkJRcFRSWmJEdjhaN2VkdEdCMGNMdWJQQSUyRkV1bG1PcWtXNnlIeUdBcDN4N1JSWXZkSXRwTENvUVhnQmVEWDFrV3lvVHdJamlseGNBTkk2Wkd5UDBTRW9nSHFuN3pxRW1qY2o4WklJQ21MSjZDbmFYJTJCZlVOVU4lMkI0cHpmbjdrUTdGSnJMSklVZyUzRCUzRA; ipList=221.221.237.26; AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg=359503849%7CMCIDTS%7C19672%7CMCMID%7C79311360846624169561888550810218726611%7CMCAAMLH-1700242316%7C11%7CMCAAMB-1700242316%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1699644716s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.1; TS01b03060=012f3506237278eb30e5cfb1378e37a7e4032eeddc8d85a013a21f3434eb1d2a333b926a6426c26cdaa6c52cf7144e4564908bd4a3; __gads=ID=5fdd2cf21c045246:T=1699629931:RT=1699637532:S=ALNI_Ma_y1sw5JT_Hh_fgQqeYUOzZNRePQ; s_sq=ieeexplore.prod%3D%2526c.%2526a.%2526activitymap.%2526page%253DDynamic%252520html%252520doc%252520detail%2526link%253DAccess%252520Through%252520Beijing%252520University%252520of%252520Technology%2526region%253DBODY%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DDynamic%252520html%252520doc%252520detail%2526pidt%253D1%2526oid%253DAccess%252520Through%25250ABeijing%252520University%252520of%252520Technology%2526oidt%253D3%2526ot%253DSUBMIT; JSESSIONID=Gka6Sw5i9gu7TfQxa_xKW1Hf_5DHqSVXg8z0AnwQC2e_NIC5XKaK!-1117416190; ERIGHTS=Wb2Nrx2FJIsvqS5W8ridr4WKpAEgQKYM3W-18x2dRjlQqGzYkFuXqW7gn9xx33Ax3Dx3Dg7t1ssnMNctdl4yKx2BjE6qgx3Dx3D-ik0nx2BLi4cJ3kAKLGx2B3vVAQx3Dx3D-kmSjmbNedUPIEul6IcIoMQx3Dx3D; WLSESSION=237134476.20480.0000; xpluserinfo=eyJpc0luc3QiOiJ0cnVlIiwiaW5zdE5hbWUiOiJCRUlKSU5HIFVOSVZFUlNJVFkgT0YgVEVDSE5PTE9HWSIsInByb2R1Y3RzIjoiSUVMfFZERXxOT0tJQSBCRUxMIExBQlN8In0=; seqId=12601; TSaeeec342027=080f8ceb8aab2000614577f56ac2f53f8f821d573da588c2793c9b5c32921d695eab27c4d7a5288008e1586d8c113000ce114d54d1586e93418ed031fc173d9e76f565b7bd0c38423129976a4dee46c457483e605cf0d8065b7ca9922181c2e8; utag_main=v_id:018bb9d69c97003c10601a3b02a80506f002b06700aee$_sn:2$_se:8$_ss:0$_st:1699639365848$vapi_domain:ieeexplore.ieee.org$ses_id:1699637515958%3Bexp-session$_pn:4%3Bexp-session'
# 将Cookie字符串转换为字典
# 使用正则表达式进行cookie解析
cookie_dict = {}
pattern = re.compile(r'(.*?)=(.*?)(;|$)')
matches = pattern.findall(cookie)
for match in matches:
    key, value, _ = match
    cookie_dict[key.strip()] = value

# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
option.add_experimental_option('prefs', {
    "download.default_directory": r'D:\PyCharm Community Edition 2023.2.3\project\pyscript\paper_scrapy',  # Change default directory for downloads
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
option.add_argument("--headless")  # 启用无头模式
# 附加的Headless参数/属性作为bot被拦截。
option.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'")
option.add_argument('--window-size=1920x1080')  # or whatever resolution you want
driver = webdriver.Chrome(options=option)
# driver.maximize_window()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})


# 遍历Cookie字典，并添加到浏览器会话中
# driver.add_cookie(cookie_dict)
driver.get('https://ieeexplore.ieee.org/Xplore/home.jsp')
for cookie_name, cookie_value in cookie_dict.items():
    cookie = {'name': cookie_name, 'value': cookie_value}
    driver.add_cookie(cookie)

# 刷新页面
driver.refresh()
# driver.save_screenshot('a.png')
# driver.find_element(By.XPATH, '//*[@id="home-page"]/section/div/div[2]/button[1]').click()
list1 = ['Aspect-Opinion Sentiment Alignment for Cross-Domain Sentiment Analysis (Student Abstract).',
         'Aspect-based Sentiment Analysis with Opinion Tree Generation.',
         'VerSA: Verifiable Secure Aggregation for Cross-Device Federated Learning.']
for i in range(len(list1)):
    # 定位搜索框
    # print(i)
    que = None
    while que is None:
        # driver.save_screenshot('b.png')
        try:
            que = WebDriverWait(driver, 30).until(
                ec.presence_of_element_located(
                    (By.XPATH, '//*[@type="search"and@aria-label="main"]'))
            )
            # driver.save_screenshot('c.png')
        except TimeoutException:
            print("Element not found! Refreshing the page1...")
            driver.refresh()
    que.clear()
    que.send_keys(list1[i])
    que.send_keys(Keys.ENTER)

    # next_btns = None
    while True:
        try:
            if WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="xplMainContent"]/div[1]/div/xpl-search-dashboard/section/div/h1/span[1]'))
            ).text == 'No results found':
                print('未找到文章')
                break
            else:
                next_btns = WebDriverWait(driver, 30).until(
                    ec.presence_of_all_elements_located((By.XPATH, '//a[@aria-label="PDF"]'))
                )
                # print(next_btns)
                print(next_btns, 'ne')
                for j in range(len(next_btns)):
                    print('j:', j)
                    next_btns = WebDriverWait(driver, 30).until(
                        ec.presence_of_all_elements_located((By.XPATH, '//a[@aria-label="PDF"]'))
                    )  # 重新查找next_btns元素
                    # print(len(next_btns), 'ne')
                    sleep(1)
                    driver.execute_script("arguments[0].click();", next_btns[j])
                    sleep(2)
                    driver.back()
                    sleep(1)
            break
        except TimeoutException:
            print("Element not found! Refreshing the page2...")
            driver.refresh()
    # # 退回主页
    # driver.back()
    # sleep(1)
    # driver.set_window_size(1920, 1080)

input()




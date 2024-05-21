#!D:\PyCharm Community Edition 2023.2.3\project\python.exe
"""
selenium版本的CCF信息安全类搜素工具，比较慢，建议还是使用request版本。
"""
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


# 颜色初始化
init(autoreset=True)
# 随机颜色(排除红色，红色警告专用)
choices = ['Fore.GREEN', 'Fore.YELLOW',
           'Fore.BLUE', 'Fore.CYAN', 'Fore.WHITE']

option = ChromeOptions()

"""
禁用GPU加速外，还添加了--log-level=3参数来禁用控制台输出。
--log-level=3参数将日志级别设置为最低，从而减少控制台输出。
"""
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument("--disable-blink-features")
option.add_argument("--disable-blink-features=AutomationControlled")
option.add_argument('--disable-gpu')  # 似乎能避免一些bug
option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片提升运行速度
option.add_argument('log-level=3')  # 禁用大量日志信息滚动输出
option.add_argument("--headless")  # 启用无头模式
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

# 进入CCF期刊官网，
driver.get('https://www.ccf.org.cn/Academic_Evaluation/NIS/')
# sleep(2)

# 选择想要的期刊：A类：tdsc,tifs,joc;B类：compsec,dcc,jcs,ACM(单独处理)
a_paper = ['tdsc', 'tifs', 'joc']
b_paper = ['tops', 'compsec', 'dcc', 'jcs']

# 输入搜索文章关键词(用“”)
keywords = []  # 创建一个空列表
while True:
    string = input(Fore.RED + "请输入文章关键词（按回车键结束）: ")
    if string == '':
        break
    keywords.append(string.strip())  # 将带有双引号的字符串加入列表中

# keywords = ["Verifiable", "Federated Learning"]
# keywords = ["DNS"]

# 退回标志
flag = False

# 选择期刊类型
choice_paper = input(eval(random.choice(choices)) + '请选择期刊类型（输入a或b，代表A类或B类）：')

# 请选择年份
year = input(eval(random.choice(choices)) + '请输入所需期刊截至年份（从2023年到之前多少年的期刊）：')
print('\n')
print(eval(random.choice(choices)) + '正在打印文章名，请耐心等待......')
print('\n')

# 取期刊长度
while True:
    if choice_paper.strip().upper() == 'A':
        lens = len(a_paper)
        break
    elif choice_paper.strip().upper() == 'B':
        lens = len(b_paper)
        break
    else:
        print(Fore.RED + '请按要求输入a 或 b ！！！')
        choice_paper = input(Fore.YELLOW + '请选择期刊类型（输入a或b，代表A类或B类）：')


# 文章计数
sum1 = 0

# 打印每个刊
for i in range(lens):  # 下标从0开始
    # 退回到选刊界面
    if flag:
        driver.back()
        driver.back()

    while True:
        if choice_paper.strip().upper() == 'A':
            # 打印a类每个刊
            driver.find_element(By.XPATH, '//a[@href="http://dblp.uni-trier.de/db/journals/' + a_paper[i] + '/"]').click()
            break
        elif choice_paper.strip().upper() == 'B':
            # 打印b类每个刊
            # 单独打印ACM刊物（因为其网址的特殊性）
            if i == 0:
                driver.find_element(By.XPATH, '//a[@href="https://dblp.org/db/journals/tissec/index.html"]').click()
            else:
                driver.find_element(By.XPATH, '//a[@href="http://dblp.uni-trier.de/db/journals/' + b_paper[i] + '/"]').click()
            break
        else:
            print(Fore.RED + '请按要求输入a 或 b ！！！')
            choice_paper = input(Fore.YELLOW + '请选择期刊类型（输入a或b，代表A类或B类）：')


    # 年份选择(很奇怪根据文本和href定位不了),1代表2023年文章，2代表2022，以此类推
    # year = input('请输如需要哪一年的文章（1代表2023年文章，2代表2022，以此类推）：')
    # // *[ @ id = "main"] / ul/ li[1] / a
    # 退回标志
    flag = False
    for y in range(1, 2025-int(year.replace(" ", ""))):
        # sleep(2)
        if flag:
            driver.back()

        # 年份选择(很奇怪根据文本和href定位不了),1代表2023年文章，2代表2022，以此类推
        # sleep(2)
        # driver.find_element(By.XPATH, '//*[@id="main"]/ul/li[' + str(year) + ']/a').click()
        el = driver.find_elements(By.XPATH, '//*[@id="main"]/ul/li[' + str(y) + ']/a')
        
        # 退回标志
        flag = False
        # sleep(2)
        for e in range(len(el)):
            if flag:
                driver.back()
            # el = driver.find_elements(By.XPATH, '//*[@id="main"]/ul/li[' + str(y) + ']/a')
            #
            # el[i].click()
            el = None
            while el is None:
                try:
                    el = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, '//*[@id="main"]/ul/li[' + str(y) + ']/a'))
                    )
                    # el[i].click()
                except TimeoutException:
                    print("Element not found! Refreshing the page1...")
                    driver.refresh()
            el[e].click()
            # e.click()

            # 输入搜索文章关键词
            # driver.implicitly_wait(10)
            # ele = driver.find_element(By.XPATH, '//*[@id="tocpage-refine"]/div/div[2]/div/span/input')

            # 使用WebDriverWait和expected_conditions来等待页面上的某个特定元素加载完成。
            ele = None
            while ele is None:
                try:
                    ele = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="tocpage-refine"]/div/div[2]/div/span/input'))
                    )
                except TimeoutException:
                    print("Element not found! Refreshing the page2...")
                    driver.refresh()

            # t = True
            # global ele
            # while t:
            #     try:
            #         ele = driver.find_element(By.XPATH, '//*[@id="tocpage-refine"]/div/div[2]/div/span/input')
            #         t = False
            #         # print("Element exists")
            #     except NoSuchElementException:
            #         # t = True
            #         driver.refresh()
            #         # print("Element does not exist")
            #     sleep(5)

            # 合成关键词并进行搜索
            keyword = " ".join(keywords)
            ele.send_keys(keyword)
            ele.send_keys(Keys.ENTER)
            # sleep(5)
            # 收集文章名字
            # global key
            # # 只有第一次得到key的Xpath值，后面重复利用
            # if not flag:
            #     key = '//*['
            #     for keys in keywords:
            #         if keys == keywords[len(keywords) - 1]:
            #             key += ' contains(text(),"' + keys + '") ]'
            #         else:
            #             key += ' contains(text(),"' + keys + '") and'

            # sleep(2)
            # ele1 = driver.find_elements(By.XPATH, '//*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "Federated Learning")]')
            # 依次打印文章名字
            # 显式等待（ExplicitWait）：显式等待是一种针对特定条件等待的机制，它会在等待时间内轮询检查条件是否满足，
            # 只有当条件满足时才会继续执行后续的命令。
            # wait = WebDriverWait(driver, 6000)
            # ele1 = wait.until(EC.visibility_of_any_elements_located((By.XPATH, key)))
            # // *[ @ id = "journals/compsec/ChenWZL23"] / cite / span[5]
            key = ('//li[@class="entry article" and not(ancestor-or-self::*[contains(@style, "display: none") or '
                   'contains(@style, "visibility: hidden")])]//span[@class="title"]')
            sleep(5)
            # 为了尽可能全面得到元素
            ele1 = driver.find_elements(By.XPATH, key)
            for k in range(2):
                ele1 = driver.find_elements(By.XPATH, key)
                sleep(1)
            for j in range(len(ele1)):
                # sleep(3)
                ele1 = driver.find_elements(By.XPATH, key)
                text = ele1[j].text.strip()
                if text != "" and text.isprintable():
                    # # Springer文章下载
                    # if choice_paper  == 'A' and i == 2:
                    # # IEEE文章下载
                    # elif (choice_paper == 'A' and i == 0) or (choice_paper == 'A' and i == 1):
                    print(Fore.MAGENTA + text)
                    sum1 += 1
            flag = True
print('\n搜索结束请查收，一共', Fore.RED + str(sum1), '篇！！！')
# 退出浏览器
input()
driver.quit()

"""
paper_ultra的测试程序
"""
import json
import time
import logging
import os
import pandas as pd
import random
import re
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
from lxml import etree

proxy = None

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='test.log',  # 日志输出到文件
    filemode='w'  # 追加模式
)


def get_proxy1():
    # 5000：settings中设置的监听端口，不是Redis服务的端口
    return requests.get("http://123.57.226.67:6666/get/").json()


def delete_proxy1(proxy):
    requests.get("http://123.57.226.67:6666/delete/?proxy={}".format(proxy))


# 2. 验证代理IP可用性
def verify_proxy1(proxy):
    # 构造请求头，模拟浏览器请求
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)"
    ]
    headers = {'User-Agent': random.choice(user_agent_list)}

    # 请求目标网页并判断响应码
    url = "http://www.baidu.com"
    try:
        response = requests.get(url, headers=headers, proxies={"http": f"http://{proxy}"}, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logging.error(f"代理 {proxy} 验证失败: {e}")
        return False


# 网址访问函数
def get_response1(url, i=0):
    global proxy
    param = {
        'q': 'title:Federated Learning type:Journal_Articles:year:2023|2022|2021|2020|2018|2019',
        's': 'ydvspc',
        'h': '30',
        'b': f'{i}'
    }
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)"
    ]
    headers = {'User-Agent': random.choice(user_agent_list)}

    # while True:
    #     session = requests.Session()
    #     # 设置重试次数以及回退策略
    #     retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    #     session.mount('http://', HTTPAdapter(max_retries=retries))

    while True:
        if proxy is None:
            proxy_info = get_proxy1()
            if not proxy_info:
                logging.error("无法获取代理")
                return None
            proxy = proxy_info.get("proxy")
            logging.info(f"使用新代理: {proxy}")

        if not verify_proxy1(proxy):
            delete_proxy1(proxy)
            proxy = None
            continue

        try:
            response = requests.get(url, params=param, headers=headers, proxies={"http": f"http://{proxy}"}, timeout=10)
            response.encoding = 'utf-8'
            response.raise_for_status()
            return response
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            logging.error(f"请求异常: {e} ")
            delete_proxy1(proxy)
            proxy = None


# # 数据初始化，读取JSON文件并转换为字典(用于进行分类)
# with open('Journal_Articles.json', 'r', encoding='utf-8') as json_file:
#     Journal_Articles = json.load(json_file)
# with open('Conference_and_Workshop_Papers.json', 'r', encoding='utf-8') as json_file:
#     Conference_and_Workshop_Papers = json.load(json_file)
#
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                      "537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

url = 'https://dblp.uni-trier.de/search/publ/api?callback=jQuery31109242945945981864_1699447770265&q=title%3AFederated Learning%20type%3AJournal_Articles%3Ayear%3A2023%7C2022%7C2021%7C2020%7C2018%7C2019&compl=year&p=2&h=0&c=10&rw=3d&format=jsonp&_=1699447770266'
# 获取搜素的文章总数
response = requests.get(url=url, headers=headers)
response_text = response.text  # 假设这是从请求中获取的文本
# 找到 JSON 数据的开始和结束位置
start = response_text.find('(') + 1
end = response_text.rfind(')')
# 提取 JSON 字符串
json_str = response_text[start:end]
# 解析 JSON 数据
data = json.loads(json_str)
total_hits = data['result']['hits']['@total']
print(f"总共检索到文章{total_hits}篇！")

# 存储数据专用
journal_data = []
# itemprop_spans = []
# title_text = []
# combined_results = []

# 创建HTML解析器对象
for i in range(0, int(int(total_hits)/30) + 1):

    url = 'https://dblp.uni-trier.de/search/publ/inc'
    res = get_response1(url, i)
    html_content = res.text
    tree = etree.HTML(html_content)
    # 拿到每一页的li标签
    li_tags = tree.xpath('//li[@class="entry article toc"]')
    # print(len(li_tags))
    # print(li_tags)

    for li in li_tags:
        # Use relative XPath queries (note the dot at the beginning)
        title_list = li.xpath('.//span[@class="title" and @itemprop="name"]/text()')
        # print(title_list)
        title = title_list[0].strip() if title_list else "Title not found"

        publisher_list = li.xpath('.//a/span/span[@itemprop="name"]/text()')
        publisher = publisher_list[0].strip() if publisher_list else "Publisher not found"

        year_list = li.xpath('.//span[@itemprop="datePublished"]/text()')
        year = year_list[0].strip() if year_list else "Year not found"

        journal_data.append({
            'title': title,
            'publisher': publisher,
            'year': year
        })
    # itemprop_spans.extend(
    #     tree.xpath('//span[@class="title" and @itemprop="name"]/following-sibling::a//span[@itemprop="name"]/text()'))
    # title_text.extend(tree.xpath('//span[@class="title" and @itemprop="name"]/text()'))
    # combined_results.extend(list(zip(title_text, itemprop_spans)))
    #     print(journal_data)

Journal_A = []
Journal_B = []
Journal_C = []

#
# # 记录循环开始时间
# start_time = time.time()
# # 输出配对结果
# for journal in journal_data:
#     if journal['publisher'] in Journal_Articles['A']:
#         Journal_A.append(journal)
#     elif journal['publisher'] in Journal_Articles['B']:
#         Journal_B.append(journal)
#     elif journal['publisher'] in Journal_Articles['C']:
#         Journal_C.append(journal)
#
# # 记录循环结束时间
# end_time = time.time()
# # 计算循环的运行时间
# elapsed_time = end_time - start_time
# print(f"循环运行时间: {elapsed_time} 秒")
#
# 检查是否搜索成功
print('总共', len(journal_data), '篇文章！\n')
if int(total_hits) == len(journal_data):
    print('搜索成功！！！')
print(journal_data)
# # 输出类别A的文章
# print("Category A articles:")
# print(len(Journal_A))
# for article in Journal_A:
#     print(article)
#
# # 输出类别B的文章
# print("\nCategory B articles:")
# print(len(Journal_B))
# for article in Journal_B:
#     print(article)
#
# # 输出类别C的文章
# print("\nCategory C articles:")
# print(len(Journal_C))
# for article in Journal_C:
#     print(article)

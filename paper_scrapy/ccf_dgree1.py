import json
import logging
import random
# from json import JSONDecodeError

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from lxml import etree

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='paper_search.log',  # 日志输出到文件
    filemode='a'  # 追加模式
)


def get_proxy1():
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
        delete_proxy1(proxy)
        return False


# 网址访问函数
def get_response1(url, proxy=None):
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

    while True:
        session = requests.Session()
        # 设置重试次数以及回退策略
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))

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
                response = session.get(url, headers=headers, proxies={"http": f"http://{proxy}"}, timeout=10)
                response.encoding = 'utf-8'
                response.raise_for_status()
                return response, proxy
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                    requests.exceptions.HTTPError, requests.exceptions.RequestException,
                    requests.exceptions.JSONDecodeError) as e:
                logging.error(f"请求异常: {e} ")
                delete_proxy1(proxy)
                proxy = None


def get_category_ids(soup):  # 注意这里的参数是BeautifulSoup对象
    category_ids = {}

    categories = soup.find_all('h3', {'class': 'm-tit1'})  # 找到所有h3标签

    for category in categories[3:6]:
        title = category.text.strip()  # A类, B类, C类
        id_ = category['id']  # 获取id
        category_ids[title] = id_

    return category_ids


def get_journal_info(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # 根据网页的实际编码来设置
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    category_ids = get_category_ids(soup)
    # print(category_ids)

    def extract_info(category_id):  # 这里改成根据id获取信息
        data = []
        ul = soup.find('h3', {'id': category_id}).find_next('ul')
        for li in ul.find_all('li')[1:]:
            sname = li.find('div', {'style': 'width:10%;'}).text.strip()
            full_name = li.find('div', {'style': 'width:40%;'}).text.strip()
            publisher = li.find('div', {'style': 'width:9%;'}).text.strip()
            address_tag = li.find('div', {'style': 'width:36%;'}).find('a')
            address = address_tag['href'] if address_tag else None
            data.append({
                'sname': sname,
                'full_name': full_name,
                'publisher': publisher,
                'address': address
            })
        return data

    a_class_data = extract_info(category_ids['A类'])
    b_class_data = extract_info(category_ids['B类'])
    c_class_data = extract_info(category_ids['C类'])

    return {
        'A类': a_class_data,
        'B类': b_class_data,
        'C类': c_class_data
    }


def print_journal_info(journals):
    print(f"{'-' * 30}")
    for i, journal in enumerate(journals, 1):
        print(f"序号: {i}")
        print(f"刊物全称：{journal['full_name']}")
        print(f"出版社：{journal['publisher']}")
        print(f"地址：{journal['address']}")
        print(f"{'-' * 30}")


def get_research_directions(current_proxy):
    url = "https://www.ccf.org.cn/Academic_Evaluation/By_category/"
    # current_proxy = None

    response, current_proxy = get_response1(url, current_proxy)

    base_url = "https://www.ccf.org.cn"
    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.content, 'lxml')
    ul_tag = soup.find('ul', style="float:right")
    if ul_tag:
        li_tags = ul_tag.find_all('li', id=True)[1:-2]  # 获取所有有id属性的li标签，并排除第一个

        # 创建空字典用来存储数据
        data = {}

        for li in li_tags:
            a_tag = li.find('a')
            if a_tag:
                title = a_tag.get('title')
                href = a_tag.get('href')
                if title and href:  # 判断 title 和 href 是否都不为 None

                    # 处理链接，确保它是一个完全的 URL
                    if not href.startswith('http'):
                        href = base_url + href

                    # 将标题和链接作为键值对添加到字典中
                    data[title] = href

    # 返回包含所有数据的字典
    return data, current_proxy


def choose_direction(data):
    selected_hrefs = []
    print('CCF推荐国际学术刊物目录: ')
    for i, title in enumerate(data.keys(), 1):
        print(f"{i}. {title}")
    print('\n')

    for i in range(1, len(data) + 1):
        # 获取用户选择的标题
        selected_title = list(data.keys())[i - 1]
        # print(selected_title)
        # 获取相应的链接
        selected_hrefs.append(data[selected_title])

    return selected_hrefs


current_proxy = None
# 创建一个字典，其键为"A"、"B"、"C"，值为空列表
# 会议的a,b,c类
Conference_and_Workshop_Papers = {'A': [], 'B': [], 'C': []}
# 选择研究的方向
data, current_proxy = get_research_directions(current_proxy)
hrefs = choose_direction(data)
for j in ['A', 'B', 'C']:
    for i in hrefs:
        journal_info = get_journal_info(i)
        select_data = journal_info[j + '类']
        for journal in select_data:
            if journal['sname']:
                print(journal['sname'])
                Conference_and_Workshop_Papers[j].append(journal['sname'])
            else:
                print('空')
                print(journal['address'])
                print('\n')

            # response, current_proxy = get_response1(journal['address'], current_proxy)
            # tree = etree.HTML(response.text)
            # h1_text = tree.xpath('//*[@id="headline"]/h1/text()')
            # if h1_text:
            #     text = h1_text[0]
            #     if text.strip() == '':
            #         print('空标题')
            #         print(journal['address'])
            #         print('\n')
            #     else:
            #         start = text.find('(')
            #         end = text.find(')')
            #         if start != -1 and end != -1:
            #             # 提取括号内的文本
            #             extracted_text = text[start + 1:end]
            #             print(extracted_text)
            #             Conference_and_Workshop_Papers[j].append(extracted_text)
            #         else:
            #             # 如果没有括号，使用整个文本
            #             extracted_text = text
            #             Conference_and_Workshop_Papers[j].append(extracted_text)
            #             print(extracted_text)
            # else:
            #     print("没有找到匹配的h1元素。")
            #     print(journal['address'])
            #     print('\n')

for k in ['A', 'B', 'C']:
    print(f'{k}类所有期刊名: \n')
    print(Conference_and_Workshop_Papers[k])
    json_data = json.dumps(Conference_and_Workshop_Papers)
    # 将JSON字符串写入文件
    with open('Conference_and_Workshop_Papers.json', 'w') as file:
        file.write(json_data)
    print('\n')





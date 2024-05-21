"""
论文搜索普通模式，速度一般，但是稳定
"""
import logging
import os
import pandas as pd
import random
import re
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='paper_search.log',  # 日志输出到文件
    filemode='a'  # 追加模式
)


def get_proxy():
    # 5000：settings中设置的监听端口，不是Redis服务的端口
    return requests.get("http://123.57.226.67:6666/get/").json()


def delete_proxy(proxy):
    requests.get("http://123.57.226.67:6666/delete/?proxy={}".format(proxy))


# 2. 验证代理IP可用性
def verify_proxy(proxy):
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
def get_response(url, proxy=None):
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
                proxy_info = get_proxy()
                if not proxy_info:
                    logging.error("无法获取代理")
                    return None
                proxy = proxy_info.get("proxy")
                logging.info(f"使用新代理: {proxy}")

            if not verify_proxy(proxy):
                delete_proxy(proxy)
                proxy = None
                continue

            try:
                response = session.get(url, headers=headers, proxies={"http": f"http://{proxy}"}, timeout=10)
                response.encoding = 'utf-8'
                response.raise_for_status()
                return response, proxy
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                    requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
                logging.error(f"请求异常: {e} ")
                delete_proxy(proxy)
                proxy = None
            # except requests.exceptions.Timeout as e:
            #     logging.error(f"请求超时: {e}")
            #     # delete_proxy(proxy)
            #     proxy = None
            # except requests.exceptions.HTTPError as e:
            #     logging.error(f"HTTP错误: {e}")
            #     delete_proxy(proxy)
            #     proxy = None
            # except requests.exceptions.ConnectionError as e:
            #     logging.error(f"连接错误: {e}")
            #     delete_proxy(proxy)
            #     proxy = None
            # except requests.exceptions.RequestException as e:
            #     logging.error(f"请求异常: {e}")
            #     delete_proxy(proxy)
            #     proxy = None


# 获取研究方向
def get_research_directions(current_proxy):
    url = "https://www.ccf.org.cn/Academic_Evaluation/By_category/"
    # current_proxy = None
    response, current_proxy = get_response(url, current_proxy)

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


# 获取abc类期刊id信息
def get_category_ids(soup):  # 注意这里的参数是BeautifulSoup对象
    category_ids = {}

    categories = soup.find_all('h3', {'class': 'm-tit1'})  # 找到所有h3标签

    for category in categories[0:3]:
        title = category.text.strip()  # A类, B类, C类
        id_ = category['id']  # 获取id
        category_ids[title] = id_

    return category_ids


# 获取某个方向的ABC类期刊信息
def get_journal_info(url, current_proxy):

    response, current_proxy = get_response(url, current_proxy)
    # response.encoding = 'utf-8'  # 根据网页的实际编码来设置
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    category_ids = get_category_ids(soup)
    # print(category_ids)

    def extract_info(category_id):  # 这里改成根据id获取信息
        data = []
        ul = soup.find('h3', {'id': category_id}).find_next('ul')
        for li in ul.find_all('li')[1:]:
            full_name = li.find('div', {'style': 'width:40%;'}).text.strip()
            publisher = li.find('div', {'style': 'width:9%;'}).text.strip()
            address_tag = li.find('div', {'style': 'width:36%;'}).find('a')
            address = address_tag['href'] if address_tag else None
            data.append({
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
    }, current_proxy


# 选择期刊种类
def choose_journal_type():
    # 提供类型选择
    while True:
        type_choice = input("Please choose the journal type: [A / B / C]: ")
        type_choice = type_choice.upper()
        if type_choice in ['A', 'B', 'C']:
            return type_choice
        else:
            print("Invalid selection. Please choose [A, B or C]: ")


# 打印某个类别的期刊信息
def print_journal_info(journals):
    print(f"{'-' * 30}")
    for i, journal in enumerate(journals, 1):
        print(f"序号: {i}")
        print(f"刊物全称：{journal['full_name']}")
        print(f"出版社：{journal['publisher']}")
        print(f"地址：{journal['address']}")
        print(f"{'-' * 30}")


# 返回选取的数据
def get_selected_journal_info(href, type_choice, current_proxy):
    journal_info, current_proxy = get_journal_info(href, current_proxy)
    select_data = journal_info[type_choice + '类']

    print(f'好的,以下是{type_choice}类所有期刊: ')
    print_journal_info(select_data)

    return select_data


# 返回选择的方向的链接
def choose_direction(data):
    for i, title in enumerate(data.keys(), 1):
        print(f"{i}. {title}")

    while True:
        choice = input("Please enter the number of the direction you want to visit: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(data):

                # 获取用户选择的标题
                selected_title = list(data.keys())[choice - 1]
                # 获取相应的链接
                selected_href = data[selected_title]
                return selected_href
            else:
                print("Invalid number. Please enter a number between 1 and", len(data))
        except ValueError:
            print("Invalid input. Please enter a number.")


# 搜索论文专用
def extract_volumes(url, current_proxy, journal_name, start_year, end_year, keyword):
    keywords = keyword.split()
    # 构建正则表达式，确保句子包含所有关键词
    pattern = r'(?=.*\b' + r'\b)(?=.*\b'.join(
        [re.escape(keyword) for keyword in keywords]) + r'\b).*\.'
    response, current_proxy = get_response(url, current_proxy)
    if not response:
        print("Failed to get response from url.")
        return [], current_proxy

    soup = BeautifulSoup(response.content, 'lxml')
    ul_content = soup.select_one('#main > ul')
    if not ul_content:
        print("Failed to find the main list in the page.")
        return [], current_proxy

    volumes_to_visit = []
    li_elements = ul_content.find_all('li')
    for li in li_elements:
        year_match = re.search(r'\d{4}', li.text)
        if year_match:
            year = int(year_match.group())
            if start_year <= year <= end_year:
                a_elements = li.find_all('a')
                for a in a_elements:
                    volumes_to_visit.append((a.get("href"), year))
    # 全局计数
    global sum1

    titles_and_journals = []
    for href, year in volumes_to_visit:
        response, current_proxy = get_response(href, current_proxy)
        if response:
            soup = BeautifulSoup(response.content, 'lxml')
            title_tags = soup.find_all('span', {'class': 'title', 'itemprop': 'name'})
            for title_tag in title_tags:
                if title_tag and re.search(pattern, title_tag.text, re.IGNORECASE):
                    titles_and_journals.append((title_tag.text, journal_name, year))
                    print(title_tag.text)
                    sum1 += 1
    # print(f"找到包含关键词的标题总数：{sum1}")
    return titles_and_journals, current_proxy


# 存为txt文件
def save_titles_to_txt(titles_and_journals, sum_article, keyword, start_year, end_year, file_path):
    dir_path = os.path.dirname(file_path)
    if dir_path:  # 检查路径是否为空
        os.makedirs(dir_path, exist_ok=True)

    # file_exists = os.path.isfile(file_path)  # 检查文件是否已经存在
    with open(file_path, 'a', encoding='utf-8') as file:
        # # 如果文件不存在或为空，写入关键词、起始年份和结束年份
        # if not file_exists or os.path.getsize(file_path) == 0:
        file.write(f"Keyword: {keyword}\n")
        file.write(f"Start Year: {start_year}\n")
        file.write(f"End Year: {end_year}\n")
        # file.write(f"Total: {sum_article}\n")
        file.write('一共' + str(sum_article) + '篇。\n')
        # 然后写入每个标题
        for title, journal, year in titles_and_journals:
            file.write(f"{title}\t{journal}\t{year}\n")


# 存为excel文件
def save_titles_to_excel(titles, sum_article, keyword, start_year, end_year, file_name):
    # 根据提供的titles数据结构，指定列名
    column_names = ['Title', 'Journal', 'Year']

    # 创建一个DataFrame
    df = pd.DataFrame(titles, columns=column_names)

    # 生成文件名
    file_name = f"{keyword}_{str(start_year)}_{str(end_year)}_{str(sum_article)}_{file_name}"

    # 写入Excel文件
    df.to_excel(file_name, index=False, engine='openpyxl')


if __name__ == '__main__':
    sum1 = 0
    # global current_proxy
    current_proxy = None
    # 示例
    start_year = 2018
    end_year = 2023
    keyword = 'federated learning'
    # keyword = "Public Opinion Analysis"
    # keyword = 'dns'
    data, current_proxy = get_research_directions(current_proxy)
    href = choose_direction(data)
    type_choice = choose_journal_type()
    select_data = get_selected_journal_info(href, type_choice, current_proxy)

    all_titles = []
    # print(select_data)
    for journal in select_data:
        journal_name = journal['full_name']  # 使用 'full_name' 作为期刊名称
        journal_url = journal['address']
        titles_and_journals, current_proxy = extract_volumes(journal_url, current_proxy, journal_name, start_year, end_year, keyword)
        all_titles.extend(titles_and_journals)

    sum_article = len(all_titles)
    print(f"一共找到包含关键词的文章总数：{sum1}")

    if all_titles:
        # 在写入每个期刊的标题之前，可能需要先写入关键词、起始年份和结束年份
        # save_titles_to_txt(all_titles, sum_article, keyword, start_year, end_year, 'journal_titles.txt')

        # 保存为Excel格式的文件
        save_titles_to_excel(all_titles, sum_article, keyword, start_year, end_year, 'journal_titles.xlsx')
    else:
        print("No titles found .")

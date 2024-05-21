"""
论文搜索异步模式，速度还行
pyinstaller --onefile --icon=ccf.ico --name="DMS Paper Spider" paper_search_upate.py
在PowerShell中，使用cd命令切换目录时，需要将文件夹路径放在引号中，因为路径中包含空格。请使用以下命令来切换到指定的文件夹：
Set-Location "D:\PyCharm Community Edition 2023\project\pyscript"
"""
import asyncio
import logging
import os
import aiohttp
import requests
from aiohttp import ClientTimeout, TCPConnector
import pandas as pd
import random
import re
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from colorama import Fore, Back, Style, init

# 颜色初始化
init(autoreset=True)
# 随机颜色(排除红色，红色警告专用)
choices = ['Fore.GREEN', 'Fore.YELLOW',
           'Fore.BLUE', 'Fore.MAGENTA', 'Fore.CYAN', 'Fore.WHITE']

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='paper_search.log',  # 日志输出到文件
    filemode='a'  # 追加模式
)


def display_credits_and_notes():
    """
    Display the creator's name and some notes to the user.
    """
    print("==========================================")
    print(Fore.RED + "DMS Paper Spider - Version 1.0")
    print(Fore.RED + "Created by: [", eval(random.choice(choices)) + "tian_you", Fore.RED + "]")
    print("==========================================")
    print(Fore.YELLOW + "\n注意事项:")
    print(Fore.RED + "1. 本脚本功能自动根据关键词汇总CCF-A B C类文章。")
    print(Fore.RED + "2. 启动和搜索过程", Fore.YELLOW + "可能比较缓慢，因为云服务器上部署的代理IP池有限，请耐心等待，感谢理解！！！")
    print(Fore.RED + "3. 如有任何问题，请联系[制作人的邮箱:2389765824@qq.com]。")
    print(Fore.RED + "4. 请不要在未经授权的情况下分发或修改此脚本。")
    print("==========================================\n")


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
                    requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
                logging.error(f"请求异常: {e} ")
                delete_proxy1(proxy)
                proxy = None


async def get_proxy(session):
    # 5000：settings中设置的监听端口，不是Redis服务的端口
    # async with aiohttp.ClientSession() as session:
    async with session.get("http://123.57.226.67:6666/get/") as response:
        return await response.json()


async def delete_proxy(proxy, session):
    # async with aiohttp.ClientSession() as session:
    await session.get(f"http://123.57.226.67:6666/delete/?proxy={proxy}")


# 2. 验证代理IP可用性
async def verify_proxy(proxy, session):
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
    async with aiohttp.ClientSession() as session:
        try:
            # 注意这里使用了 await 来等待异步操作的结果
            async with session.get(url, headers=headers, proxy=f"http://{proxy}", timeout=10) as response:
                # 这里也需要使用 await 来等待 raise_for_status 的结果
                response.raise_for_status()
                return True
        except aiohttp.ClientError as e:
            logging.error(f"代理 {proxy} 验证失败: {e}")
            return False


# 网址访问函数
async def get_response(url, proxy=None, session=None):
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


    # aiohttp 不支持自动重试，所以我们需要手动实现

    while True:
        if proxy is None:
            proxy_info = await get_proxy(session)  # 使用 await 调用异步函数
            if not proxy_info:
                logging.error("无法获取代理")
                return None
            proxy = proxy_info.get("proxy")
            logging.info(f"使用新代理: {proxy}")

        if not await verify_proxy(proxy, session):  # 使用 await 调用异步函数
            await delete_proxy(proxy, session)  # 使用 await 调用异步函数
            proxy = None
            continue

        try:
            async with session.get(url, headers=headers, proxy=f"http://{proxy}") as response:
                response.raise_for_status()
                return await response.text(), proxy
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(f"请求异常: {e}")
            await delete_proxy(proxy, session)  # 使用 await 调用异步函数
            proxy = None
        except Exception as e:
            logging.error(f"未预料的错误: {e}")
            proxy = None

    # return None, proxy


# 获取研究方向
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

    response, current_proxy = get_response1(url, current_proxy)
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
        type_choice = input(eval(random.choice(choices)) + "请选择期刊类别: [A / B / C]: ")
        type_choice = type_choice.upper()
        if type_choice in ['A', 'B', 'C']:
            return type_choice
        else:
            print(Fore.RED + "Invalid selection. Please choose [A, B or C]: ")


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

    print(eval(random.choice(choices)) + f'好的,以下是{type_choice}类所有期刊: ')
    print_journal_info(select_data)

    return select_data


# 返回选择的方向的链接
def choose_direction(data):
    print(eval(random.choice(choices)) + 'CCF推荐国际学术刊物目录: ')
    for i, title in enumerate(data.keys(), 1):
        print(f"{i}. {title}")
    print('\n')

    while True:
        choice = input(eval(random.choice(choices)) + "请选择研究方向(输入数字1-10）: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(data):

                # 获取用户选择的标题
                selected_title = list(data.keys())[choice - 1]
                # 获取相应的链接
                selected_href = data[selected_title]
                return selected_href
            else:
                print(Fore.RED + "Invalid number. Please enter a number between 1 and", len(data))
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")


# 抛出异常
class ContentNotFoundException(Exception):
    pass


# 搜索论文专用
async def extract_volumes(url, current_proxy, journal_name, start_year, end_year, keyword, session):
    keywords = keyword.split()
    pattern = r'(?=.*\b' + r'\b)(?=.*\b'.join(
        [re.escape(keyword) for keyword in keywords]) + r'\b).*\.'

    response, current_proxy = await get_response(url, current_proxy, session)
    if not response:
        raise ContentNotFoundException("Failed to get response from url.")

    soup = BeautifulSoup(response, 'lxml')
    ul_content = soup.select_one('#main > ul')
    if not ul_content:
        raise ContentNotFoundException("Failed to find the main list in the page.")

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

    titles_and_journals = []
    for href, year in volumes_to_visit:
        response, current_proxy = await get_response(href, current_proxy, session)
        if response:
            soup = BeautifulSoup(response, 'lxml')
            title_tags = soup.find_all('span', {'class': 'title', 'itemprop': 'name'})
            for title_tag in title_tags:
                if title_tag and re.search(pattern, title_tag.text, re.IGNORECASE):
                    titles_and_journals.append((title_tag.text, journal_name, year))
                    print(Fore.CYAN + title_tag.text)
                    all_titles.append((title_tag.text, journal_name, year))

    return titles_and_journals, current_proxy


# 存为txt文件
def save_titles_to_txt(titles, sum_article, keyword, start_year, end_year, file_name):
    dir_path = os.path.dirname(file_name)
    if dir_path:  # 检查路径是否为空
        os.makedirs(dir_path, exist_ok=True)

    # file_exists = os.path.isfile(file_path)  # 检查文件是否已经存在
    with open(file_name, 'a', encoding='utf-8') as file:
        # # 如果文件不存在或为空，写入关键词、起始年份和结束年份
        # if not file_exists or os.path.getsize(file_path) == 0:
        file.write(f"Keyword: {keyword}\n")
        file.write(f"Start Year: {start_year}\n")
        file.write(f"End Year: {end_year}\n")
        # file.write(f"Total: {sum_article}\n")
        file.write('一共' + str(sum_article) + '篇。\n')
        # 然后写入每个标题
        for title, journal, year in titles:
            file.write(f"{title}\t{journal}\t{year}\n")


# 存为excel文件
def save_titles_to_excel(titles, sum_article, keyword, start_year, end_year, file_name):
    # 根据提供的titles数据结构，指定列名
    # titles = list(titles)
    column_names = ['Title', 'Journal', 'Year']
    # 创建一个DataFrame
    df = pd.DataFrame(titles, columns=column_names)

    # 生成文件名
    file_name = f"{keyword}_{str(start_year)}_{str(end_year)}_{str(sum_article)}_{file_name}"

    # 写入Excel文件
    df.to_excel(file_name, index=False, engine='openpyxl')


async def fetch_and_extract(journal, current_proxy, start_year, end_year, keyword, session):
    retries = 0
    max_retries = 100
    while retries < max_retries:
        try:
            journal_name = journal['full_name']
            journal_url = journal['address']
            titles_and_journals, current_proxy = await extract_volumes(
                journal_url, current_proxy, journal_name, start_year, end_year, keyword, session
            )
            # 确保返回的是列表
            return titles_and_journals, current_proxy
        except Exception as e:
            # 如果发生异常，记录或处理它，并进行重试
            logging.error(f"在获取和提取过程中发生错误: {e}, 正在重试... ({retries + 1}/{max_retries})")
            # print(f"在获取和提取过程中发生错误: {e}, 正在重试... ({retries + 1}/{max_retries})")
            retries += 1
            await asyncio.sleep(1)  # 增加延迟避免立即重试可能导致的问题
    return [], current_proxy  # 达到最大重试次数后返回空列表


async def main(start_year, end_year, keyword):
    global all_titles
    global current_proxy

    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=10), connector=TCPConnector(ssl=False)) as session: # 创建一次会话用于所有的请求
            # all_titles = []
            tasks = []

            for journal in select_data:
                task = asyncio.create_task(
                    fetch_and_extract(journal, current_proxy, start_year, end_year, keyword, session))
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)

    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")


if __name__ == "__main__":
    display_credits_and_notes()
    all_titles = []
    current_proxy = None
    # 选择研究的方向
    data, current_proxy = get_research_directions(current_proxy)
    href = choose_direction(data)
    while True:
        valid_input = False  # A flag to track if the input is valid
        while not valid_input:
            try:
                # Get user input for start and end years and keyword

                keyword = input(eval(random.choice(choices)) + "请输入研究的关键词：")
                start_year = input(eval(random.choice(choices)) + "请输入开始年份：")
                end_year = input(eval(random.choice(choices)) + "请输入结束年份：")

                # Attempt to convert years to integers and validate
                start_year = int(start_year)
                end_year = int(end_year)
                if start_year > end_year:
                    raise ValueError(Fore.RED + "开始年份不能晚于结束年份！！！")
                valid_input = True  # If inputs are valid, set the flag to True
            except ValueError as e:
                # If there is a ValueError, print the error and the loop will continue
                print(Fore.RED + f"输入错误: {e}")

        # # 选择研究的方向
        # data, current_proxy = get_research_directions(current_proxy)
        # href = choose_direction(data)
        # 选择期刊种类
        type_choice = choose_journal_type()
        print('\n')
        # 打印出来
        select_data = get_selected_journal_info(href, type_choice, current_proxy)
        print('\n')

        print(eval(random.choice(choices)) + '正在全力搜索中(代理IP效率有限，请耐心等待)......\n')

        # 运行主函数
        asyncio.get_event_loop().run_until_complete(main(start_year, end_year, keyword))

        all_titles = set(all_titles)

        sum_article = len(all_titles)

        print('\n')

        print(f"一共找到包含关键词的文章总数：{Fore.RED + str(sum_article)}\n")

        # 判断是否有获取到标题
        if all_titles:
            # 询问用户是否保存
            save_choice = input(eval(random.choice(choices)) + "是否将标题保存到本地？(y/n): \n")

            # 如果用户选择保存
            if save_choice.lower() == 'y':
                while True:  # 开始循环以确保用户提供正确的输入
                    # 用户输入1保存为文本，输入2保存为Excel
                    format_choice = input(eval(random.choice(choices)) + "请选择保存格式（输入 '1' 为文本，'2' 为Excel）: ")
                    print('\n')
                    if format_choice == '1':
                        # 保存为文本格式
                        save_titles_to_txt(all_titles, sum_article, keyword, start_year, end_year, 'journal_titles.txt')
                        print(eval(random.choice(choices)) + "标题已保存到文本文件。\n")
                        break  # 成功保存后退出循环
                    elif format_choice == '2':
                        # 保存为Excel格式
                        save_titles_to_excel(all_titles, sum_article, keyword, start_year, end_year,
                                             'journal_titles.xlsx')
                        print(eval(random.choice(choices)) + "标题已保存到Excel文件。\n")
                        break  # 成功保存后退出循环
                    else:
                        print(Fore.RED + "输入有误，请输入 '1' 或 '2' 选择保存格式。\n")
            else:
                print(Fore.RED + "未保存标题。\n")
        else:
            print(Fore.RED + "没有找到相关的标题！！！\n")

        # 询问用户是否继续
        user_choice = input(eval(random.choice(choices)) + "是否继续（输入 'q' 退出，其他键继续）: ")
        print('\n')
        if user_choice.lower() == 'q':
            print(eval(random.choice(choices)) + '已成功退出！！！\n')
            break  # 如果用户输入 'q'，则退出循环



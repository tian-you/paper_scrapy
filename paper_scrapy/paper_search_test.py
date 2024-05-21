import re
import time
from lxml import html
import requests
from bs4 import BeautifulSoup


def get_proxy():
    # 5000：settings中设置的监听端口，不是Redis服务的端口
    return requests.get("http://127.0.0.1:6666/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:6666/delete/?proxy={}".format(proxy))


# 2. 验证代理IP可用性
def verify_proxy(proxy):
    # 构造请求头，模拟浏览器请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    # 请求目标网页并判断响应码
    url = "http://www.baidu.com"
    try:
        response = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)}, timeout=5)
        if response.status_code == 200:
            print("可以用")
            return True
        else:
            return False
    except:
        return False


# 网址访问函数
def get_response(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    while True:
        proxy = get_proxy().get("proxy")
        if verify_proxy(proxy):
            response = requests.get(url, headers=headers, proxies={"http": "http://{}".format(proxy)})
            return response
        else:
            proxy = get_proxy().get("proxy")


# 搜索论文专用
def extract_volumes(url, start_year, end_year, keyword):

    etree = html.etree
    response = get_response(url)
    parser = etree.HTMLParser()
    tree = etree.fromstring(response.content, parser)

    # 使用xpath找到正确的ul标签
    ul_content = tree.xpath('//*[@id="main"]/ul')[0]

    # 使用BeautifulSoup解析该ul的内容
    soup = BeautifulSoup(etree.tostring(ul_content), 'lxml')

    # 获取所有li标签
    li_elements = soup.find_all('li')
    # print(li_elements)

    volumes_to_visit = []
    for li in li_elements:
        # 尝试提取li标签内部的文本中的四位数字作为年份
        year = re.search(r'\d{4}', li.text)
        if year:
            year = year.group()
        else:
            year = "Unknown"

        # print(year)
        if start_year <= int(year) <= end_year:
            # 获取当前li标签下的所有a标签
            a_elements = li.find_all('a')
            hrefs = [a.get("href") for a in a_elements]
            print(f"Year: {year}")
            # 计数专用
            sum1 = 0
            for href in hrefs:
                print(f"  - {href}")
                # volumes_to_visit = []
                volumes_to_visit.append(href)

                response = get_response(href)
                # response.encoding = 'utf-8'  # 手动指定字符编码为utf-8
                print('访问此链接进行搜索......')
                html_content = response.content
                # html_content = html_content.encode('utf-8')

                # 使用BeautifulSoup解析HTML
                soup = BeautifulSoup(html_content, 'lxml')

                # 定位标签
                title_tags = soup.find_all('span', {'class': 'title', 'itemprop': 'name'})
                titles = []
                # 提取标签内容
                if title_tags:
                    for title in title_tags:
                        # print(span_tag.text)
                        # 使用正则表达式查找包含关键字 'Federated Learning' 的<span>标签文本
                        # if title and re.search(r'\b{}\b'.format(re.escape(keyword)), title.text, re.IGNORECASE):
                        keywords = keyword.split()
                        # 构建正则表达式，确保句子包含所有关键词
                        pattern = r'(?=.*\b' + r'\b)(?=.*\b'.join(
                            [re.escape(keyword) for keyword in keywords]) + r'\b).*\.'
                        if title and re.search(pattern, title.text, re.IGNORECASE):
                            titles.append(title.text)
                            print(title.text)
                            sum1 += 1
                else:
                    print("标签未找到")

            print(f"找到包含关键词的标题总数：{sum1}")


if __name__ == '__main__':

    # 示例
    url = "https://dblp.uni-trier.de/db/journals/joc/index.html"
    start_year = 2021
    end_year = 2023
    keyword = "Federated Learning"
    extract_volumes(url, start_year, end_year, keyword)

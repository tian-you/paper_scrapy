"""
paper_ultra的测试程序
"""
import asyncio
import json
import logging
import aiohttp
import random

import pandas as pd
import requests
from aiohttp import TCPConnector, ClientTimeout
from lxml import etree

proxy = None
# 数据初始化，读取JSON文件并转换为字典(用于进行分类)
with open('Journal_Articles.json', 'r', encoding='utf-8') as json_file:
    Journal_Articles = json.load(json_file)
with open('Conference_and_Workshop_Papers.json', 'r', encoding='utf-8') as json_file:
    Conference_and_Workshop_Papers = json.load(json_file)

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='test.log',  # 日志输出到文件
    filemode='w'  # 追加模式
)


async def get_proxy(session):
    # 5000：settings中设置的监听端口，不是Redis服务的端口
    # async with aiohttp.ClientSession() as session:
    async with session.get("http://123.57.226.67:6666/get/") as res:
        return await res.json()


async def delete_proxy(prox, session):
    # async with aiohttp.ClientSession() as session:
    await session.get(f"http://123.57.226.67:6666/delete/?proxy={prox}")


# 2. 验证代理IP可用性
async def verify_proxy(prox, session):
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
    header = {'User-Agent': random.choice(user_agent_list)}

    # 请求目标网页并判断响应码
    u = "http://www.baidu.com"
    try:
        # 注意这里使用了 await 来等待异步操作的结果
        async with session.get(u, headers=header, proxy=f"http://{prox}", timeout=10) as res:
            # 这里也需要使用 await 来等待 raise_for_status 的结果
            res.raise_for_status()
            return True
    except aiohttp.ClientError as e:
        logging.error(f"代理 {proxy} 验证失败: {e}")
        return False


# 网址访问函数
async def get_response(u, i, session, qe):
    global proxy
    param = {
        'q': qe,
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
    header = {'User-Agent': random.choice(user_agent_list)}

    while True:
        # if proxy is None:
        #     proxy_info = await get_proxy(session)  # 使用 await 调用异步函数
        #     if not proxy_info:
        #         logging.error("无法获取代理")
        #         return None
        #     proxy = proxy_info.get("proxy")
        #     logging.info(f"使用新代理: {proxy}")
        #
        # if not await verify_proxy(proxy, session):  # 使用 await 调用异步函数
        #     await delete_proxy(proxy, session)  # 使用 await 调用异步函数
        #     proxy = None
        #     continue
        try:
            async with session.get(u, params=param, headers=header) as res:
                res.raise_for_status()
                return await res.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(f"请求异常: {e}")
            # await delete_proxy(proxy, session)
            # proxy = None
        except Exception as e:
            logging.error(f"未预料的错误: {e}")
            proxy = None


async def fetch(u, i, session, q):
    retries = 0
    max_retries = 100
    while retries < max_retries:
        try:
            res = await get_response(u, i, session, q)  # 确保传递正确的参数以获取不同页的结果
            return res
        except Exception as e:
            # 如果发生异常，记录或处理它，并进行重试
            logging.error(f"在获取和提取过程中发生错误: {e}, 正在重试... ({retries + 1}/{max_retries})")
            # print(f"在获取和提取过程中发生错误: {e}, 正在重试... ({retries + 1}/{max_retries})")
            retries += 1
            await asyncio.sleep(1)  # 增加延迟避免立即重试可能导致的问题


journal_data_lock = asyncio.Lock()
global_journal_data = []


async def parse(html_content, choices):
    tree = etree.HTML(html_content)

    if choices == 'Journal_Articles':
        li_tags = tree.xpath('//li[@class="entry article toc"]')
    else:
        li_tags = tree.xpath('//li[@class="entry inproceedings toc"]')

    j_data = []

    for li in li_tags:
        title_list = li.xpath('.//span[@class="title" and @itemprop="name"]//text()')
        title = ''.join(title_list).strip()
        # title = title_list[0].strip() if title_list else "Title not found"

        publisher_list = li.xpath('.//a/span/span[@itemprop="name"]/text()')
        publisher = publisher_list[0].strip() if publisher_list else "Publisher not found"

        years_list = li.xpath('.//span[@itemprop="datePublished"]/text()')
        year = years_list[0].strip() if years_list else "Year not found"

        j_data.append({
            'title': title,
            'publisher': publisher,
            'year': year
        })

    async with journal_data_lock:
        global_journal_data.extend(j_data)


async def main(total, qury, cho):
    u = 'https://dblp.uni-trier.de/search/publ/inc'
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=10),
                                         connector=TCPConnector(ssl=False)) as session:  # 创建一次会话用于所有的请求

            tasks = []
            for i in range(0, int(total) // 30 + 1):
                ts = asyncio.create_task(fetch(u, i, session, qury))
                tasks.append(ts)  # 创建异步获取任务
            print('并发执行所有获取任务')
            pages_content = await asyncio.gather(*tasks, return_exceptions=True)

        tasks = []
        for html_content in pages_content:
            ts = asyncio.create_task(parse(html_content, cho))
            tasks.append(ts)  # 创建解析任务

        print('并发执行所有的解析任务')
        await asyncio.gather(*tasks, return_exceptions=True)  # 并发执行所有的解析任务

    except Exception as e:
        print(f"An error occurred: {e}")


def create_journal_entry(title, typ, years):
    # 将年份列表转换成字符串，并用'|'符号连接
    years_str = '|'.join(map(str, years))
    # 根据输入拼接字符串
    entry = f"title:{title} type:{typ}:year:{years_str}"
    return entry


def save_titles_to_excel(titles_A, titles_B, titles_C, sum_article, keyword, star, en, file_name):
    # 根据提供的titles数据结构，指定列名
    column_names = ['Title', 'Journal', 'Year']
    file_name = f"{keyword}_{str(star)}_{str(en)}_{'共'+str(sum_article)+'篇'}_{file_name}"

    # 创建ExcelWriter对象，用于写入Excel文件
    excel_writer = pd.ExcelWriter(file_name, engine='openpyxl', mode='w')

    # 将titles_A写入到Sheet1
    df_a = pd.DataFrame(titles_A, columns=column_names)
    df_a.to_excel(excel_writer, sheet_name='A类', index=False)

    # 将titles_B写入到Sheet2
    df_b = pd.DataFrame(titles_B, columns=column_names)
    df_b.to_excel(excel_writer, sheet_name='B类', index=False)

    # 将titles_C写入到Sheet3
    df_c = pd.DataFrame(titles_C, columns=column_names)
    df_c.to_excel(excel_writer, sheet_name='C类', index=False)

    # 保存并关闭ExcelWriter对象
    # excel_writer.save()
    excel_writer.close()
    # 生成文件名
    # file_name = f"{keyword}_{str(star)}_{str(en)}_{str(sum_article)}_{file_name}"


if __name__ == '__main__':

    title_input = None

    # journal_data = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                      "537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    input_valid = False
    while not input_valid:
        title_input = input("请输入标题：").strip()

        print("您输入的标题是：", title_input)
        confirm = input("确认输入正确吗？(Y/N): ")

        if confirm.upper() == 'Y':
            input_valid = True
        elif confirm.upper() == 'N':
            print("请重新输入标题。")
        else:
            print("无效的选择，返回重新输入标题。")

    input_valid = False
    type_input = None
    while not input_valid:
        choice = input("请输入数字选择内容：1. Journal_Articles  2. Conference_and_Workshop_Papers: ")
        if choice == '1':
            type_input = 'Journal_Articles'
            input_valid = True
        elif choice == '2':
            type_input = 'Conference_and_Workshop_Papers'
            input_valid = True
        else:
            print("错误：请输入1或2进行选择。")
    # 假设用户可以输入多个年份，以逗号分隔
    while True:
        try:
            start_year = int(input("请输入开始年份："))
            end_year = int(input("请输入结束年份："))

            if start_year > end_year:
                print("错误：开始年份不能大于结束年份，请重新输入。")
                continue

            break
        except ValueError:
            print("错误：请输入有效的整数年份。")

    year_list = [str(year) for year in range(start_year, end_year + 1)]
    # 调用函数并打印结果
    journal_entry = create_journal_entry(title_input, type_input, year_list)

    url = ('https://dblp.uni-trier.de/search/publ/api?callback=jQuery31109242945945981864_1699447770265&q=' +
           journal_entry.replace("type:", "%20type:") +
           '&compl=year&p=2&h=0&c=10&rw=3d&format=jsonp&_=1699447770266')
    # print(url)
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

    asyncio.get_event_loop().run_until_complete(main(total_hits, journal_entry, type_input))  # 运行异步主函数

    # print(global_journal_data)  # 打印结果
    # 用于存储分类结果
    Journal_A = []
    Journal_B = []
    Journal_C = []

    Conference_A = []
    Conference_B = []
    Conference_C = []

    # 输出配对结果
    print(type_input)
    for journal in global_journal_data:
        if type_input == 'Journal_Articles':
            if journal['publisher'] in Journal_Articles['A']:
                Journal_A.append(journal)
            elif journal['publisher'] in Journal_Articles['B']:
                Journal_B.append(journal)
            elif journal['publisher'] in Journal_Articles['C']:
                Journal_C.append(journal)

        else:
            if journal['publisher'] in Conference_and_Workshop_Papers['A']:
                Conference_A.append(journal)
            elif journal['publisher'] in Conference_and_Workshop_Papers['B']:
                Conference_B.append(journal)
            elif journal['publisher'] in Conference_and_Workshop_Papers['C']:
                Conference_C.append(journal)

    if type_input == 'Journal_Articles':
        ja = []
        jb = []
        jc = []
        # 检查是否搜索成功
        print('总共', len(global_journal_data), '篇文章！\n')
        if int(total_hits) == len(global_journal_data):
            print('搜索成功！！！')
        else:
            print('搜索失败！！！')

        # 输出类别A的文章
        print("Category A articles:")
        print(len(Journal_A))
        for j in Journal_A:
            print(j['title'])
            ja.append((j['title'], j['publisher'], j['year']))

        # # 输出类别B的文章
        print("\nCategory B articles:")
        print(len(Journal_B))
        for j in Journal_B:
            print(j['title'])
            jb.append((j['title'], j['publisher'], j['year']))

        # 输出类别C的文章
        print("\nCategory C articles:")
        print(len(Journal_C))
        for j in Journal_C:
            print(j['title'])
            jc.append((j['title'], j['publisher'], j['year']))

        save_titles_to_excel(ja, jb, jc, len(global_journal_data), title_input, start_year,
                             end_year, 'journal_titles.xlsx')
    else:
        ca = []
        cb = []
        cc = []
        # 检查是否搜索成功
        print('总共', len(global_journal_data), '篇会议！\n')
        if int(total_hits) == len(global_journal_data):
            print('搜索成功！！！')
        else:
            print('搜索失败！！！')

        # 输出类别A的文章
        print("Category A conferences:")
        print(len(Conference_A))
        for c in Conference_A:
            print(c['title'])
            ca.append((c['title'], c['publisher'], c['year']))

        # # 输出类别B的文章
        print("\nCategory B conferences:")
        print(len(Conference_B))
        for c in Conference_B:
            print(c['title'])
            cb.append((c['title'], c['publisher'], c['year']))

        # 输出类别C的文章
        print("\nCategory C conferences:")
        print(len(Conference_C))
        for c in Conference_C:
            print(c['title'])
            cc.append((c['title'], c['publisher'], c['year']))

        save_titles_to_excel(ca, cb, cc, len(global_journal_data), title_input, start_year,
                             end_year, 'conference_titles.xlsx')

import requests
from bs4 import BeautifulSoup

# 获取网页内容
url = "https://www.ccf.org.cn/Academic_Evaluation/NIS/"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')


# 创建一个函数来提取信息
def extract_info(category):
    data = []
    ul = soup.find('h3', {'id': category}).find_next('ul')
    for li in ul.find_all('li')[1:]:  # 跳过第一个li，因为它是标题
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


# 提取A类和B类的信息
a_class_data = extract_info('16420')
b_class_data = extract_info('16421')
c_class_data = extract_info('16422')

print("A类：")
for item in a_class_data:
    print(f"刊物全称: {item['full_name']}")
    print(f"出版社: {item['publisher']}")
    print(f"地址: {item['address']}")
    print("------")

print("\nB类：")
for item in b_class_data:
    print(f"刊物全称: {item['full_name']}")
    print(f"出版社: {item['publisher']}")
    print(f"地址: {item['address']}")
    print("------")

print("\nC类：")
for item in c_class_data:
    print(f"刊物全称: {item['full_name']}")
    print(f"出版社: {item['publisher']}")
    print(f"地址: {item['address']}")
    print("------")

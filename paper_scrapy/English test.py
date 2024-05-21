from curl_cffi import requests
url = 'https://s.weibo.com/weibo?q=%E5%A4%A9%E6%B4%A5%E9%AB%98%E6%A0%A1%E8%B4%AB%E5%9B%B0%E7%94%9F%E5%8A%A9%E5%AD%A6%E9%87%91&page=2'

response = requests.get(url=url, impersonate="chrome101")
# s = requests.Session()
# s.get(url=url)
# print(s.cookies)
print(response.content)


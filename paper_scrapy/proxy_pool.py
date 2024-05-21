"""
代理池使用相关代码
"""
import requests


def get_proxy():
    # 5000：settings中设置的监听端口，不是Redis服务的端口
    return requests.get("http://123.57.226.67:6666/get/").json()


def count_proxy():
    return requests.get('http://123.57.226.67:6666/count').json()


def delete_proxy(proxy):
    requests.get("http://123.57.226.67:6666/delete/?proxy={}".format(proxy))


# 主代码
def getHtml():
    retry_count = 5
    proxy = get_proxy().get("proxy")
    print(proxy)
    while retry_count > 0:
        try:
            html = requests.get('http://www.baidu.com', proxies={"http": "http://{}".format(proxy)})
            print(html.text)
            break
        except Exception:
            retry_count -= 1
            # 删除代理池中代理
    delete_proxy(proxy)
    return None


print(count_proxy())
# getHtml()

import requests
import os
import random
from datetime import datetime
from notify import send
from bs4 import BeautifulSoup

def get_proxy():
    urls_str = os.getenv('sock_proxy', '')
    
    # 使用换行符分割 URL
    urls = [url.strip() for url in urls_str.split('\n') if url.strip()]
    #随机选择一个ip
    url = random.choice(urls)
    #获取ip地址并打印
    response = requests.get("https://api.ipify.org", proxies={"http": url, "https": url} )
    print("代理ip地址：",response.text)
    return url

def parse_gpu_data(bs):
    result = []
    
    ul = bs.find('ul', class_='product-list')
    for item in ul.find_all('li', class_='mk2TagParm'):
        item_data = {
            "name": item['mk2pname'].strip(),
            "url": "https://www.kojima.net" + item.find('a', class_='mk2TagClick')['href']
        }
        result.append(item_data)

    return result

def get_kojima_stock(url):
    proxy = get_proxy()
    response = requests.get(url, proxies={"http": proxy, "https": proxy})
    bs = BeautifulSoup(response.text, 'html.parser')
    gpu_data = parse_gpu_data(bs)
    return gpu_data;

if __name__ == "__main__":
    url =  os.getenv('kojima_url', '')
    stock_info = get_kojima_stock(url)

    for item in stock_info:
        print(item['name'])
        send(
                    title='🎯 コジマ 发现目标商品！',
                    content=f'''## {item['name']}

> **直达链接：**
> [点击购买]({item['url']})

---'''
            )
import requests
import json
import os
import random
from notify import send
import cloudscraper
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
    
    # 遍历所有商品
    for item in bs.find_all('div', class_='item_listbox'):        
        # 提取商品信息
        item_data = {
                    "item_name": item.find('li', class_='itemname1').text.strip(),
                    "price": item.find('div', class_='price_box').text.strip(),
                    "stock": "在庫あり" in item.find('span', class_='cart-stat').text.strip(),
                    "url": "https://www.ark-pc.co.jp" + item.find('a', class_='t_open')['href']
                }        
        result.append(item_data)
    
    return result

def get_ark_stock(url):
    proxy = get_proxy()
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, proxies={"http": proxy, "https": proxy})
    bs = BeautifulSoup(response.text, 'html.parser')
    gpu_data = parse_gpu_data(bs)
    return gpu_data;

if __name__ == "__main__":
    url =  os.getenv('ark_url', '')
    stock_info = get_ark_stock(url)
    #空数组的话，打出没有库存
    if not stock_info:
        print("没获取到商品信息")
    else:
        # 检查状态是否改变
        for item in stock_info:
            if item['stock']:
                print("商品已上库存：",item['item_name'])
                send(
                        title='🎯 ark 发现目标商品！',
                        content=f'''## {item['item_name']}
价格：{item['price']}

> **直达链接：**
> [点击购买]({item['url']})

---'''
                    )
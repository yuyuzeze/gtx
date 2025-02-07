import requests
import json
import os
import random
from notify import send
from datetime import datetime

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

def parse_gpu_data(str):
    json_text = str.replace('xsearchCallback(', '').rstrip(');')    
    json_obj = json.loads(json_text)
    return json_obj

def get_koubou_stock(url):
    proxy = get_proxy()
    response = requests.get(url, proxies={"http": proxy, "https": proxy})
    gpu_data = parse_gpu_data(response.text)
    return gpu_data;

if __name__ == "__main__":
    weburl =  os.getenv('pc_koubou_url', '')
    current_time = datetime.now()
    time_str = current_time.strftime("%Y%m%d%H%M%S")
    model = "G.P.U.%23%23GeForce%20RTX%204060"
    timestamp = int(current_time.timestamp() * 1000)
    #url = f"https://www.pc-koubou.jp/search/npsearch.php?time={time_str}&path=%E8%87%AA%E4%BD%9CPC%E3%83%91%E3%83%BC%E3%83%84%3A%E3%82%B0%E3%83%A9%E3%83%95%E3%82%A3%E3%83%83%E3%82%AF%E3%82%AB%E3%83%BC%E3%83%89&sn1[]={model}&s1=1&n16c=1%3A50&sort=number11&limit=15&cache_t=30&callback=xsearchCallback&fmt=jsonp&s2b=%E9%80%9A%E5%B8%B8&_={timestamp}"
    url = f"{weburl}"    
    stock_info = get_koubou_stock(url)
    
    if len(stock_info["kotohaco"]["result"]["items"]) > 0:
        for item in stock_info:
            if item['stock']:
                print("商品已上库存：",item['title'])
                url = "https://www.pc-koubou.jp" + item['url']
                send(
                        title='🎯 pc-koubou 发现目标商品！',
                        content=f'''## {item['title']}

> **直达链接：**
> [点击购买]({url})

---'''
                    )
    else:
        print("没有库存")
        
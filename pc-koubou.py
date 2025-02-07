import requests
import json
import os
from notify import send
from datetime import datetime
import cloudscraper

def get_proxy():
    url = os.getenv('http_proxy')
    #获取ip地址并打印
    #response = requests.get("https://api.ipify.org", proxies={"http": url, "https": url} )
    #print("代理ip地址：",response.text)
    return url

def parse_gpu_data(str):
    json_text = str.replace('xsearchCallback(', '').rstrip(');')
    json_obj = json.loads(json_text)
    return json_obj

def get_koubou_stock(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.pc-koubou.jp/',
        'Origin': 'https://www.pc-koubou.jp',
        'Connection': 'keep-alive'
    }
    proxy = get_proxy()
    gpu_data = None
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, headers=headers, proxies={"http": proxy, "https": proxy})
    if response.status_code == 403:
        print("403 error！")
    else:
        gpu_data = parse_gpu_data(response.text)
    return gpu_data;

if __name__ == "__main__":
    weburl =  os.getenv('pc_koubou_url', '')
    current_time = datetime.now()
    time_str = current_time.strftime("%Y%m%d%H%M%S")
    model = "G.P.U.%23%23GeForce%20RTX%205090"
    timestamp = int(current_time.timestamp() * 1000)
    url = f"https://www.pc-koubou.jp/search/npsearch.php?time={time_str}&path=%E8%87%AA%E4%BD%9CPC%E3%83%91%E3%83%BC%E3%83%84%3A%E3%82%B0%E3%83%A9%E3%83%95%E3%82%A3%E3%83%83%E3%82%AF%E3%82%AB%E3%83%BC%E3%83%89&sn1[]={model}&s1=1&n16c=1%3A50&sort=number11&limit=15&cache_t=30&callback=xsearchCallback&fmt=jsonp&s2b=%E9%80%9A%E5%B8%B8&_={timestamp}"
    print(url)
    stock_info = get_koubou_stock(url)
    
    if stock_info and len(stock_info["kotohaco"]["result"]["items"]) > 0:
        for item in stock_info["kotohaco"]["result"]["items"]:
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
        
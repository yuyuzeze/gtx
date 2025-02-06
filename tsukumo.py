import requests
import json
import os
import random
from notify import send
from bs4 import BeautifulSoup

def get_proxy():
    urls_str = os.getenv('sock_proxy', '')
    
    # 使用换行符分割 URL
    urls = [url.strip() for url in urls_str.split('\n') if url.strip()]
    #随机选择一个ip
    url = random.choice(urls)
    #获取ip地址并打印
    response = requests.get("https://api.ip.sb/ip")
    print("代理ip地址：",response.text)
    return url

def parse_gpu_data(bs):
    result = {"makers": []}
    
    # 遍历所有厂商区块
    items_section = bs.find('section', id='items')
    for maker_section in items_section.find_all('h3', class_='tc'):
        maker_data = {
            "name": maker_section.text,
            "items": []
        }
        
        # 找到该厂商下的所有商品
        item_list = maker_section.find_next('div', class_='item_list')
        if item_list:
            for item in item_list.find_all('div', class_='item'):
                # 提取商品信息
                item_data = {
                    "item_name": item.find('div', class_='item_name').text.strip(),
                    "price": item.find('span', class_='price').text.strip(),
                    "detail_button": item.find('div', class_='detail_button').text.strip()
                }
                maker_data["items"].append(item_data)
        
        result["makers"].append(maker_data)
    
    return result

def get_tsukumo_stock(url):
    proxy = get_proxy()
    response = requests.get(url, proxies={"http": proxy, "https": proxy})
    bs = BeautifulSoup(response.text, 'html.parser')
    gpu_data = parse_gpu_data(bs)
    return gpu_data;

def get_5090_details(stock_info):
    if not stock_info or 'makers' not in stock_info:
        return {}
    
    return {item['item_name']: item['detail_button'] 
            for maker in stock_info['makers'] 
            for item in maker['items'] 
            if '5090' in item['item_name']}

if __name__ == "__main__":
    url =  os.getenv('tsukumo_url', '')
    #url = "https://shop.tsukumo.co.jp/features/rtx-50/"
    stock_info = get_tsukumo_stock(url)
    stock_info_last = None
    
    #如果文件存在，则读取文件
    if os.path.exists('tsukumo_gpu_data.json'):
        with open('tsukumo_gpu_data.json', 'r') as f:
            stock_info_last = json.load(f)
    
    # 比较新旧数据
    details_current = get_5090_details(stock_info)
    details_last = get_5090_details(stock_info_last)

    # 检查状态是否改变
    for name, button in details_current.items():
        if name in details_last and details_last[name] == button:
            continue
        else:
            print(name, button)
            send(
                        title='🎯 ツクモ 发现目标商品！',
                        content=f'''## {name}

> **直达链接：**
> [点击购买]({url})

---'''
                    )

    with open('tsukumo_gpu_data.json', 'w') as f:
        json.dump(stock_info, f)
    

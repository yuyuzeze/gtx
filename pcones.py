import requests
import os
import random
import subprocess
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
    current_item = {}
    
    table_ele = bs.find('table', id='product_list')
    for tr in table_ele.find_all('tr'):
        # 找到商品名
        name_td = tr.find('td', class_='list_name')
        if name_td:
            if current_item:  
                result.append(current_item)
            current_item = {}
            current_item['name'] = name_td.text.strip()
            current_item['url'] = "https://www.1-s.jp" + name_td.find('a')['href']
            continue
            
        # 找到库存状态
        stock_td = tr.find('td', class_='list_stock')
        if stock_td:
            no_stock_img = stock_td.find('img')
            if no_stock_img:
                current_item['in_stock'] = False
            else:
                current_item['in_stock'] = True
                
    if current_item:
        result.append(current_item)

    return [item for item in result if item.get('in_stock', False)]

def get_pc4u_stock(url):
    proxy = get_proxy()
    ones_session = os.getenv('pcones_session', '')
    cmd = f'''curl --location '{url}' \
        --proxy '{proxy}' \
        --header 'Cookie: ones_session={ones_session}' '''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    bs = BeautifulSoup(result.stdout, 'html.parser')
    gpu_data = parse_gpu_data(bs)
    return gpu_data;

if __name__ == "__main__":
    url = os.getenv('pcones_url', '')
    stock_info = get_pc4u_stock(url)

    for item in stock_info:
        print(item['name'])
        send(
                    title='🎯 PCones 发现目标商品！',
                    content=f'''## {item['name']}

> **直达链接：**
> [点击购买]({item['url']})

---'''
            )
import aiohttp
import asyncio
import json
import os
from notify import send
from bs4 import BeautifulSoup

def get_urls():
    urls_str = os.getenv('amazon_urls', '')
    
    # 使用换行符分割 URL
    urls = [url.strip() for url in urls_str.split('\n') if url.strip()]
    return urls

async def fetch_amazon_product(url):
    params = {
        "linkCode": "sl1",
        "tag": "twm1a4080-22",
        "linkId": "387fac7c4d0581478539f94f3afea1ff",
        "language": "ja_JP",
        "ref_": "as_li_ss_tl"
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "device-memory": "4",
        "downlink": "10",
        "dpr": "1",
        "ect": "4g",
        "priority": "u=0, i",
        "rtt": "50",
        "sec-ch-device-memory": "4",
        "sec-ch-dpr": "1",
        "sec-ch-ua": '"Chromium";v="129", "Not=A?Brand";v="8"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua-platform-version": '"6.0"',
        "sec-ch-viewport-width": "400",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
        "viewport-width": "400"
    }

    amazon_cookies = json.loads(os.environ.get("AMAZON_COOKIES", "{}"))
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, headers=headers, cookies=amazon_cookies) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"请求失败，状态码：{response.status}")
                    return None
        except Exception as e:
            print(f"发生错误：{str(e)}")
            return None

URLS = get_urls()

async def main():
    for url in URLS:
        result = await fetch_amazon_product(url)
        if result:
            print("请求成功！")
            soup = BeautifulSoup(result, 'html.parser')
            try:
                add_to_cart_element = soup.find('input', {'id': 'add-to-cart-button'})
                if add_to_cart_element:
                    product_title = soup.find('meta', attrs={'name': 'title'})['content']
                    
                    # 发送通知
                    send(
                        title='Amazon 发现目标商品！',
                        content=f'''商品名: {product_title}  
商品链接: [点击购买]({url})

---
原始链接: {url}'''
                    )
                    print("已发送库存通知")
                else:
                    print("商品暂无库存")
                
            except Exception as e:
                print(f"检查库存时出错: {str(e)}")
    
if __name__ == "__main__":
    asyncio.run(main())















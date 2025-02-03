import aiohttp
import asyncio
import json
import os

async def fetch_amazon_product():
    url = "https://www.amazon.co.jp/gp/product/B0BSLJ52ZF"
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

async def main():
    result = await fetch_amazon_product()
    if result:
        print("请求成功！")
        # 这里可以添加处理响应数据的代码
    
if __name__ == "__main__":
    asyncio.run(main())















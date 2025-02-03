from PyCookieCloud import PyCookieCloud
import json
import os

def update_amazon_cookies():
    try:
        # 获取CookieCloud数据
        cookie_cloud = PyCookieCloud('https://cookiecloud.ddsrem.com', 'sYpzgkTvGpQvJjBkgSTpZZ', 'u3Sd9YPe8EX4iBq4vKg6in')
        decrypted_data = cookie_cloud.get_decrypted_data()
        
        # 提取amazon.co.jp的cookies
        amazon_cookies = {}
        if "amazon.co.jp" in decrypted_data:
            for cookie in decrypted_data["amazon.co.jp"]:
                amazon_cookies[cookie['name']] = cookie['value']
        
        # 将cookies保存到环境变量
        if amazon_cookies:
            cookie_str = json.dumps(amazon_cookies)
            os.environ["amazon_cookies"] = cookie_str
            print("Amazon cookies 更新成功！")
            return True
        else:
            print("未找到 Amazon cookies！")
            return False
            
    except Exception as e:
        print(f"更新 cookies 时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    update_amazon_cookies()
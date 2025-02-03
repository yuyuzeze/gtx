from PyCookieCloud import PyCookieCloud
import json
import os

def update_amazon_cookies():
    try:
        # 获取CookieCloud数据
        cookie_cloud = PyCookieCloud(os.environ.get("cookie_cloud_url"), os.environ.get("cookie_cloud_uuid"), os.environ.get("cookie_cloud_pwd"))
        decrypted_data = cookie_cloud.get_decrypted_data()
        
        # 提取amazon.co.jp的cookies
        amazon_cookies = {}
        if "amazon.co.jp" in decrypted_data:
            for cookie in decrypted_data["amazon.co.jp"]:
                amazon_cookies[cookie['name']] = cookie['value']
        
        # 将cookies保存到文件
        if amazon_cookies:
            cookie_str = json.dumps(amazon_cookies)
            cookie_file = "amazon_cookies.json"
            with open(cookie_file, "w") as f:
                f.write(cookie_str)
            print(f"Cookies 已保存到 {cookie_file}")
            return True
        else:
            print("未找到 Amazon cookies！")
            return False
            
    except Exception as e:
        print(f"保存 cookies 时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    update_amazon_cookies()
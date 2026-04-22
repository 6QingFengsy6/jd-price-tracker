import time
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import requests
import pickle

def get_jd_price_selenium(sku_id):
    edge_options = Options()
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    edge_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Edge(options=edge_options)
    
    try:
        print("正在打开京东首页...")
        driver.get('https://www.jd.com/')
        
        print("\n请在弹出的浏览器中完成登录：")
        print("1. 点击页面上的「请登录」或「你好，请登录」")
        print("2. 用手机京东APP扫码登录")
        print("3. 登录成功后，回到这里按回车键")
        print("注意：浏览器不会自动关闭，请放心操作\n")
        
        # 等待用户手动登录
        input("登录完成后，按回车键继续...")
        
        # 保存登录信息
        with open('jd_cookies.pkl', 'wb') as f:
            pickle.dump(driver.get_cookies(), f)
        print("登录信息已保存")
        
        # 访问商品页面
        url = f'https://item.jd.com/{sku_id}.html'
        print(f"正在打开商品页: {url}")
        driver.get(url)
        time.sleep(5)
        
        # 获取价格
        price = None
        try:
            price_elem = driver.find_element(By.CSS_SELECTOR, '#price, .price, .p-price')
            price_text = price_elem.text
            import re
            match = re.search(r'(\d+\.?\d*)', price_text)
            if match:
                price = float(match.group(1))
        except:
            pass
        
        if price is None:
            page_text = driver.page_source
            import re
            matches = re.findall(r'¥(\d+\.?\d*)', page_text)
            if matches:
                price = float(matches[0])
        
        driver.quit()
        return price
        
    except Exception as e:
        print(f"获取失败: {e}")
        driver.quit()
        return None

def send_wechat(title, content):
    sckey = "SCT341099TLZEIv2uz1fS1gb9AIAlThZFj"
    url = f"https://sc.ftqq.com/{sckey}.send"
    data = {"text": title, "desp": content}
    try:
        requests.post(url, data=data)
        print("微信通知已发送")
    except Exception as e:
        print(f"微信通知发送失败: {e}")

def save_price_history(price):
    with open("price_history.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()},{price}\n")

def get_last_notify_price():
    if os.path.exists("last_notify_price.txt"):
        try:
            with open("last_notify_price.txt", "r") as f:
                return float(f.read().strip())
        except:
            return None
    return None

def save_last_notify_price(price):
    with open("last_notify_price.txt", "w") as f:
        f.write(str(price))

TARGET_PRICE = 400
SKU_ID = "10175657056098"

print(f"正在查询京东商品 {SKU_ID} 的价格...")

current_price = get_jd_price_selenium(SKU_ID)

if current_price is None:
    print("价格获取失败，请重试")
    exit()

now = datetime.now()
print(f"检查时间: {now}")
print(f"当前价格: {current_price} 元")
print(f"目标价格: {TARGET_PRICE} 元")

save_price_history(current_price)

last_notify = get_last_notify_price()

if current_price < TARGET_PRICE:
    if last_notify is None or current_price < last_notify:
        print(f"价格 {current_price} 元，发送微信通知")
        send_wechat(
            "京东降价提醒",
            f"商品当前价格 {current_price} 元，已低于目标价 {TARGET_PRICE} 元！\n点击购买：https://item.jd.com/{SKU_ID}.html"
        )
        save_last_notify_price(current_price)
    else:
        print(f"价格未低于上次通知价 {last_notify}，不重复通知")
else:
    print("价格未达标，不发送通知")

print("完成")
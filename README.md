# 京东商品价格监控爬虫

Python + Selenium 实现的京东价格监控工具，价格低于目标价时通过微信自动推送通知。

## 功能特点

- 模拟浏览器登录，突破反爬
- 微信实时推送降价提醒
- 只在新低价时通知，不重复打扰
- 自动保存价格历史

## 技术栈

- Python 3.14
- Selenium
- Edge WebDriver
- Server酱（微信推送）

## 环境要求

- Windows 10/11
- Python 3.7+
- Edge 浏览器 (Chromium内核)

> 需要下载与你的 Edge 浏览器版本匹配的 **Edge WebDriver**，并将其放入项目根目录。
> 下载地址：[Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

## 快速开始

1. 安装依赖：pip install selenium requests
2. 修改 test.py 中的 TARGET_PRICE 为目标价格
3. 修改 SKU_ID 为商品ID
4. 注册 Server酱 获取 SCKEY 填入代码
5. 运行：python test.py

## 作者

GitHub: 6QingFengsy6

import os
import time
import requests
import schedule
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve

# 创建保存图片的目录
save_dir = "ld"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 要请求的URL
url = "https://data.cma.cn/data/online.html?dataCode=RAD__B0_CR&dataTime=20241003053000"

def fetch_and_save_images():
    try:
        # 请求页面
        response = requests.get(url)
        response.raise_for_status()
        
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到包含 "image.data.cma.cn/vis/" 的图片链接
        for img_tag in soup.find_all('img'):
            img_url = img_tag.get('src')
            if "image.data.cma.cn/vis/" in img_url:
                # 完整的图片URL
                full_img_url = urljoin(url, img_url)
                # 生成保存路径
                img_name = os.path.join(save_dir, os.path.basename(img_url))
                
                # 下载图片
                urlretrieve(full_img_url, img_name)
                print(f"已下载: {img_name}")
    
    except Exception as e:
        print(f"发生错误: {e}")

# 先获取一次图片
fetch_and_save_images()

# 定时任务：每6分钟执行一次
schedule.every(6).minutes.do(fetch_and_save_images)

print("开始执行定时任务，每6分钟请求并保存图片...")

# 循环执行定时任务
while True:
    schedule.run_pending()
    time.sleep(1)

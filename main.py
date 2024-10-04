import os
import requests
from datetime import datetime, timedelta, timezone
import time

# 创建ld文件夹（如果不存在）
os.makedirs('E:/ld', exist_ok=True)

while True:
    # 获取当前UTC时间并减去20分钟
    utc_now = datetime.now(timezone.utc) - timedelta(minutes=18)

    # 格式化URL参数（使用UTC时间）
    year = utc_now.strftime("%Y")
    month = utc_now.strftime("%m")
    day = utc_now.strftime("%d")
    time_str = utc_now.strftime("%Y%m%d%H%M00")

    # 构建图片URL
    url = f"http://image.nmc.cn/product/{year}/{month}/{day}/RDCP/medium/SEVP_AOC_RDCP_SLDAS3_ECREF_ACHN_L88_PI_{time_str}000.PNG"

    # 获取当前时间（UTC+8）用于保存文件名
    local_now = utc_now + timedelta(hours=8)
    print(f"Downloading from URL: {url}")

    # 下载图片
    response = requests.get(url)
    if response.status_code == 200:
        # 重命名文件为保存时间（UTC+8）
        filename = f"E:/ld/{local_now.strftime('%Y%m%d%H%M%S')}.PNG"
        try:
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"图片保存成功！文件名: {filename}")
        except Exception as e:
            print(f"保存文件时出错: {e}")
    else:
        print("下载失败！状态码:", response.status_code)

    # 等待6分钟
    time.sleep(60)  # 360秒 = 6分钟

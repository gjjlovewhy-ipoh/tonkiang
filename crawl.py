import requests
import re
import time

# 你提供的真实手机浏览器 UA
USER_AGENT = "Mozilla/5.0 (Linux; Android 14; V2352GA) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.200 Mobile Safari/537.36 VivoBrowser/28.9.0.3"

# 目标地址
BASE_URL = "http://tonkiang.us/"
TARGET_URLS = [
    "http://tonkiang.us/?iptv=955227985",
    "http://tonkiang.us/?iptv=%E5%8D%97%E9%80%9A"
]

# 完整模拟手机端请求头
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Referer": "http://tonkiang.us/",
    "Upgrade-Insecure-Requests": "1"
}

# 匹配页面上 频道名,直播地址 文本行
REGEX_LINE = re.compile(r'([^,\n]+?)\s*,\s*(http[s]?://[^ \n<"]+)')

def main():
    # 维持会话，保存Cookie，绕过人机检测
    session = requests.Session()
    session.headers.update(HEADERS)

    # 第一步：先访问首页建立会话和Cookie，模拟真人访问
    try:
        session.get(BASE_URL, timeout=20)
        time.sleep(2)  # 模拟人为浏览延迟
    except Exception as e:
        print(f"首页访问失败: {e}")

    all_channel = []

    # 第二步：逐个访问目标 IPTV 链接
    for url in TARGET_URLS:
        try:
            resp = session.get(url, timeout=20)
            resp.encoding = "utf-8"
            html = resp.text

            # 提取所有频道和流地址
            items = REGEX_LINE.findall(html)
            for name, link in items:
                name = name.strip()
                link = link.strip()
                if name and link:
                    all_channel.append((name, link))
            print(f"成功抓取: {url} 拿到 {len(items)} 条")
        except Exception as e:
            print(f"抓取失败 {url}: {str(e)}")

    # 第三步：生成标准 #genre# 分组订阅 txt
    with open("iptv.txt", "w", encoding="utf-8") as f:
        # 分组头格式
        f.write("nttv,#genre#\n")
        # 写入所有频道
        for name, link in all_channel:
            f.write(f"{name},{link}\n")

    print(f"总计抓取 {len(all_channel)} 条直播源，已写入 iptv.txt")

if __name__ == "__main__":
    main()

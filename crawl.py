import requests
import re
import time

# 你的手机浏览器UA
UA = "Mozilla/5.0 (Linux; Android 14; V2352GA) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.200 Mobile Safari/537.36 VivoBrowser/28.9.0.3"
# 固定频道名称
FIX_NAME = "南通新闻综合"

# 目标两个地址
URLS = [
    "http://tonkiang.us/?iptv=955227985",
    "http://tonkiang.us/?iptv=%E5%8D%97%E9%80%9A"
]

HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "http://tonkiang.us/",
    "Connection": "keep-alive"
}

# 正则：匹配所有 http/https 完整链接，不限后缀
REG_URL = re.compile(r'https?://[^ \n\r<>"\']+')

def main():
    sess = requests.Session()
    sess.headers.update(HEADERS)

    # 先访问首页 过机器人验证 保存Cookie
    try:
        sess.get("http://tonkiang.us/", timeout=20)
        time.sleep(2)
    except:
        pass

    all_links = set()

    for url in URLS:
        try:
            res = sess.get(url, timeout=20)
            res.encoding = "utf-8"
            html = res.text

            # 提取页面所有 http/https 链接
            links = REG_URL.findall(html)
            for link in links:
                # 过滤掉本站自身链接，只保留直播源
                if "tonkiang.us" not in link:
                    all_links.add(link.strip())

            print(f"【{url}】抓到 {len(links)} 个链接")
        except Exception as e:
            print(f"访问失败 {url}：{e}")

    # 生成订阅格式 txt
    with open("iptv.txt", "w", encoding="utf-8") as f:
        f.write("nttv,#genre#\n")
        for link in sorted(all_links):
            f.write(f"{FIX_NAME},{link}\n")

    print(f"\n总计有效直播链接：{len(all_links)} 条")

if __name__ == "__main__":
    main()

# 请求头
headers = {
    "cookie": r"_ga=GA1.2.1734072428.1636705875; has_js=1; _gid=GA1.2.1656587261.1637463907",
    "user-agent": r"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
# https://www.iwara.tv/videos?f%5B0%5D=created%3A2021&f%5B1%5D=created%3A2021-11
# 代理配置
proxies = {
    "http": "http://127.0.0.1:10810",
    "https": "http://127.0.0.1:10810"
}
# 正则提取详情页链接
detail_regx = r'<a href="(.*?)">.*</a>'

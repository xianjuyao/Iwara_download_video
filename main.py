import requests
import re
from bs4 import BeautifulSoup
from utils import headers, proxies, detail_regx


# 1.请求视频预览页获取视频的详情链接
# 2.通过详情页拿到下载的链接
# 3.下载视频

# 1.请求视频预览页获取视频的详情链接
def get_videos_name(pages=1, year=2021, month=11):
    video_name = []
    # https://www.iwara.tv/videos?f%5B0%5D=created%3A2021&f%5B1%5D=created%3A2021-11&page=0
    for page in range(0, pages):
        url = f"https://www.iwara.tv/videos?f%5B0%5D=created%3A{year}&f%5B1%5D=created%3A{year}-{month}&page={page}"
        print(url)
        res = requests.get(url, headers=headers, proxies=proxies)  # 请求获取html源码
        html = res.content.decode()  # 转换成字符串
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.findAll("h3", class_="title"):  # 找出所有详情页的链接
            item = str(item)  # 转换成字符串对象
            url = re.findall(detail_regx, item)[0]  # 正则查找链接
            url = url.split("/")[-1]  # 获取视频的名字
            video_name.append(url)
    if len(video_name) > 0:
        return video_name
    else:
        print("输入的年份、月份或者页数有问题")
        return None


#
#  api:https://www.iwara.tv/api/video/2n1mktze3ahqlb1pq
# [
#     {
#         "resolution": "Source",
#         "uri": "//yukari.iwara.tv/file.php?expire=1637505983&hash=950de66cbb43024a5faebb1734dbed4ffd1d6f8b&file=2021%2F11%2F21%2F1637477477_2N1mkTzE3AHqLb1pq_Source.mp4&op=dl&r=0",
#         "mime": "video/mp4"
#     },
#     {
#         "resolution": "540p",
#         "uri": "//yukari.iwara.tv/file.php?expire=1637505983&hash=af27fa8684d7e4665da0111ec2153060668feb5d&file=2021%2F11%2F21%2F1637477477_2N1mkTzE3AHqLb1pq_540.mp4&op=dl&r=0",
#         "mime": "video/mp4"
#     },
#     {
#         "resolution": "360p",
#         "uri": "//miki.iwara.tv/file.php?expire=1637505983&hash=6f19175b868f5c8564c240890368f82b7a0543d6&file=2021%2F11%2F21%2F1637477477_2N1mkTzE3AHqLb1pq_360.mp4&op=dl&r=0",
#         "mime": "video/mp4"
#     }
# ]

# 解析出下载视频链接地址
def get_video_download_urls(video_name=""):
    res = requests.get(f"https://www.iwara.tv/api/video/{video_name}", proxies=proxies, headers=headers)
    down_list = res.json()  # 返回一个列表
    # //yukari.iwara.tv/file.php?expire=1637507023&hash=efb7fe463ec9057a938ce2b0d80ccf815fffd762&file=2021%2F11%2F21%2F1637477477_2N1mkTzE3AHqLb1pq_Source.mp4&op=dl&r=0
    if len(down_list) != 0:
        download_url = down_list[0]["uri"]  # 取得url
        # 缺少https 加上https
        download_url = r"https:" + download_url
        return download_url
    else:
        print(f"{video_name}下载失败.....")
        return None


# 下载保存视频
def download_video(download_url):
    if download_url is not None:  # 下载链接有一部分可能为None
        size = 0  # 当前下载数据量
        chunk_size = 1024  # 每次下载数据量
        file_name = download_url.split("&")[-3].split("_", 1)[1]  # 截取url链接作为文件名 2N1mkTzE3AHqLb1pq_Source.mp4
        print(f"{file_name} 正在下载中.....")
        try:
            res = requests.get(download_url, proxies=proxies, headers=headers, stream=True)
            content_size = int(res.headers["content-length"])  # 内容总大小
            if res.status_code == 200:
                with open(rf"G:\python\videos\{file_name}", 'wb') as f:
                    for chunk in res.iter_content(chunk_size=chunk_size):  # 每次下载1KB 1024字节
                        if chunk:
                            f.write(chunk)
                            size += len(chunk)
                            print(
                                "\r" + f"[下载进度]:[{'>' * int(size * 50 / content_size)}]{float(size / content_size):.2%}",
                                end="")
                print()  # 换行
                print(f"{file_name} 下载完毕.")
        except Exception as e:
            print(e)
            print("文件下载失败，请检查网络问题")


def user_interface():
    print("========================欢迎使用下载器====================================")
    while True:
        try:
            year = int(input("请输入下载的年份:"))
            month = int(input("请输入下载的月份:"))
            pages = int(input("请输入下载的页数:"))
            return [pages, year, month]
        except ValueError:
            print("请输入正确的值!")


def main():
    pages, year, month = user_interface()
    video_names = get_videos_name(pages, year, month)
    for name in video_names:
        download_url = get_video_download_urls(name)
        download_video(download_url)
    print("所有任务结束....")


if __name__ == '__main__':
    main()

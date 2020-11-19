import requests
import re

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
}


def get_cid_name(url):
    response = requests.get(url, headers=header)
    text = response.text  # 获取cid
    cid_obj = re.search(r'cid=([\d]+)', text)
    # 获取视频名
    name_obj = re.search(
        r' <title data-vue-meta="true">(.*?)_.*?</title>', text)
    name = name_obj(1)
    return cid_obj.group(1), name_obj(1)


# 保存文件
def save(url, name):
    response = requests.get(url, headers=header)
    # 不设置编码的话会导致乱码
    response.encoding = 'utf-8'
    text = response.text
    with open('J://video//{}.xml'.format(name), 'w', encoding='utf-8') as fp:
        fp.write(text)


def main():
    video_url = 'https://www.bilibili.com/video/BV15D4y197NU'
    danmaku_url = 'http://comment.bilibili.com/{}.xml'
    cid, name = get_cid_name(video_url)
    danmaku_url = danmaku_url.format(cid)
    save(danmaku_url, name)


if __name__ == "__main__":
    main()

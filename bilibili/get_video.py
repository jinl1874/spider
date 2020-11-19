# 实现功能，将 bilibili 的视频以及封面弹幕下载到特定的地方。
import requests
import re
import json
import os
from moviepy.editor import *


# 请求视频的请求头
headers_1 = {
    'Accept': '*/*',
    'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'TE': 'Trailers',
    'Range': 'bytes=0-',
    'Origin': 'https://www.bilibili.com',
    'Connection': 'keep-alive',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
}


# 请求许可的请求头
headers_2 = {
    'Host': 'cn-gdgz4-cmcc-v-10.bilivideo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': '*/*',
    'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'range',
    'Referer': 'https://www.bilibili.com/video/BV1by4y1z76X',
    'Origin': 'https://www.bilibili.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

# 普通请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
}

video_json = {
}


# 弹幕的xml文件
def get_xml(res: requests.session().get):
    text = res.text
    # 获取cid
    cid = re.findall(r'cid=([\d]+)', text)[0]
    return cid


# 获取封面的url地址
def get_cover(res: requests.session().get):
    text = res.text
    cover_url = re.findall(
        r'<meta data-vue-meta="true" itemprop="image" content="(.*?)">', text)[0]
    video_json['cover'] = cover_url
    return cover_url


# 得到视频以及音频的下载链接
def get_av_url(res: requests.session().get):
    text = res.text
    text = re.findall(r'<script>window.__playinfo__=(.*?)</script>', text)[0]
    json_data = json.loads(text)
    video = json_data['data']['dash']['video']
    audio = json_data['data']['dash']['audio']

    # 一般有多种格式可选，优先选1080p，没有就选720p。什么？没有720p！这样的视频还有下载的必要？
    video_url = json_data['data']['dash']['video'][0]['baseUrl']
    audio_url = json_data['data']['dash']['audio'][0]['baseUrl']

    # video_json['duration'] = json_data['data']['dash']['duration']
    return video_url, audio_url


def get_name(res: requests.session().get):
    text = res.text
    name = re.findall(r'<span class="tit">(.*?)</span>', text)[0]
    video_json['title'] = name
    if not name:
        # 如果名字没找到，那就用 BV号来代替
        name = re.findall(r'/video/(.*?)$', res.url)
    elif len(name) > 30:
        # 如果名字过长，就取前20对反爬虫策略有一定的反制手段，如使用代理IP、设置随机访问时间、获取ajax等个字符
        name = name[:30]
    return name


def download(session: requests.session(), url, name, cid, cover_url, v_url, a_url, index):

    # 设置基本路径
    base_path = r'E:\bilibili\download'
    print("视频：{} 开始下载……\n".format(name))
    path = os.path.join(base_path, name)
    if not os.path.exists(path):
        os.mkdir(path)

    # 设置请求头 Referer 属性
    headers_1['Referer'] = url
    headers_2['Referer'] = url

    # 获取准许
    session.options(v_url, headers=headers_2)
    session.options(a_url, headers=headers_2)

    # 获取数据
    video_content = session.get(v_url, headers=headers_1).content
    audio_content = session.get(a_url, headers=headers_1).content

    audio_name = os.path.join(path, '{}.mp3'.format(index))
    video_name = os.path.join(path, '{}.flv'.format(index))

    xml = 'http://comment.bilibili.com/{}.xml'.format(cid)
    video_json['danmaku_{}'.format(index)] = xml
    # 获取弹幕
    danmaku = session.get(xml, headers=headers)
    danmaku.encoding = 'utf-8'

    # 获取封面
    cover = session.get(cover_url, headers=headers).content

    # 保存
    with open(audio_name, 'wb') as fp:
        fp.write(audio_content)
        print("音频下载完成。\n")

    with open(os.path.join(path, cid+'.xml'), 'w', encoding='utf-8') as fp:
        fp.write(danmaku.text)
        print("弹幕下载完成。\n")

    with open(os.path.join(path, 'cover.jpg'), 'wb') as fp:
        fp.write(cover)
        print("封面下载完成。\n")

    with open(video_name, 'wb') as fp:
        fp.write(video_content)
        print("视频下载完成。\n")

    with open(os.path.join(path, 'video.json'), 'w', encoding='utf-8') as fp:
        text = json.dumps(video_json)
        fp.write(text)
    return video_name, audio_name, path


def merge(video_name, audio_name, index, path):
    print("合并开始……\n")
    # 合并音频视频
    video = VideoFileClip(video_name)
    audio = AudioFileClip(audio_name)
    new_video = video.set_audio(audio)
    new_video.to_videofile(os.path.join(
        path, '{}.mp4'.format(index)), fps=24, remove_temp=False)
    os.remove(video_name)
    os.remove(audio_name)

    print("合并结束\n")


def main():
    print("开始……\n")
    # 需要发送两个option请求，分别获取到下载视频以及音频的许可，所以需要使用session保存信息
    session = requests.session()
    # 视频的地址，可改为控制台输入
    url = input("输入视频的地址，如果要下载特定的分P，填入指定的分P地址，下载视频数设为1，从第1p开始。否则填入基本的视频地址\n>>>")
    # url = 'https://www.bilibili.com/video/BV1Q54y1m7uY'

    start_num = int(input("从第几P开始？\n>>>"))
    p_num = int(input("一共下载多少P视频?\n>>>"))

    for i in range(start_num, start_num + p_num):
        if p_num != 1:
            url += "?p={}".format(i)
        res = session.get(url, headers=headers)
        name = get_name(res)
        cover_url = get_cover(res)
        cid = get_xml(res)
        v_url, a_url = get_av_url(res)
        v_name, a_name, path = download(
            session, url, name, cid, cover_url, v_url, a_url, i)
        merge(v_name, a_name, i, path)
    print("结束……\n")


if __name__ == '__main__':
    main()

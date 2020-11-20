import requests
import re
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}


def get_video_urls(url):
    res = requests.get(url, headers=headers)
    # 获取答案url上的id
    answer_id = re.findall(r'answer/(\d+)', url)[0]

    # 获取json文本
    text = res.text
    json_text = re.findall(
        r'<script id="js-initialData" type="text/json">(.*?)</script>', text)[0]

    # 提取答案的content文件。
    data = json.loads(json_text)
    content = data['initialState']['entities']['answers'][answer_id]['content']
    # 提取url
    video_urls = re.findall(r'(https://www.zhihu.com/zvideo/\d+)', content)
    return video_urls


def get_name_url(url):
    get_video_url = 'https://lens.zhihu.com/api/v4/videos/{}'
    # 找到 json_url 的id
    res = requests.get(url, headers=headers)
    url = re.findall(
        '<iframe class="ZVideo-player" src=\"(.*?)\"', res.text)[0]
    video_id = re.findall(r'/video/(\d+)', url)[0]
    # 合并
    json_url = get_video_url.format(video_id)

    # 获取真实的视频url
    res = requests.get(json_url, headers=headers)
    data = json.loads(res.text)
    # 可选 LD 和 SD，不过一般选最清晰的 HD
    HD_url = data['playlist']['HD']['play_url']

    title = data['title']
    video_name = title + '.mp4'
    return video_name, HD_url


def save(name, url):
    res = requests.get(url, headers=headers)
    with open(name, 'wb') as fp:
        fp.write(res.content)


def main():
    url = 'https://www.zhihu.com/question/398940907/answer/1275941024'
    urls = get_video_urls(url)
    for i in urls:
        name, HD_url = get_name_url(i)
        save(name, HD_url)


if __name__ == "__main__":
    main()

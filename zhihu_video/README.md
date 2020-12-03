#! https://zhuanlan.zhihu.com/p/302410625
![Image](https://pic4.zhimg.com/80/v2-bb617555b12dd3be6c590dc0f4239893.jpg)

# 使用 Python 爬取知乎答案上的视频

## 分析

老规矩，先抓包。随便进入一个[视频页面](https://www.zhihu.com/question/398940907/answer/1275941024)，进入开发者模式，选择网络，再筛选为 XHR。
很快啊，啪的一下进来，就找到了这么一个请求。
![Image](https://pic4.zhimg.com/80/v2-7e27c91b207ddb2c058ade3d4ca5b3c1.png)
再点开这个 json，发现里面这么些数据：
![Image](https://pic4.zhimg.com/80/v2-ca4e22e60affb10e8da45280f9600d69.png)
很明显，这里面有三个不同清晰度的视频，分别是 LD、HD、SD。点开里面的'play_url'之后，就会提示下载一个视频文件。这已经很明显了，这就是我们要找的视频地址。

那要怎么获取呢？

先看下 url，是这样的——(https://lens.zhihu.com/api/v4/videos/1254186650735267840)，前面的都是不变的，只有后面ID是动态的。
那么首要任务就是将这个 ID 找出来，在网页代码搜索一下，发现为空。
由于新版的知乎视频里，在答案上插入视频需要将视频发表到另一个地方，所以试着找一下在答案找到这个视频的地址。然后再去访问一下那里，看有没有这个 ID。

很明显，我们在答案的代码中找到了视频的 url 地址，在一个 `<script id="js-clientConfig" type="text/json">`标签里，有一个整个页面的 json 文件，包括了题目、答案和作者等详细信息，而视频 url 也在里面。

使用正则表达式提取出来，再去访问视频的 url。在视频的网页页面下，搜索一下视频 ID，果然在里面。
![Image](https://pic4.zhimg.com/80/v2-a67f2f921865a245851fdc95abb8a7a5.png)

所以这就很简单了。

## 思路

1. 先获取答案上的所有的视频 url；
2. 再分别访问视频，获取一个返回包含视频信息的 json 的 url；
3. 从 json 上获取到真实的视频 url 地址；
4. 访问，再保存；

## 提取 url

```python
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

```

## 获取真实的视频地址以及标题

```python
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
```

## 保存

```python
def save(name, url):
    res = requests.get(url, headers=headers)
    with open(name, 'wb') as fp:
        fp.write(res.content)
```

## 完整代码

[Github|spider](https://github.com/jinl1874/spider/tree/master/zhihu_video)

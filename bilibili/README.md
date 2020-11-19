#! https://zhuanlan.zhihu.com/p/300700424
![Image](https://pic4.zhimg.com/80/v2-7845078e3c79cca06685bd947ee64e1f.jpg)

# 详细解析 Python 爬取 bilibili 的视频、弹幕以及封面

### 环境

用到的 Python 库：

- Python 3.7
- requests
- moviepy
- json
- re
- os

浏览器：Firefox/ 83.0

### 访问测试

打开一个视频网址，如(https://www.bilibili.com/video/BV1E4411e7ir)，然后直接打开发者工具，转到网络，选择XHR文件，再点击播放视频。可以看到很快就传输了很多文件。
![Image](https://pic4.zhimg.com/80/v2-85113af77b767f72731b2ca03aaa5b2f.png)
可以看出有两种不同的文件，一种是 30280，另一种是 30080。

因为 B 站是把音频和视频分开传输的，所以很明显，一种是视频，另一种就是音频。按大小来分的话，30080 是视频，30280 是音频文件。

首先用试着获取其中的一个文件，来测试一下。
先把请求视频 url 复制下来，再把请求头弄下来，接着发送个请求。

```python
import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'TE': 'Trailers',
    'Range': 'bytes=1431-391742',
    'Origin': 'https://www.bilibili.com',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.bilibili.com/video/BV1E4411e7ir',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
}

url = 'https://upos-sz-mirrorks3.bilivideo.com/upgcxcode/40/06/91280640/91280640-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1605719498&gen=playurl&os=ks3bv&oi=2028921166&trid=cfe12b1b9d1b4b58bf13bb1d08429d3au&platform=pc&upsig=00dbb5691fd73fdc2b8e3a834e50ad15&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=11418834&orderid=0,3&agrr=0&logo=80000000'

res = requests.get(url, headers=headers)

with open('test.flv', 'wb') as fp:
    fp.write(res.content)
```

然而请求之后发现 flv 文件是空的，再看一下发回的请求文本，显示 403 禁止错误：

```html
<html>
  <head>
    <title>403 Forbidden</title>
  </head>
  <body bgcolor="white">
    <center><h1>403 Forbidden</h1></center>
    <hr />
    <center>QCMAS/V2</center>
  </body>
</html>
```

再仔细观察一下抓包情况，在发送请 get 请求之前，浏览器会发送两个 options 请求，应该是请求许可的意思。分别是请求音频许可和请求视频许可，因为请求 url 与请求音视频的 url 相同。
![Image](https://pic4.zhimg.com/80/v2-5153a353ee437a06f7138f8f320da5bc.png)
那么用 session 来发送请求，保存好信息，再去请求链接。修改一下代码：

```python
import requests

# 请求音视频的请求头
headers_1 = {
    'Accept': '*/*',
    'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'TE': 'Trailers',
    'Range': 'bytes=1431-391742',
    'Origin': 'https://www.bilibili.com',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.bilibili.com/video/BV1E4411e7ir',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
}

# 请求的OPTIONS的请求头
headers_2 = {
    'Host': 'cn-gdgz4-cmcc-v-10.bilivideo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': '*/*',
    'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'range',
    'Referer': 'https://www.bilibili.com/video/BV1E4411e7ir',
    'Origin': 'https://www.bilibili.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

url = 'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/40/06/91280640/91280640-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1605752758&gen=playurl&os=cosbv&oi=2028921166&trid=18e55ae8ed4d41018ee9374a63501860u&platform=pc&upsig=346e8bea6d225d1ea592bb5a0c470c48&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=11418834&orderid=0,3&agrr=1&logo=80000000'

session = requests.session()

session.get(url, headers=headers_2)
res = session.get(url, headers=headers_1)

with open('test.flv', 'wb') as fp:
    fp.write(res.content)
```

可以看到，test.flv 有文件大小了。
![Image](https://pic4.zhimg.com/80/v2-ebf0c0dbd2661b9c39a7d2fa25468338.png)

但打开时显示解析错误：
![Image](https://pic4.zhimg.com/80/v2-472360a7dc6b6cac2c2142ca3603df29.png)

再看一下多个不同请求的请求头，只有 range 发生明显的改变，而且 range 的值里的 bytes 参数，说明这很有可能是一个下载的文件大小范围。那么找到最后一个发送视频请求的的包，把最大值复制下来，然后再设置请求头里的 range 值为 0-最大值，即`'Range':'bytes=0-29271958'`，然后再次运行 py 文件。很明显这次请求回来的文件比之前的大了许多，再点击播放，解析成功，有画面，但是没有声音。
![Image](https://pic4.zhimg.com/80/v2-b85b56c06b33bba13b8b7c410033649e.png)

### 找到 url 地址

要找到请求 url 肯定不能在在抓包里找到，可以尝试看下网页的源代码。
复制一点 url 的信息，在网页中查找，果然找到了信息。
![Image](https://pic4.zhimg.com/80/v2-589145616caa6133d318734f71e06d21.png)
这些信息存在 `window.__playinfo__` 里，然后把这个 json 提取出来，放到一个 json 文件里，再用 Firefox 打开。

![Image](https://pic4.zhimg.com/80/v2-a89fee6326296fbdc82bc033e8422ec2.png)

![Image](https://pic4.zhimg.com/80/v2-6304876f124845ac5ed37c19d9062638.png)
可以看到，视频的 url 信息就在 'video' 这个键里面，id 指的就是请求的质量，对应着上面的 accept_quality，`'id': 116`指就是高清 1080p60。
视频的在里面，那么音频的 url 也在 `audio`这个键里面。

提取也很容易，先把 `window._playinfo` 用正则表达式获取到，再将其转为 python 的 json 对象，然后就可以取出来了。

请求的 range 参数怎么设置呢？可以把其删去，或者设为`'range': 'bytes=0-'`，这样就会请求一个全文件了。

```python
## 请求视频页面，注意此时的请求头不是同一个
res = session.get(url, headers=headers)
text = res.text
text = re.findall(r'<script>window.__playinfo__=(.*?)</script>', text)[0]
json_data = json.loads(text)
# 一般有多种格式可选，优先选1080p，没有就选720p。什么？没有720p！这样的视频还有下载的必要？
v_url = json_data['data']['dash']['video'][0]['baseUrl']
a_url = json_data['data']['dash']['audio'][0]['baseUrl']

# 获取准许
session.options(v_url, headers=headers_2)
session.options(a_url, headers=headers_2)

# 获取数据
video_content = session.get(v_url, headers=headers_1).content
audio_content = session.get(a_url, headers=headers_1).content

# 保存
with open('test.mp3', 'wb') as fp:
   fp.write(audio_content)

with open('test.flv, 'wb') as fp:
   fp.write(video_content)
```

### 弹幕

要获取 B 站的弹幕，首先得知道 B 站的弹幕文件是从哪加载的。B 站的弹幕文件放在`http://comment.bilibili.com/{cid}.xml`，所以要获取弹幕，就要获取 B 站的视频的 cid。
视频的 cid 号在页面也可以找到，所以用正则表达式提取。
![Image](https://pic4.zhimg.com/80/v2-135f61b5a63426a2195d960aca66ac3d.png)

```python
text = res.text
# 获取cid
cid = re.findall(r'cid=([\d]+)', text)[0]

# 获取弹幕文件
xml = 'http://comment.bilibili.com/{}.xml'.format(cid)
danmaku = session.get(xml, headers=headers)
# 不设置的话，提取会乱码
danmaku.encoding = 'utf-8'

# 保存
with open(cid+'.xml', 'w', encoding='utf-8') as fp:
    fp.write(danmaku.text)
```

### 封面

封面也可以在页面找到。

```python
text = res.text
cover_url = re.findall(
    r'<meta data-vue-meta="true" itemprop="image" content="(.*?)">', text)[0]
```

### 合并音视频

这里使用 python 的 moviepy 库，安装命令`pip install moviepy`。

导入 `from moviepy.editor import *`，然后合并导出。

```python
video = VideoFileClip(video_name)
audio = AudioFileClip(audio_name)
new_video = video.set_audio(audio)
new_video.to_videofile("test.mp4", fps=24, remove_temp=False)
os.remove(video_name)
os.remove(audio_name)
```

## 代码

完全代码查看我的 [Github 地址](https://github.com/jinl1874/spider/tree/master/bilibili)

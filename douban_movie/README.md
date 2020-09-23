## 爬取豆瓣当前地区的上映电影

### 准备

使用 requests 库以及 xpath 提取：

```powershell
pip install  requests
pip install lxml
```

### 思路

访问豆瓣的地区上映电影，将标题、评分、地区、导演、主演提取出来，再将其合成一个字符串，写入并生成一个以当前时间来命名的 TXT 文件。

### 使用

在变量 url 里可更换地区，比如把 url 里的 guangzhou 改成 beijing。

在当前文件夹下直接使用`python douban.py` 即可运行。


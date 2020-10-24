## 爬取知乎问题的所有答案

### 准备

Python 版本：3.8

用到的 python 库：requests，re，json，os

浏览器：Firefox



### 分析

知乎是采用 Ajax 技术来动态加载网页，直接请求只会返回一些文件头信息。

处理 Ajax 网页一般有两种方式，一种是使用 selenium 等无头浏览器来获取数据，另一种是通过分析网页抓包来直接访问数据源，来获取到返回的 json 数据。

第一种方式简单，但很慢，所以使用第二种方法。



打开浏览器，打开一个知乎问题，按 `ctrl + shift + i` 进入开发者模式。

选择`网络`，文件类型勾选 XHR，然后将网页往下拉，多拉几次就会发现出现这么一个文件![image-20201023192702856](http://image.jinl1874.xyz/img/20201023193603.png)

查看其响应内容：

![image-20201023192848470](http://image.jinl1874.xyz/img/20201023193555.png)

确实是其答案内容。

再观察其请求网址 (https://www.zhihu.com/api/v4/questions/361402303/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=13&platform=desktop&sort_by=default)

发现其它格式都差不多，仅有 `offset=xx`改变，容易发现其是位移值。

然后就可根据请求网址来进行爬取，返回的是一串json字符串，可根据想提取的数据进行相对应的解析。


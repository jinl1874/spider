# 获取知乎某个答案里的回答
import requests
import json
import re
import time
import os

raw_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=10&offset=0&platform=desktop&sort_by=default'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Origin': 'https://www.zhihu.com'
}

question_id = '361402303'


def get_page(url):
    response = requests.get(url=url, headers=headers)
    return response


# 解析数据
def parse(response):
    json_str = json.loads(response.text)
    data = json_str.get('data')
    question_title = data[0].get('question').get('title')
    if not os.path.exists('J:\\Desktop\\test.md'):
        with open('J:\\Desktop\\test.md', 'a', encoding='utf-8') as f:
            f.write("### {}\n\n".format(question_title))
    for i in data:
        name = i.get('author').get("name")
        answer_url = i.get('url')
        answer_url = re.sub(r'(https://www\.zhihu\.com/)api/v4/answers/(\d+)',
                            r'\1question/{}/answer/\2'.format(question_id), answer_url)
        excerpt = i.get('excerpt')
        comment_count = i.get('comment_count')
        vote_count = i.get('voteup_count')
        with open('J:\\Desktop\\test.md', 'a', encoding='utf-8') as f:
            f.write('答主：{}\n摘录：{}\n赞同数：{}，评论数：{}\n>链接：{}\n\n'.format(
                name, excerpt, vote_count, comment_count, answer_url))

    paging = json_str.get('paging')
    is_end = paging.get('is_end')
    if not is_end:
        # 如果后面还有答案，那么继续进行下一个分析
        next_url = paging.get('next')
        time.sleep(5)
        parse(get_page(next_url))
    else:
        print('It is end!')


def save(text):
    with open('test.json', 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    # 填写到知乎的问题id
    url = raw_url.format(question_id)
    response = get_page(url)
    parse(response)


if __name__ == '__main__':
    main()

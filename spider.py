import requests
import re


def get_cookie():
    '''从文件中获得cookies'''
    with open('cookie', 'r') as f:
        acookie = {}
        for line in f.read().split(";"):
            name, value = line.strip().split('=', 1)
            acookie[name] = value
        return acookie


def get_headers():
    '''获得标准头文件'''
    with open('headers', 'r') as f:
        headers = {}
        for line in f.read().split(';\n'):
            name, value = line.split(':', 1)
            headers[name] = value
        return headers


def parse_one_page(html):
    '''进行正则匹配'''
    pattern = re.compile('<div class="Card TopstoryItem.*?name="User".*?>(.*?)</a>'  #用户姓名
                         +'.*?</span></span>(.*?)</span>' #用户操作
                         +'.*?<h2 class="ContentItem-title.*?name="Title".*?>(.*?)</a' #推荐内容
                         +'.*?<meta itemprop="name" content="(.*?)"/>', re.S) #作者
    items = re.findall(pattern, html)

    for item in items:
        yield {
            'ActiveUser': item[0],
            'Active': item[1],
            'Title': item[2],
            'Author': item[3]
        }


def save_html(html):
    '''保存网页'''
    with open('html.txt', 'w', encoding='utf-8') as f:
        f.write(html)
        f.close()


def main():
    url = 'https://www.zhihu.com'
    headers = get_headers()
    cookies = get_cookie()
    s = requests.Session()
    req2 = s.get(url, headers=headers, cookies=cookies)
    html = req2.content.decode('utf-8')
    save_html(html)
    ##n = 0
    for item in parse_one_page(html):
        print(item)
        '''
        n += 1
        if n == 20:
            break
        '''


if __name__ == '__main__':
    main()

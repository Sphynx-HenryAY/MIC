import re
from urllib.request import urlopen as urllib_request_urlopen
from urllib.request import Request as urllib_request_Request
from urllib.parse import urlencode as urllib_parse_urlencode


def get_url(search_keyword):
    baidu_url_base = 'http://www.baidu.com/s?chrome=UTF-8&'
    url = ''.join([baidu_url_base, urllib_parse_urlencode({'wd': search_keyword})])
    return url


def remove_excess(string, *excess):
    if len(excess) == 1:
        return string.replace(excess, '')
    else:
        for e in excess:
            string = string.replace(e, '')
        return string
    

def get_baidu_result_1(search_keyword, page_content, pattern = 'href = "(.*?)</a>'):
    result = dict()
    for e in re.findall(pattern, page_content.replace('\n', '')):
        if 'www.baidu.com/link?url' in e:
            e = remove_excess(e, '<em>', '</em>', ' ', '\t', '\n')
            link, text = e.strip().split('"target="_blank">')
            result[link] = text
    #[print(e) for e in result.items()]
    return result


def get_baidu_result_2(search_keyword, page_content, pattern = 'href="(.*?)</a>'):
    result = dict()
    for e in re.findall(pattern, page_content.replace('\n', '')):
        if 'www.baidu.com/link?url' in e:
            link, text = e.split('"', 1)
            text = search_keyword + ' - ' + text.split('>')[-1]
            if text:
                result[link] = text.replace('<em>', '').replace('</em>', '')
    #[print(e) for e in result.items()]
    return result


def main(search_keyword):
    url = get_url(search_keyword)
    req = urllib_request_Request(url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    page_content = urllib_request_urlopen(req).read().decode('utf8')

    baidu_search_result = dict()
    #baidu_search_result.update(get_baidu_result_2(search_keyword, page_content))
    baidu_search_result.update(get_baidu_result_1(search_keyword, page_content))

    return {e[1]:e[0] for e in baidu_search_result.items()}

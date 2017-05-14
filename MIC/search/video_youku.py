import re
from urllib.request import urlopen as urllib_request_urlopen
from urllib.request import Request as urllib_request_Request
from urllib.parse import urlencode as urllib_parse_urlencode

def get_url(search_keyword):
    youku_url_base = 'http://www.soku.com/search_video/q_'
    url = youku_url_base+search_keyword.replace(' ', '%20')
    #url = ''.join([youku_url_base, urllib_parse_urlencode(search_keyword)])
    return url


def get_youku_result(search_keyword, page_content, pattern = '''_log_vid="([^"']+)"'''):
    result = dict()
    title_pattern = '''title="(.*?)" target="_blank" href="'''
    for vid_id in set(re.findall(pattern, page_content)):
        link = 'http://v.youku.com/v_show/id_' + vid_id
        link_title = re.findall(title_pattern+link, page_content)[0]
        
        result[link_title] = link
    return result


def main(search_keyword):
    url = get_url(search_keyword)
    req = urllib_request_Request(url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    page_content = urllib_request_urlopen(req).read().decode('utf8')

    return get_youku_result(search_keyword, page_content)

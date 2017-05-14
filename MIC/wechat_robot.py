import sys
import itchat
from itchat import content as itchat_content

sys.path.append('C:\\Users\\HAY\\Desktop\\Getting Started\\')

from . import wechat_search
from . import video

VideoAccess = video.VideoAccess
msg_web_search = wechat_search.msg_web_search

search_session = dict()

def add_session(curr_user):
    if curr_user not in search_session:
        search_session[curr_user] = dict()
        return '%s added'%curr_user
    else:
        return '%s exist'%curr_user

@itchat.msg_register(itchat_content.TEXT)
def personal_msg_web_search_reply(msg):
    curr_user = msg['FromUserName']

    add_session(curr_user)
    search_session[curr_user] = msg_web_search(msg, search_session[curr_user])


@itchat.msg_register(itchat_content.TEXT, isGroupChat=True)
def group_msg_web_search_reply(msg):
    if msg['isAt']:
        curr_user = msg['FromUserName']

        add_session(curr_user)
        search_session[curr_user] = msg_web_search(msg, search_session[curr_user])

itchat.auto_login(True)
itchat.run()

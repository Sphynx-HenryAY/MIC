import re
import itchat
from . import search
from . import video


def exist(keyword, msg):
    return re.search(keyword, msg.split(None, 1)[0], re.I)


def is_int(msg):
    try:
        num = eval(msg)
        if type(num) == int:
            return True
    except (NameError, SyntaxError):
        return False


def send_search_msg(session, search_result, curr_user):
    if 'reply' in session:
        itchat.revoke(session['reply'][0], session['reply'][1], curr_user)
        
    session = search_result
    
    ret_msg = ',\n'.join(['%d: %s'%e for e in enumerate(session.keys())])
    ret_msg+= '\n\nReply id to get link!\n回覆標號以獲取連結!'
    
    ret = itchat.send(ret_msg, curr_user)
    localID, msgID = ret['LocalID'], ret['MsgID']
    session['reply'] = (localID, msgID)
    
    return session


def msg_web_search(msg, session):
    print('Received:', msg['Content'])
    curr_user = msg['FromUserName']

    if exist('bd', msg['Text']):
        search_result = search.text(msg['Text'].split(None, 1)[1])
        session = send_search_msg(session, search_result, curr_user)

    elif exist('vd', msg['Text']):
        search_result = search.video(msg['Text'].split(None, 1)[1])
        session = send_search_msg(session, search_result, curr_user)
    
    elif is_int(msg['Text']) and eval(msg['Text']) < len(session.keys()):
        key = list(session.keys())[eval(msg['Text'])]
        itchat.send('%s :%s\n%s\r\n' % (msg['Text'], key, session[key]), curr_user)

    elif exist('sc', msg['Text']):
        #only message with only 'sc' will trigger this
        if 'reply' in session:
            itchat.revoke(session['reply'][0], session['reply'][1], curr_user)
        session = dict()

    return session

__author__ = 'badpoet'

import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import json

URL_LOGIN = "http://student.tsinghua.edu.cn/practiceLogin.do"


def analyze_info(s):
    # soup = BeautifulSoup(html, fromEncoding = 'gbk')
    # something = soup.findAll('span', attrs = {'class': 'uportal-navi-user'})
    # if (len(something) < 4):
        # pass
    # return (something[1].text, something[2].text)
    print "yoyo"
    obj = json.loads(s, "gbk")
    print "heihei"
    name = obj["realname"]
    print name.encode("gbk")
    id = obj["username"]
    return (name, id)

def tunet_login(username, password):
    data = (
        ('userName', username),
        ('password', password),
    )
    req = urllib2.Request(URL_LOGIN, urllib.urlencode(data))
    try:
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        if not res.strip():
            return None
        user_data = analyze_info(res)
        return {
            "id": user_data[1],
            "name": user_data[0]
        }
    except Exception, e:
        print e
        # TODO  solve exception when log in
        return None

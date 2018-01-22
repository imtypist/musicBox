# -*-coding:utf8 -*-

import json
import urllib
import urllib2
import os
import time
import itchat
import threading
from aip import AipSpeech

music_list = []

""" 你的 APPID AK SK """
APP_ID = 'App ID'
API_KEY = 'Api Key'
SECRET_KEY = 'Secret Key'

def request_ajax_url(url,body,referer=None,cookie=None,**headers):
    req = urllib2.Request(url)

    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')

    if cookie:
        req.add_header('Cookie',cookie)
    if referer:
        req.add_header('Referer',referer)
    if headers:
        for k in headers.keys():
            req.add_header(k,headers[k])

    postBody = urllib.urlencode(body)
    response = urllib2.urlopen(req, postBody)
    if response:
        return response

def music(name):
	platform_list = ["xiami","netease","qq","kugou","kuwo","migu"]
	url = "http://music.liuzhijin.cn/"
	referer = "http://music.liuzhijin.cn/"
	for index,platform in enumerate(platform_list):
		FormData = {"input": name, "filter": "name", "type": platform, "page": 1}
		res = json.loads(request_ajax_url(url, FormData, referer).read())
		if res['code'] == 200:
            for el in res['data']:
                if el['url'] and len(el['title']) <= len(name)*2:
                    result  = client.synthesis('下一首歌曲 ' + name, 'zh', 1, {'vol': 5,})
                    if not isinstance(result, dict):
                        with open('audio.mp3', 'wb') as f:
                            f.write(result)
                        os.system("mpg123 audio.mp3")
                    os.system("mpg123 " + el['url'])
                    return True
		else:
			if index == len(platform_list) - 1:
				result  = client.synthesis('没有找到歌曲 ' + name, 'zh', 1, {'vol': 5,})
                if not isinstance(result, dict):
                    with open('audio.mp3', 'wb') as f:
                        f.write(result)
                    os.system("mpg123 audio.mp3")


def worker_run():
    while True:
        if len(music_list) == 0:
            time.sleep(0.5)
        else:
            music(music_list[0])
            del music_list[0]


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    data = msg.text.split('@')
    if data[0] == u'点歌':
        music_list.append(data[1].encode('utf8'))
        return data[1] + u'已进入等待播放队列...'
    if data[0] == u'当前歌单':
        temp = u''
        for index,item in enumerate(music_list):
            temp = temp + str(index) + '.' + item.decode('utf8') + '\n'
        return temp


def wechat_run():
	itchat.auto_login(enableCmdQR=2)
	itchat.run()


if __name__ == '__main__':
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
	t = threading.Thread(target=worker_run)
	t.start()
    wechat_run()

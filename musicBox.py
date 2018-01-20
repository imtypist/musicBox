# -*-coding:utf8 -*-

import json
import urllib
import urllib2
import os
import time
import itchat
import threading

music_list = []

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
    print postBody
    response = urllib2.urlopen(req, postBody)
    if response:
        return response

def music(name):
	platform_list = ["netease","qq","kugou","kuwo","xiami","migu"]
	url = "http://music.liuzhijin.cn/"
	referer = "http://music.liuzhijin.cn/"
	for index,platform in enumerate(platform_list):
		FormData = {"input": name, "filter": "name", "type": platform, "page": 1}
		res = json.loads(request_ajax_url(url, FormData, referer).read())
		if res['code'] == 200:
			os.system("mpg123 " + res['data'][0]['url']);
			return True
		else:
			if index == len(platform_list)-1:
				print platform, u'未找到符合的歌曲，请另选曲目'
			else:
				print platform, u'未找到符合的歌曲，查找下个平台', platform_list[index+1]


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
        for item in music_list:
            temp = temp + item.decode('utf8') + '\n'
        return temp


def wechat_run():
	itchat.auto_login(enableCmdQR=2)
	itchat.run()


if __name__ == '__main__':
	threads = []
	t1 = threading.Thread(target=wechat_run)
	threads.append(t1)
	t2 = threading.Thread(target=worker_run)
	threads.append(t2)
	for t in threads:
		t.setDaemon(True)
		t.start()
	t.join()
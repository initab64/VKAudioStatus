#!/usr/bin/python

import os
import time
import re
import urllib

path = 'users/'

def write_param(user_id, name, param):
    f = open(path+user_id+'/'+name, 'wt')
    f.write(str(param))
    f.close()

def read_param(user_id, name):
    try:
	f = open(path+user_id+'/'+name, 'rt')
	res = f.read()
	f.close()
	return res
    except:
	return ''

while 1 == 1:
    for user_id in os.listdir(path):
	print user_id,
	lastfm_user = read_param(user_id, 'lastfm_user')
	access_token = read_param(user_id, 'access_token')
	last_status = read_param(user_id, 'last_status')
	print lastfm_user,
	try:
	    xml = urllib.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='+lastfm_user+'&limit=1&api_key=****************************').read()
	except:
	    continue
	r = re.search("""<track nowplaying="true">""", xml)
	try:
	    r.groups(0)
	    r = re.search("""<artist mbid="[^"]*">([^<]*)</artist>""", xml)
	    artist = r.groups(0)[0]
	    r = re.search("""<name>([^<]*)</name>""", xml)
	    track = r.groups(0)[0]
	    status = artist + ' - ' + track
	    print status
	    url = 'https://api.vk.com/method/status.set?text=Now playing: '+status+'&access_token='+str(access_token)
	    if status != last_status:
		if int(time.time()) - os.stat(path+user_id+'/last_status').st_mtime > 60 or last_status == '':
		    print urllib.urlopen(url).read()
		    write_param(user_id, 'last_status', status)
	except:
	    print 'No music'
	    if last_status != '':
		if int(time.time()) - os.stat(path+user_id+'/last_status').st_mtime > 60:
		    url = 'https://api.vk.com/method/status.set?text=&access_token='+str(access_token)
		    print urllib.urlopen(url).read()
		    write_param(user_id, 'last_status', '')

    time.sleep(10)

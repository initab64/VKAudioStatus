#!/usr/local/bin/python

import cgi
import os
import urllib
import json
import datetime

def write_param(dr, name, param):
    f = open(dr+'/'+name, 'wt')
    f.write(str(param))
    f.close()

form = cgi.FieldStorage()

print "Content-type: text/html;"
print

try:
    code = form['code'].value
except:
    print "Error! No CODE!"
    raise

f = urllib.urlopen('https://oauth.vkontakte.ru/access_token?client_id=**********&client_secret=***************&code='+code)
resp = f.read()
res = json.loads(resp)

try:
    access_token = res['access_token']
    expires_in = res['expires_in']
    user_id = res['user_id']
    dr = 'users/'+str(user_id)
    try:
	os.mkdir(dr)
    except:
	pass
    write_param(dr, 'access_token', access_token)
#    write_param(dr, 'expires_time', int((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds()))
    write_param(dr, 'lastfm_user', form['lastfm_user'].value)
    write_param(dr, 'last_status', '')
    
    print "It's OK!"

except:
    print "error"


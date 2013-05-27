__author__ = 'SolPie'
import urllib
import urllib2
import re

url = "http://l.5sing.com/HandlerMP3.ashx"


def getMP3(xml):
    p = re.compile(r'http://(.*?).mp3')
    g = p.findall(xml)
    # g=pattern.search(xml)#re.findall(regMP3,page)
    # return g[0]+'/ssss/ss.mp3'
    return xml.split('s="')[1].split('.mp3')[0] + '.mp3'


def leech5sing(c, s):
    data = {"SongType": c, "SongID": s}
    data = urllib.urlencode(data)
    req = request = urllib2.Request(url + '?' + data)
    response = urllib2.urlopen(request)
    page = response.read()
    print page
    return getMP3(page)

import urllib,urllib2,re,xbmcplugin,xbmcgui

#TV DASH - by You 2008.

def CATEGORIES():
    addDir('Seinastu sendingarnar', 'http://stream.kringvarp.fo/webservice/ripley_service.xml?media=1&sort=1&page=0', 2, '', 0)
    addLink('LIVE', 'rtmp://46.137.78.64:1935/fo', 'video', 'http://www.kringvarp.fo/MediaPlayer/ripley/Ripley.1.3.2.swf', '')
    addLink('LIVE (HQ)', 'rtmp://46.137.78.64:1935/fo', 'videohigh', 'http://www.kringvarp.fo/MediaPlayer/ripley/Ripley.1.3.2.swf', '')

def INDEX(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    match = re.compile('').findall(link)
    for thumbnail, url, name in match:
        addDir(name, url, 2, thumbnail, 0)

def VIDEOLINKS(url,name, page):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    match = re.compile('<id>(.*)</id>\n.*<title>(.*)</title>(\n.*){1,20}<publish>(.*)</publish>(\n.*){1,20}<media>(.*)</media>').findall(link)
    for nothing, name, nothing2, publish, nothing3, url in match:
        addLink(name.replace('&amp;','&') + ' : ' + publish,'rtmp://87.230.58.72:1935/vod', 'mp4:video/' +  url.upper() + '.mp4','http://www.kringvarp.fo/MediaPlayer/ripley/Ripley.1.3.2.swf','')
    addDir('Fleiri sendingar - s. ' + str(page + 1), 'http://stream.kringvarp.fo/webservice/ripley_service.xml?media=1&sort=1&page=' + str((page + 1)), 2, '', page + 1)



def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params=sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param




def addLinkOLD(name, url, iconimage):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage = iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = url, listitem = liz)
    return ok

def addLink(name, url, playpath, swfUrl, iconimage):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    liz.setProperty("SWFPlayer", swfUrl)
    liz.setProperty("PlayPath", playpath)
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = url, listitem = liz)
    #xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(url, liz)
    return ok



def addDir(name,url,mode,iconimage,page):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&page=" + str(page)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


params = get_params()
url = None
name = None
mode = None
page = 0

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
        
try:
    page = int(params["page"])
except:
    pass

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "Page: " + str(page)

if mode == None or url == None or len(url) < 1:
    print ""
    CATEGORIES()
       
elif mode == 1:
    print "" + url
    INDEX(url)
        
elif mode == 2:
    print "" + url
    VIDEOLINKS(url, name, page)



xbmcplugin.endOfDirectory(int(sys.argv[1]))

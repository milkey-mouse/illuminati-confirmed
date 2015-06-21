import os
import md5
import urllib
import platform
if "Windows" in platform.platform():
    from ctypes import *
    winmm = windll.winmm
    def mciSend(s):
        i=winmm.mciSendStringA(s,0,0,0)
        if i<>0:
            print "Error %d in mciSendString %s" % ( i, s )
class peladophobian(object):
    def __init__(self):
        pass

    def mlgsay(self, text):
        text = text.replace("Illuminati", "Illuminotty")
        payload = "<engineID>4</engineID><voiceID>5</voiceID><langID>1</langID><ext>mp3</ext>" + text
        phash = md5.new(payload).hexdigest()
        url = "http://cache-a.oddcast.com/c_fs/{0}.mp3?engine=4&language=1&voice=5&text={1}&useUTF8=1".format(phash, text)
        try:
            r = urllib.urlretrieve(url, "mlg.mp3")
        except:
            #in use or can't retrieve, just forget it
            return
        if "Windows" in platform.platform():
            mciSend("Close All")
            mciSend("Open \"mlg.mp3\" Type MPEGVideo Alias mlg")
            mciSend("Play mlg Wait")
            mciSend("Close mlg")
        else: #assuming *nix
            os.system("aplay mlg.mp3")



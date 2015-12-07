import os
import hashlib
import urllib
import requests
import platform
import time

class peladophobian(object):
    def __init__(self):
        pass

    def mlgsay(self, text):
        return mlgsay(text)

def mlgsay(text, play=True):
    payload = u"<engineID>4</engineID><voiceID>5</voiceID><langID>1</langID><ext>mp3</ext>" + text
    phash = hashlib.md5(payload.encode("utf-8")).hexdigest()
    url = u"http://cache-a.oddcast.com/c_fs/{0}.mp3?engine=4&language=1&voice=5&text={1}&useUTF8=1".format(phash, text)
    if not os.path.exists(phash+".mp3"):
        r = requests.get(url, stream=True)
        with open(phash + ".mp3", "wb") as f:
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
            f.flush()
    if play:
        os.system("ffplay mlg.mp3 -autoexit -fs -showmode 1")
    return phash + ".mp3"

if __name__ == "__main__":
    while True:
        try:
            text = None
            if sys.version_info[0] > 2:
                text = input(">>")
            else:
                text = raw_input(">>")
            mlgsay(text)
        except KeyboardInterrupt:
            break

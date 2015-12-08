import praw
from peladophobian import mlgsay
import time
import os, sys

r = praw.Reddit(user_agent="NoContext (sillystixco@hotmail.com)")
r.login(username="NoContextBot1337", password="123456")
with open("files.txt", "w") as f:
    for c in r.get_subreddit("nocontext").get_top_from_all(limit=100):
        try:
            print(c.title)
            name = mlgsay(c.title, play=False)
            f.write("file '" + name + "'\n")
            f.write("file 'silence.mp3'\n")
        except:
            pass
os.system("ffmpeg -f concat -i files.txt -c copy hax.mp3 -y")
os.system("ffplay hax.mp3 -autoexit -fs -showmode 1")

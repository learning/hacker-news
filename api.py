from threading import Thread
from urllib import request
import json

TOPSTORIES = 'https://hacker-news.firebaseio.com/v0/topstories.json'
ITEM = 'https://hacker-news.firebaseio.com/v0/item/%s.json'

class API(object):
    def top_stories(self, callback):
        return RequestThread(self, TOPSTORIES, callback).start()

    def item(self, id, callback):
        return RequestThread(self, ITEM % id, callback).start()

    def handler(self, data, callback):
        callback and callback(data)

class RequestThread(Thread):

    def __init__(self, parent, url, callback):
        self.parent = parent
        self.url = url
        self.callback = callback
        super(RequestThread, self).__init__()

    def run(self):
        r = request.urlopen(self.url)
        self.parent and self.parent.handler(
            json.loads(str(r.read(), 'utf-8')), self.callback)

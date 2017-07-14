import Thread from threading
import urllib.request
import json

TOPSTORIES = 'https://hacker-news.firebaseio.com/v0/topstories.json'
ITEM = 'https://hacker-news.firebaseio.com/v0/item/%s.json'

class Request:
    def new_thread(self):
        return RequestThread(parent=self)
    def on_thread_finished(self, thread, data):
        print thread, data

class RequestThread(Thread):

    def __init__(self, parent=None):
        self.parent = parent
        super(RequestThread, self).__init__()

    def run(self):
        self.parent and self.parent.on_thread_finished(self, 42)

    def __init__(self):

#!/usr/bin/python
import requests

class Poster(object):
    def post(data):
        url = 'https://www.herokuserver.topostto.com/data'
        data_post = requests.post(url, data)
        print(data_post.text)
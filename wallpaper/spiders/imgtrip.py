# coding: utf-8
# wallhaven.py

import sys

import os
import json
import time

import scrapy
from scrapy import Request

__parent_dir__ = os.path.split(os.path.realpath(__file__))[0] + '/../'

sys.path.append(__parent_dir__)
import settings

class ImgTripSpider(scrapy.Spider):
    name = 'imgtrip'
    write_to_path = settings.WriteToPath

    def start_requests(self):
        base_url = 'https://www.imgtrip.com/api/image/page'
        for i in range(10):
            yield Request(url=base_url, callback=self.get_urls, dont_filter=True)
    
    def get_urls(self, response):
        data = json.loads(response.body)
        
        for d in data:
            yield Request(url=d['src'], meta={'name':d['name']}, callback=self.get_image)
    
    def get_image(self, response):
        img = response.body
        with open(os.path.join(self.write_to_path, response.meta['name'].replace('/', '') + '.jpg'), 'wb') as f:
           f.write(img)
        

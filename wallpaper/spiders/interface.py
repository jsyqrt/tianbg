# coding: utf-8
# wallhaven.py

import os
import time

import scrapy
from scrapy import Request

class InterFaceSpider(scrapy.Spider):
    name = 'interface'
    write_to_path = '/home/jsyqrt/Pictures/wallpaper/'

    def start_requests(self):
        url = 'https://interfacelift.com/wallpaper/downloads/random/wide_16:9/'
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        for img_url in response.xpath('//a[starts-with(@href, "/wallpaper/") and "_5120x2880.jpg"=substring(@href, string-length(@href) - string-length("_5120x2880.jpg") + 1)]/@href').extract():
        #for img_url in response.xpath('//a[starts-with(@href, "/wallpaper/") and ends-with(@href, "_5120x2880.jpg")]/@href').extract():
            print img_url
            yield Request(
                url = 'http://interfacelift.com' + img_url,
                meta = {

                },
                callback = self.save_image,
            )

    def save_image(self, response):
        img = response.body
        with open(os.path.join(self.write_to_path, str(int(time.time() * 1000)) + '.jpg'), 'wb') as f:
           f.write(img)
        print 'finished 1 wallpaper saving.'

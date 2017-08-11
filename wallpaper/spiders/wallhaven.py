# coding: utf-8
# wallhaven.py

import os
import time

import scrapy
from scrapy import Request

class WallHavenSpider(scrapy.Spider):
    name = 'wallhaven'
    write_to_path = '/home/jsyqrt/Pictures/wallpaper/'

    def start_requests(self):
        urls = ['https://alpha.wallhaven.cc/random?page=' + str(i) for i in xrange(1, 10)]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        for img_url in response.xpath('//a[@class="preview" and starts-with(@href, "https://alpha.wallhaven.cc/wallpaper/")]/@href').extract():
            print img_url
            yield Request(
                url = img_url,
                meta = {

                },
                callback = self.get_image,
            )

    def get_image(self, response):
        img_real_url = response.xpath('//img[@id="wallpaper" and starts-with(@src, "//wallpapers.wallhaven.cc/wallpapers/full/wallhaven-")]/@src').extract_first()
        yield Request(
            url = 'https:' + img_real_url,
            meta = {

            },
            callback = self.save_image,
        )

    def save_image(self, response):
        img = response.body
        with open(os.path.join(self.write_to_path, response.url.split('/')[-1]), 'wb') as f:
           f.write(img)
        print 'finished 1 wallpaper saving.'

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


class WallHavenSpider(scrapy.Spider):
    name = 'wallhaven'
    write_to_path = settings.WriteToPath

    def start_requests(self):
        urls = ['https://wallhaven.cc/random?seed=NYJVkS&page={}'.format(str(i)) for i in range(1, 10)]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        for img_url in response.xpath('//a[@class="preview" and starts-with(@href, "https://wallhaven.cc/w/")]/@href').extract():
            yield Request(
                url = img_url,
                meta = {

                },
                callback = self.get_image,
            )

    def get_image(self, response):
        img_real_url = response.xpath('//img[@id="wallpaper" and starts-with(@src, "https://w.wallhaven.cc/full/")]/@src').extract_first()
        yield Request(
            url = img_real_url,
            meta = {

            },
            callback = self.save_image,
        )

    def save_image(self, response):
        img = response.body
        with open(os.path.join(self.write_to_path, response.url.split('/')[-1]), 'wb') as f:
           f.write(img)


# coding: utf-8

import sys

import os
import json
import datetime

import scrapy
from scrapy import Request

__parent_dir__ = os.path.split(os.path.realpath(__file__))[0] + '/../'

sys.path.append(__parent_dir__)
import settings


class CNUSpider(scrapy.Spider):
    name = 'cnu'
    write_to_path = settings.WriteToPath

    def start_requests(self):
        url = 'http://www.cnu.cc/'
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        for img_url in response.xpath('//a[@class="workCover thumbnail" and starts-with(@href, "http://www.cnu.cc/works/")]/@href').extract():
            yield Request(
                url = img_url,
                meta = {

                },
                callback = self.get_image,
            )

    def get_image(self, response):
        today = datetime.date.today()
        year = today.year
        month = today.month
        date = str(year)[2:] + str(month).zfill(2)
        xpath = '//img[starts-with(@data-original, "http://imgoss.cnu.cc/{}/")]/@data-original'.format(date)
        for img_url in response.xpath(xpath).extract():
            img_url = img_url.split('?')[0]
            yield Request(
                url = img_url,
                meta = {

                },
                callback = self.save_image,
            )

    def save_image(self, response):
        img = response.body
        with open(os.path.join(self.write_to_path, response.url.split('/')[-1]), 'wb') as f:
           f.write(img)


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-
import re
import random
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class PicscrapyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            if re.match(r'http', url):
                yield Request(url)

    # 重写函数，修改了下载图片名称的生成规则，改成了url地址的最后一个加了随机送
    def file_path(self, request, response=None, info=None):
        if not isinstance(request, Request):
            url = request
        else:
            url = request.url
        url = urlparse(url)
        img_name = url.path.split('/')[5].split('.')[0] + '-' + str(random.randint(1000, 9999))
        return '%s.jpg' % img_name

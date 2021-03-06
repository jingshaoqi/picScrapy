# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class PicscrapyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 通过meta属性传递title
        return [Request(x, meta={'title': item['title'], 'cat': item['category_name']}) for x in
                item.get(self.images_urls_field, [])]

    # 重写函数，修改了下载图片名称的生成规则
    def file_path(self, request, response=None, info=None):
        if not isinstance(request, Request):
            url = request
        else:
            url = request.url
        url = urlparse(url)
        img_name = url.path.split('/')[5].split('.')[0]
        return request.meta['cat'] + '/' + request.meta['title'] + '/%s.jpg' % img_name

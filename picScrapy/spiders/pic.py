# -*- coding:utf-8 -*-
# ! /bin/bash/python3

import re
from urllib.parse import urljoin
from scrapy.spiders import Spider
from scrapy.http import Request
from picScrapy.items import PicscrapyItem


class PicSpider(Spider):
    name = "pic"  # 定义爬虫名
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    }

    def start_requests(self):
        main_url = 'http://www.jj20.com/bz/'
        yield Request(main_url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//body/div/div[@class="g-class-top"]/a/@href').extract()
        '''this urls is 
        "/bz/zrfg/" 
        "/bz/dwxz/"
        "/bz/hhzw"
        ...
        '''
        if urls is not None:
            for u in urls:
                full_url = urljoin(response.url, u)
                yield Request(url = full_url, callback=self.parse_by_category)

    # 一级页面的处理函数
    def parse_by_category(self, response):
        # 提取界面所有的符合入口条件的url
        all_urls = response.xpath('//div/ul[@class="picbz"]/li/a[1]/@href').extract()
        category_name = response.xpath('//div/div/em/h1/text()').get()

        # all_urls 有4X6=24张图片
        if len(all_urls):
            # 遍历获得的url，继续爬取
            for url in all_urls:
                # urljoin生成完整url地址
                url = urljoin(response.url, url)
                yield Request(url, callback=self.parse_img, meta={'cat': category_name})

        # 能否在本页找到下一页按钮
        next_node = response.xpath('//div[@class="tspage"]/div[@class="tsp_nav"]/a[contains(string(),"下一页")]')
        if next_node is not None:
            next_href = next_node.xpath('.//@href').get()
            next_url = urljoin(response.url, next_href)
            yield Request(url= next_url,callback=self.parse, meta={'cat': category_name})

    # 二级页面的处理函数
    def parse_img(self, response):
        item = PicscrapyItem()
        # 提取页面符合条件的图片地址进行下载
        item['image_urls'] = response.xpath('//img[@id="bigImg"]/@src').extract()
        title = response.xpath('/html/body/div[3]/h1/span/text()').extract()[0]
        item['title'] = title.split('(')[0] + '(' + re.search(r'(\d+)/(\d+)', title).group(2) + ')'
        item['category_name'] = response.meta['cat']
        yield item

        # 提取符合条件的url
        all_urls = response.xpath('//ul[@id="showImg"]/li/a/@href').extract()
        # 遍历获得的url，继续爬取
        for url in all_urls:
            url = urljoin(response.url, url)
            yield Request(url, callback=self.parse_img_img, meta={'cat': response.meta['cat']})

    @staticmethod
    # 三级页面的处理函数
    def parse_img_img(response):
        item = PicscrapyItem()
        # 提取符合条件的图片地址
        item['image_urls'] = response.xpath('//img[@id="bigImg"]/@src').extract()
        title = response.xpath('/html/body/div[3]/h1/span/text()').extract()[0]
        item['title'] = title.split('(')[0] + '(' + re.search(r'(\d+)/(\d+)', title).group(2) + ')'
        item['category_name'] = response.meta['cat']
        yield item

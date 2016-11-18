import scrapy
import re
import os.path
from lxml import etree
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from craigslist_sample.items import VFItem
from scrapy.utils.response import body_or_str

class MySpider(CrawlSpider):
    name = "vf"
    allowed_domains = ["vanityfair.com"]
    start_urls = ['http://www.vanityfair.com/']

    base_url = 'http://www.vanityfair.com/sitemap?year='
    year = ['2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006',
            '2005','2004','2003','2002','2001','2000']
    month = ['&month=12','&month=11','&month=10','&month=9','&month=8','&month=7',
             '&month=6','&month=5','&month=4','&month=3','&month=2','&month=1']
    day = ['&week=5','&week=4','&week=3','&week=2','&week=1']

    def parse(self,response):
        for y in self.year:
            for m in self.month:
                 for d in self.day:
                    url = self.base_url+y+m+d
                    yield scrapy.Request(url,self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        articles = sel.xpath("//ul[@class='list']/li/a").extract()
        for article in articles:
            root = etree.fromstring(article)
            link = root.attrib['href']
            yield scrapy.Request(link,self.parse_items)

    def parse_items(self, response):
        hxs = Selector(response)
        items = []
        item = VFItem()
        item["title"] = hxs.xpath('//h1[@class="hed"]/text()').extract()[0]
        item["article"] = hxs.xpath('//*[contains(@class,"content-section") or contains(@class,"content drop-cap") or contains(@class,"content")]/p/text()').extract()
        item['link'] = response.url
        item["date"] = hxs.xpath('//meta[@name="pubdate"]/@content').extract()[0].encode('utf8')
        items.append(item)

        return items
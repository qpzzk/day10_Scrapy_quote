# -*- coding: utf-8 -*-
import scrapy
from ..items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response): #默认的回调
        quotes=response.css('.quote')
        for quote in quotes:
            item=QuoteItem()  #声明一个item对象
            text=quote.css('.text::text').extract_first()
            author=quote.css('.author::text').extract_first()
            tags=quote.css('.tags .tag::text').extract()
            item['text']=text
            item['author']=author
            item['tags']=tags
            yield item

        #实现下一页的功能
        next=response.css('.pager .next a::attr(href)').extract_first()
        url=response.urljoin(next) #将获取的下一页的url后部分加在原url上面
        yield scrapy.Request(url=url,callback=self.parse) #回调解析方法
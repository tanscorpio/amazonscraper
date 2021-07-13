from typing import Text
import scrapy
from ..items import MyproItem
class Amazon(scrapy.Spider):

    name = 'amazon'
    page_number=2
    start_urls = { 'https://www.amazon.in/s?k=phone&i=electronics&rh=n%3A1389401031&page=1&qid=1626182910&ref=sr_pg_2' }

    def parse(self,response):
        items = MyproItem()

        objects=response.css('div[data-index]')
        for obj in objects:
            productname=obj.css('.a-color-base.a-text-normal::text').extract()
            productprice=obj.css('.a-price-whole::text').extract()
            productimg=obj.css('.s-image::attr(src)').extract()
            items['product_name']=productname
            items['product_img']=productimg
            items['product_price']=productprice
            if len(items['product_price'])==0:
                continue

        # yield { 'a':objects }
            yield items
            next_page='https://www.amazon.in/s?k=phone&i=electronics&rh=n%3A1389401031&page='+ str(Amazon.page_number) +'&qid=1626182910&ref=sr_pg_2'
            if(Amazon.page_number<6):
                Amazon.page_number=Amazon.page_number+1
                yield response.follow(next_page, callback = self.parse)